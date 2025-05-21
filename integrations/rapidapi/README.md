# Token Metrics RapidAPI Hub Listing

This integration provides the Token Metrics AI API on the RapidAPI Hub marketplace, making it accessible to millions of developers worldwide.

## Features

- Complete OpenAPI 3.1 specification
- Sandbox environment with 10 requests per minute
- Searchable under "crypto ratings" category
- Comprehensive documentation for all endpoints

## Setup Instructions

1. Upload the `openapi.yaml` file to RapidAPI Hub
2. Configure the sandbox environment with a rate limit of 10 requests per minute
3. Set up the upgrade URL to direct users to Token Metrics subscription plans
4. Ensure the listing is searchable under the "crypto ratings" category

## API Endpoints

The integration exposes the following endpoints:

- **GET /ratings** - Retrieve AI-powered ratings for cryptocurrencies
- **GET /metrics** - Get metrics that influence cryptocurrency ratings
- **GET /sentiments** - Access sentiment analysis for cryptocurrencies

## Authentication

The API uses Bearer JWT authentication with the following required claims:
- `plan`: User subscription plan
- `payment_method`: Payment method used
- `stake_score`: Staking score for discounts

## Testing

The integration has been tested to ensure it meets the acceptance criteria:
- Listing is searchable under "crypto ratings" category
- Sandbox environment allows 10 requests per minute
- Upgrade URL directs users to Token Metrics subscription plans
