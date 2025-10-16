import datetime
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

import requests

from .exceptions import APIRequestError

# Optional pandas support. Import lazily so the core SDK can be used without the
# heavy dependency unless dataframe conversion is explicitly requested.
try:  # pragma: no cover - exercised indirectly when pandas is installed
    import pandas as pd  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - import side effect only
    pd = None

class BaseEndpoint:
    """Base class for all API endpoints"""
    
    def __init__(self, client):
        """Initialize the endpoint with a client instance.
        
        Args:
            client: TokenMetricsClient instance
        """
        self.client = client
        self.base_url = client.base_url
    
    def _request(self, method, endpoint, params=None, json=None):
        """Make a request to the API.
        
        Args:
            method (str): HTTP method (get, post, etc.)
            endpoint (str): API endpoint path
            params (dict, optional): Query parameters for GET requests
            json (dict, optional): JSON payload for POST requests
            
        Returns:
            dict: API response data
        """
        url = f"{self.base_url}/{endpoint}".rstrip("/")
        method = method.upper()

        if method not in {"GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"}:
            raise ValueError(f"Unsupported HTTP method: {method}")

        headers = self.client.build_headers()
        if method in {"POST", "PUT", "PATCH"}:
            headers.setdefault("content-type", "application/json")

        try:
            response = self.client.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json,
                timeout=self.client.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:  # pragma: no cover - requests raises detailed exceptions
            raise APIRequestError(
                endpoint=endpoint,
                method=method,
                params=params,
                status_code=getattr(exc.response, "status_code", None),
            ) from exc

        return response.json()
    
    def _chunk_date_range(self, startDate, endDate, max_days=29):
        """Split a date range into chunks of max_days.
        
        Args:
            startDate (str): Start date in YYYY-MM-DD format
            endDate (str): End date in YYYY-MM-DD format
            max_days (int): Maximum number of days in each chunk
            
        Returns:
            list: List of (chunk_start_date, chunk_end_date) tuples
        """
        if not startDate or not endDate:
            return [(startDate, endDate)]  # If dates not provided, return as is
            
        try:
            start = datetime.datetime.strptime(startDate, "%Y-%m-%d")
            end = datetime.datetime.strptime(endDate, "%Y-%m-%d")
        except ValueError:
            # If date parsing fails, return as is
            return [(startDate, endDate)]
            
        # Check if the range is already within limits
        if (end - start).days <= max_days:
            return [(startDate, endDate)]
            
        # Split into chunks
        result = []
        chunk_start = start
        
        while chunk_start < end:
            # Calculate chunk end date (chunk_start + max_days or end date, whichever is earlier)
            chunk_end = min(chunk_start + datetime.timedelta(days=max_days), end)
            
            # Add to result as strings
            result.append((
                chunk_start.strftime("%Y-%m-%d"),
                chunk_end.strftime("%Y-%m-%d")
            ))
            
            # Move to next chunk
            chunk_start = chunk_end
            
        return result
    
    def _paginated_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        max_days: int = 29,
        custom_limit: Optional[int] = None,
    ) -> Union[Dict[str, Any], List[Any]]:
        """Make paginated requests to handle date ranges and custom pagination logic.
        
        This method handles two forms of pagination:
        1. Date chunking: Splitting long date ranges into <= max_days chunks
        2. Offset-based pagination: Since the API's page parameter doesn't work as expected
        
        Args:
            method (str): HTTP method (get, post, etc.)
            endpoint (str): API endpoint path
            params (dict): Query parameters including startDate and endDate
            max_days (int): Maximum number of days allowed between startDate and endDate
            custom_limit (int, optional): Custom limit value. If None, uses endpoint-specific defaults.
            
        Returns:
            dict: Combined API response data
        """
        # Default limits for different endpoints
        endpoint_limits = {
            'daily-ohlcv': 100,
            'hourly-ohlcv': 1000,
            'trader-grades': 1000,
            'investor-grades': 1000,
            'market-metrics': 1000,
            'trader-indices': 1000,
            'trading-signals': 1000,
            # Default for any other endpoint
            'default': 1000
        }
        params = dict(params or {})
            
        # Extract date parameters
        startDate = params.get('startDate')
        endDate = params.get('endDate')
        
        # Determine the limit to use
        if custom_limit is not None:
            limit = custom_limit
        else:
            # Use endpoint-specific limit
            limit = endpoint_limits.get(endpoint, endpoint_limits['default'])
        
        # Override user-provided limit with our internal limit
        params['limit'] = limit
        
        if 'page' in params:
            del params['page']

        if not startDate or not endDate:
            date_chunks: Iterable[Tuple[Optional[str], Optional[str]]] = [(startDate, endDate)]
        else:
            date_chunks = self._chunk_date_range(startDate, endDate, max_days)

        all_data: List[Any] = []
        combined_meta: Dict[str, Any] = {}
        errors: List[Dict[str, Any]] = []

        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = getattr(
            self.client, "progress_callback", None
        )

        for chunk_start, chunk_end in date_chunks:
            chunk_params = params.copy()
            if chunk_start:
                chunk_params['startDate'] = chunk_start
            if chunk_end:
                chunk_params['endDate'] = chunk_end
            chunk_params['limit'] = limit

            next_page: Optional[int] = params.get('page', 0) or 0

            while True:
                chunk_params['page'] = next_page

                try:
                    response = self._request(method, endpoint, chunk_params)
                except APIRequestError as exc:
                    if self.client.allow_partial_results:
                        errors.append({
                            "chunk": {
                                "startDate": chunk_start,
                                "endDate": chunk_end,
                                "page": next_page,
                            },
                            "error": str(exc),
                        })
                        break
                    raise

                data_items, metadata = self._extract_data(response)

                if data_items:
                    all_data.extend(data_items)

                combined_meta.update(metadata)

                if progress_callback:
                    progress_callback({
                        "endpoint": endpoint,
                        "chunk": {
                            "startDate": chunk_start,
                            "endDate": chunk_end,
                        },
                        "page": next_page,
                        "items_fetched": len(data_items),
                    })

                next_page = self._calculate_next_page(
                    metadata=metadata,
                    previous_page=next_page,
                    received=len(data_items),
                    page_size=limit,
                )

                if next_page is None:
                    break

        result: Union[List[Any], Dict[str, Any]]
        if combined_meta:
            result = dict(combined_meta)
            result['data'] = all_data
        elif all_data and isinstance(all_data[0], dict):
            result = {"data": all_data}
        else:
            result = all_data

        if errors:
            if isinstance(result, dict):
                result = dict(result)
                result['errors'] = errors
                return result
            return {"data": result, "errors": errors}

        if isinstance(result, list):
            return result

        return result

    def _extract_data(self, response: Any) -> Tuple[List[Any], Dict[str, Any]]:
        """Normalize API responses into data payload and metadata."""
        if isinstance(response, dict):
            metadata = {key: value for key, value in response.items() if key != "data"}
            data_payload = response.get("data")
            if isinstance(data_payload, list):
                return data_payload, metadata
            if data_payload is None:
                return [], metadata
            return [data_payload], metadata

        if isinstance(response, list):
            return response, {}

        return [response], {}

    def _calculate_next_page(
        self,
        metadata: Dict[str, Any],
        previous_page: Optional[Any],
        received: int,
        page_size: int,
    ) -> Optional[Any]:
        """Determine the next page identifier based on metadata and payload size."""

        try:
            previous_numeric = int(previous_page) if previous_page is not None else None
        except (TypeError, ValueError):
            previous_numeric = None

        for key in ("next_page", "nextPage", "next_page_token", "nextPageToken"):
            if key in metadata and metadata[key] not in (None, ""):
                try:
                    return int(metadata[key])
                except (TypeError, ValueError):
                    return metadata[key]

        total_pages = metadata.get("total_pages") or metadata.get("totalPages")
        current_page = metadata.get("page") or metadata.get("current_page") or metadata.get("currentPage")
        if total_pages is not None and current_page is not None:
            try:
                if int(current_page) + 1 < int(total_pages):
                    return int(current_page) + 1
                return None
            except (TypeError, ValueError):
                return None

        has_more = metadata.get("has_more") or metadata.get("hasMore")
        if has_more is False:
            return None
        if has_more is True:
            base = previous_numeric if previous_numeric is not None else 0
            return base + 1

        if received < page_size or page_size == 0:
            return None

        if previous_numeric is None:
            return None

        return previous_numeric + 1

    def to_dataframe(self, data):
        """Convert API response data to a pandas DataFrame.
        
        Args:
            data (dict): API response data
            
        Returns:
            pandas.DataFrame: DataFrame containing the response data
        """
        # Implementation depends on the specific structure of each endpoint's response
        # This is a placeholder to be overridden by subclasses
        if pd is None:
            raise ImportError(
                "pandas is required for DataFrame conversion. Install the optional "
                "dependency with `pip install tmai-api[dataframe]` or add pandas "
                "to your project."
            )

        if isinstance(data, list):
            if not data:  # Handle empty list
                return pd.DataFrame()
            return pd.DataFrame(data)
        elif isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
            if not data["data"]:  # Handle empty data array
                return pd.DataFrame()
            return pd.DataFrame(data["data"])
        else:
            return pd.DataFrame([data])
