import json
import os
import logging
from datetime import datetime, timedelta
import requests
import tm_api

# Configure logging
logging.basicConfig(level=logging.INFO)

class PortfolioManager:
    def __init__(self, storage_file="portfolios.json"):
        """Initialize the portfolio manager."""
        self.storage_file = storage_file
        self.portfolios = self._load_portfolios()
    
    def _load_portfolios(self):
        """Load portfolios from the JSON file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                logging.error(f"Error decoding {self.storage_file}. Starting with empty portfolio list.")
                return {}
        return {}
    
    def _save_portfolios(self):
        """Save portfolios to the JSON file."""
        try:
            with open(self.storage_file, 'w') as file:
                json.dump(self.portfolios, file, indent=2)
        except Exception as e:
            logging.error(f"Error saving portfolios: {e}")
    
    def create_portfolio(self, user_id, initial_balance=10000):
        """Create a new portfolio for a user."""
        user_id = str(user_id)  # Convert to string for JSON compatibility
        
        # Check if portfolio already exists
        if user_id in self.portfolios:
            return False, "You already have a portfolio."
        
        # Create new portfolio
        self.portfolios[user_id] = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "initial_balance": initial_balance,
            "current_balance": initial_balance,
            "holdings": {},
            "transactions": []
        }
        
        self._save_portfolios()
        return True, f"Portfolio created with ${initial_balance} initial balance."
    
    def get_portfolio(self, user_id):
        """Get a user's portfolio."""
        user_id = str(user_id)
        
        if user_id not in self.portfolios:
            return None
        
        return self.portfolios[user_id]
    
    def reset_portfolio(self, user_id, initial_balance=10000):
        """Reset a user's portfolio."""
        user_id = str(user_id)
        
        if user_id not in self.portfolios:
            return False, "You don't have a portfolio yet. Use /portfolio create to start."
        
        # Reset portfolio
        self.portfolios[user_id] = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "initial_balance": initial_balance,
            "current_balance": initial_balance,
            "holdings": {},
            "transactions": []
        }
        
        self._save_portfolios()
        return True, f"Portfolio reset with ${initial_balance} initial balance."
    
    async def buy(self, user_id, symbol, amount):
        """Buy a token in the user's portfolio."""
        user_id = str(user_id)
        symbol = symbol.upper()
        
        # Validate portfolio exists
        if user_id not in self.portfolios:
            return False, "You don't have a portfolio yet. Use /portfolio create to start."
        
        portfolio = self.portfolios[user_id]
        
        # Validate amount
        try:
            amount = float(amount)
            if amount <= 0:
                return False, "Amount must be positive."
        except ValueError:
            return False, "Invalid amount. Please provide a number."
        
        # Check if user has enough balance
        if amount > portfolio["current_balance"]:
            return False, f"Insufficient balance. You have ${portfolio['current_balance']:.2f} available."
        
        # Get current price using CoinGecko API (free and reliable)
        try:
            # Use CoinGecko API for price data
            symbol_lower = symbol.lower()
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol_lower}&vs_currencies=usd"
            response = requests.get(url)
            data = response.json()
            
            if symbol_lower not in data:
                # Try with mapping common symbols
                coin_mapping = {
                    "btc": "bitcoin",
                    "eth": "ethereum",
                    "sol": "solana",
                    "bnb": "binancecoin",
                    "xrp": "ripple",
                    "ada": "cardano",
                    "doge": "dogecoin",
                    "dot": "polkadot",
                    "matic": "polygon",
                    "link": "chainlink",
                    "avax": "avalanche"
                }
                
                if symbol_lower in coin_mapping:
                    coin_id = coin_mapping[symbol_lower]
                    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
                    response = requests.get(url)
                    data = response.json()
                    if coin_id in data:
                        price = data[coin_id]["usd"]
                    else:
                        return False, f"Could not get price for {symbol}."
                else:
                    return False, f"Could not get price for {symbol}. Try a popular coin like BTC or ETH."
            else:
                price = data[symbol_lower]["usd"]
                
        except Exception as e:
            logging.error(f"Error fetching price: {e}")
            return False, f"Error fetching price for {symbol}."
        
        # Calculate quantity
        quantity = amount / price
        
        # Update portfolio
        portfolio["current_balance"] -= amount
        
        if symbol in portfolio["holdings"]:
            # Average down the purchase price
            current_quantity = portfolio["holdings"][symbol]["quantity"]
            current_value = current_quantity * portfolio["holdings"][symbol]["price"]
            new_value = amount
            total_value = current_value + new_value
            total_quantity = current_quantity + quantity
            avg_price = total_value / total_quantity if total_quantity > 0 else price
            
            portfolio["holdings"][symbol]["quantity"] += quantity
            portfolio["holdings"][symbol]["price"] = avg_price
        else:
            portfolio["holdings"][symbol] = {
                "quantity": quantity,
                "price": price
            }
        
        # Record transaction
        transaction = {
            "type": "buy",
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "amount": amount,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        portfolio["transactions"].append(transaction)
        
        self._save_portfolios()
        
        # Get trading signal to compare with user's action
        signal_data = tm_api.generate_signal(symbol)
        signal_advice = ""
        
        if "error" not in signal_data:
            action = signal_data.get("action", "").split()[0]  # Get just BUY/SELL/HOLD without emoji
            confidence = signal_data.get("confidence", 0)
            
            if action == "BUY":
                signal_advice = f"\n\n✅ Smart move! TM AI has a {confidence}% confidence BUY signal for {symbol}."
            elif action == "HOLD":
                signal_advice = f"\n\n⚠️ Note: TM AI currently has a HOLD signal for {symbol} with {confidence}% confidence."
            elif action == "SELL":
                signal_advice = f"\n\n⚠️ Caution: TM AI currently has a SELL signal for {symbol} with {confidence}% confidence."
        
        return True, f"Successfully bought {quantity:.6f} {symbol} at ${price:.2f} per token.{signal_advice}"
    
    async def sell(self, user_id, symbol, quantity=None, percentage=None):
        """Sell a token from the user's portfolio."""
        user_id = str(user_id)
        symbol = symbol.upper()
        
        # Validate portfolio exists
        if user_id not in self.portfolios:
            return False, "You don't have a portfolio yet. Use /portfolio create to start."
        
        portfolio = self.portfolios[user_id]
        
        # Check if user has the token
        if symbol not in portfolio["holdings"]:
            return False, f"You don't own any {symbol}."
        
        current_quantity = portfolio["holdings"][symbol]["quantity"]
        
        # Determine quantity to sell
        sell_quantity = 0
        if quantity is not None:
            try:
                sell_quantity = float(quantity)
            except ValueError:
                return False, "Invalid quantity. Please provide a number."
        elif percentage is not None:
            try:
                percentage = float(percentage)
                if percentage <= 0 or percentage > 100:
                    return False, "Percentage must be between 0 and 100."
                sell_quantity = current_quantity * (percentage / 100)
            except ValueError:
                return False, "Invalid percentage. Please provide a number between 0 and 100."
        else:
            # If no quantity or percentage specified, sell all
            sell_quantity = current_quantity
        
        # Validate quantity
        if sell_quantity <= 0:
            return False, "Quantity must be positive."
        
        if sell_quantity > current_quantity:
            return False, f"You only have {current_quantity:.6f} {symbol} available."
        
        # Get current price
        try:
            # Use CoinGecko API for price data
            symbol_lower = symbol.lower()
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol_lower}&vs_currencies=usd"
            response = requests.get(url)
            data = response.json()
            
            if symbol_lower not in data:
                # Try with mapping common symbols
                coin_mapping = {
                    "btc": "bitcoin",
                    "eth": "ethereum",
                    "sol": "solana",
                    "bnb": "binancecoin",
                    "xrp": "ripple",
                    "ada": "cardano",
                    "doge": "dogecoin",
                    "dot": "polkadot",
                    "matic": "polygon",
                    "link": "chainlink",
                    "avax": "avalanche"
                }
                
                if symbol_lower in coin_mapping:
                    coin_id = coin_mapping[symbol_lower]
                    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
                    response = requests.get(url)
                    data = response.json()
                    if coin_id in data:
                        price = data[coin_id]["usd"]
                    else:
                        return False, f"Could not get price for {symbol}."
                else:
                    return False, f"Could not get price for {symbol}."
            else:
                price = data[symbol_lower]["usd"]
                
        except Exception as e:
            logging.error(f"Error fetching price: {e}")
            return False, f"Error fetching price for {symbol}."
        
        # Calculate sell amount
        sell_amount = sell_quantity * price
        
        # Update portfolio
        portfolio["current_balance"] += sell_amount
        
        # Calculate profit/loss
        buy_price = portfolio["holdings"][symbol]["price"]
        profit_loss = (price - buy_price) * sell_quantity
        profit_loss_percentage = ((price / buy_price) - 1) * 100 if buy_price > 0 else 0
        
        if sell_quantity == current_quantity:
            # Sold all tokens
            del portfolio["holdings"][symbol]
        else:
            # Update holding
            portfolio["holdings"][symbol]["quantity"] -= sell_quantity
        
        # Record transaction
        transaction = {
            "type": "sell",
            "symbol": symbol,
            "quantity": sell_quantity,
            "price": price,
            "amount": sell_amount,
            "profit_loss": profit_loss,
            "profit_loss_percentage": profit_loss_percentage,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        portfolio["transactions"].append(transaction)
        
        self._save_portfolios()
        
        # Format profit/loss message
        profit_loss_msg = (
            f"Profit: ${profit_loss:.2f} (+{profit_loss_percentage:.2f}%)" 
            if profit_loss >= 0 
            else f"Loss: ${abs(profit_loss):.2f} ({profit_loss_percentage:.2f}%)"
        )
        
        # Get trading signal to compare with user's action
        signal_data = tm_api.generate_signal(symbol)
        signal_advice = ""
        
        if "error" not in signal_data:
            action = signal_data.get("action", "").split()[0]  # Get just BUY/SELL/HOLD without emoji
            confidence = signal_data.get("confidence", 0)
            
            if action == "SELL":
                signal_advice = f"\n\n✅ Smart move! TM AI has a {confidence}% confidence SELL signal for {symbol}."
            elif action == "HOLD":
                signal_advice = f"\n\n⚠️ Note: TM AI currently has a HOLD signal for {symbol} with {confidence}% confidence."
            elif action == "BUY":
                signal_advice = f"\n\n⚠️ Note: TM AI currently has a BUY signal for {symbol} with {confidence}% confidence."
        
        return True, f"Successfully sold {sell_quantity:.6f} {symbol} at ${price:.2f} per token.\n{profit_loss_msg}{signal_advice}"
    
    async def portfolio_summary(self, user_id):
        """Get a summary of the user's portfolio."""
        user_id = str(user_id)
        
        # Validate portfolio exists
        if user_id not in self.portfolios:
            return False, "You don't have a portfolio yet. Use /portfolio create to start."
        
        portfolio = self.portfolios[user_id]
        
        # Calculate total portfolio value
        total_value = portfolio["current_balance"]
        holdings_value = 0
        holdings_summary = []
        
        # Get current prices for all tokens
        for symbol, holding in portfolio["holdings"].items():
            try:
                # Try to get price from CoinGecko
                symbol_lower = symbol.lower()
                url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol_lower}&vs_currencies=usd"
                response = requests.get(url)
                data = response.json()
                
                if symbol_lower not in data:
                    # Try with mapping common symbols
                    coin_mapping = {
                        "btc": "bitcoin",
                        "eth": "ethereum",
                        "sol": "solana",
                        "bnb": "binancecoin",
                        "xrp": "ripple",
                        "ada": "cardano",
                        "doge": "dogecoin",
                        "dot": "polkadot",
                        "matic": "polygon",
                        "link": "chainlink",
                        "avax": "avalanche"
                    }
                    
                    if symbol_lower in coin_mapping:
                        coin_id = coin_mapping[symbol_lower]
                        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
                        response = requests.get(url)
                        data = response.json()
                        if coin_id in data:
                            current_price = data[coin_id]["usd"]
                        else:
                            current_price = holding["price"]  # Use purchase price as fallback
                    else:
                        current_price = holding["price"]  # Use purchase price as fallback
                else:
                    current_price = data[symbol_lower]["usd"]
                    
            except Exception as e:
                logging.error(f"Error fetching price for {symbol}: {e}")
                current_price = holding["price"]  # Use purchase price as fallback
            
            quantity = holding["quantity"]
            purchase_price = holding["price"]
            current_value = quantity * current_price
            purchase_value = quantity * purchase_price
            profit_loss = current_value - purchase_value
            profit_loss_percentage = ((current_price / purchase_price) - 1) * 100 if purchase_price > 0 else 0
            
            holdings_value += current_value
            
            # Get trading signal for this token
            signal_data = tm_api.generate_signal(symbol)
            signal = "N/A"
            confidence = 0
            
            if "error" not in signal_data:
                signal = signal_data.get("action", "N/A").split()[0]  # Get just BUY/SELL/HOLD without emoji
                confidence = signal_data.get("confidence", 0)
            
            # Add to summary
            holding_summary = {
                "symbol": symbol,
                "quantity": quantity,
                "purchase_price": purchase_price,
                "current_price": current_price,
                "purchase_value": purchase_value,
                "current_value": current_value,
                "profit_loss": profit_loss,
                "profit_loss_percentage": profit_loss_percentage,
                "signal": signal,
                "confidence": confidence
            }
            holdings_summary.append(holding_summary)
        
        # Sort holdings by value (highest first)
        holdings_summary.sort(key=lambda x: x["current_value"], reverse=True)
        
        # Calculate portfolio performance
        total_value += holdings_value
        initial_balance = portfolio["initial_balance"]
        total_profit_loss = total_value - initial_balance
        total_profit_loss_percentage = ((total_value / initial_balance) - 1) * 100 if initial_balance > 0 else 0
        
        # Format summary
        summary = f"🗂 PORTFOLIO SUMMARY\n\n"
        summary += f"💰 Total Value: ${total_value:.2f}\n"
        summary += f"💵 Cash: ${portfolio['current_balance']:.2f}\n"
        summary += f"📈 Holdings: ${holdings_value:.2f}\n"
        
        if total_profit_loss >= 0:
            summary += f"✅ Profit: ${total_profit_loss:.2f} (+{total_profit_loss_percentage:.2f}%)\n\n"
        else:
            summary += f"❌ Loss: ${abs(total_profit_loss):.2f} ({total_profit_loss_percentage:.2f}%)\n\n"
        
        if holdings_summary:
            summary += "📊 HOLDINGS:\n"
            for holding in holdings_summary:
                symbol = holding["symbol"]
                quantity = holding["quantity"]
                current_value = holding["current_value"]
                profit_loss = holding["profit_loss"]
                profit_loss_pct = holding["profit_loss_percentage"]
                signal = holding["signal"]
                
                profit_indicator = "📈" if profit_loss >= 0 else "📉"
                signal_emoji = "✅" if signal == "BUY" else "❌" if signal == "SELL" else "⏹️"
                
                summary += f"{profit_indicator} {symbol}: {quantity:.6f} (${current_value:.2f})\n"
                summary += f"    P/L: {'+'if profit_loss >= 0 else ''}{profit_loss_pct:.2f}% (${profit_loss:.2f})\n"
                summary += f"    Signal: {signal} {signal_emoji} ({holding['confidence']}%)\n"
        else:
            summary += "No holdings yet. Use /buy to start investing!"
        
        return True, summary
    
    async def performance(self, user_id):
        """Get performance analysis of the user's portfolio."""
        user_id = str(user_id)
        
        # Validate portfolio exists
        if user_id not in self.portfolios:
            return False, "You don't have a portfolio yet. Use /portfolio create to start."
        
        portfolio = self.portfolios[user_id]
        
        # Analyze transactions
        if not portfolio["transactions"]:
            return False, "No transactions yet. Use /buy to start investing!"
        
        total_trades = len(portfolio["transactions"])
        winning_trades = 0
        losing_trades = 0
        total_profit = 0
        total_loss = 0
        
        for transaction in portfolio["transactions"]:
            if transaction["type"] == "sell":
                profit_loss = transaction.get("profit_loss", 0)
                if profit_loss > 0:
                    winning_trades += 1
                    total_profit += profit_loss
                else:
                    losing_trades += 1
                    total_loss += abs(profit_loss)
        
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        profit_factor = total_profit / total_loss if total_loss > 0 else float('inf')
        
        # Calculate portfolio performance
        total_portfolio_value = portfolio["current_balance"]
        
        # Get current values of holdings
        for symbol, holding in portfolio["holdings"].items():
            try:
                # Get current price
                symbol_lower = symbol.lower()
                url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol_lower}&vs_currencies=usd"
                response = requests.get(url)
                data = response.json()
                
                if symbol_lower not in data:
                    # Try with mapping common symbols
                    coin_mapping = {
                        "btc": "bitcoin",
                        "eth": "ethereum",
                        "sol": "solana",
                        "bnb": "binancecoin",
                        "xrp": "ripple",
                        "ada": "cardano",
                        "doge": "dogecoin",
                        "dot": "polkadot",
                        "matic": "polygon",
                        "link": "chainlink",
                        "avax": "avalanche"
                    }
                    
                    if symbol_lower in coin_mapping:
                        coin_id = coin_mapping[symbol_lower]
                        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
                        response = requests.get(url)
                        data = response.json()
                        if coin_id in data:
                            current_price = data[coin_id]["usd"]
                        else:
                            current_price = holding["price"]  # Use purchase price as fallback
                    else:
                        current_price = holding["price"]  # Use purchase price as fallback
                else:
                    current_price = data[symbol_lower]["usd"]
                    
            except Exception as e:
                logging.error(f"Error fetching price for {symbol}: {e}")
                current_price = holding["price"]  # Use purchase price as fallback
            
            quantity = holding["quantity"]
            current_value = quantity * current_price
            total_portfolio_value += current_value
        
        # Calculate overall performance
        initial_balance = portfolio["initial_balance"]
        total_profit_loss = total_portfolio_value - initial_balance
        total_profit_loss_percentage = ((total_portfolio_value / initial_balance) - 1) * 100 if initial_balance > 0 else 0
        
        # Calculate hypothetical performance if followed all TM signals
        # (This is simplified - in a real app, you'd need historical signal data)
        
        # Format performance report
        report = f"📊 PERFORMANCE ANALYSIS\n\n"
        report += f"Initial Investment: ${initial_balance:.2f}\n"
        report += f"Current Value: ${total_portfolio_value:.2f}\n"
        
        if total_profit_loss >= 0:
            report += f"Overall Profit: ${total_profit_loss:.2f} (+{total_profit_loss_percentage:.2f}%)\n\n"
        else:
            report += f"Overall Loss: ${abs(total_profit_loss):.2f} ({total_profit_loss_percentage:.2f}%)\n\n"
        
        report += f"Total Trades: {total_trades}\n"
        report += f"Winning Trades: {winning_trades}\n"
        report += f"Losing Trades: {losing_trades}\n"
        report += f"Win Rate: {win_rate:.2f}%\n"
        report += f"Profit Factor: {profit_factor:.2f}x\n\n"
        
        # Compare with TM signals (basic implementation)
        correct_signals = 0
        total_signals = 0
        
        for transaction in portfolio["transactions"]:
            if "signal_followed" in transaction:
                total_signals += 1
                if transaction.get("signal_profit", False):
                    correct_signals += 1
        
        signal_accuracy = (correct_signals / total_signals) * 100 if total_signals > 0 else 0
        
        if total_signals > 0:
            report += f"📡 TOKEN METRICS SIGNALS\n"
            report += f"Signals Followed: {total_signals}\n"
            report += f"Correct Signals: {correct_signals}\n"
            report += f"Signal Accuracy: {signal_accuracy:.2f}%\n\n"
            
            if signal_accuracy > win_rate:
                report += "✨ Following TM signals would have improved your performance!"
            else:
                report += "😎 Your trading is currently outperforming the TM signals!"
        else:
            report += "No signal data available yet. Keep trading to build performance metrics!"
        
        return True, report
    
    def recent_transactions(self, user_id, limit=5):
        """Get recent transactions for a user."""
        user_id = str(user_id)
        
        # Validate portfolio exists
        if user_id not in self.portfolios:
            return False, "You don't have a portfolio yet. Use /portfolio create to start."
        
        portfolio = self.portfolios[user_id]
        
        if not portfolio["transactions"]:
            return False, "No transactions yet. Use /buy to start investing!"
        
        # Get recent transactions
        recent = sorted(portfolio["transactions"], key=lambda x: x["timestamp"], reverse=True)[:limit]
        
        # Format transactions
        message = f"🕒 RECENT TRANSACTIONS (Last {len(recent)})\n\n"
        
        for i, transaction in enumerate(recent, 1):
            tx_type = transaction["type"].upper()
            symbol = transaction["symbol"]
            quantity = transaction["quantity"]
            price = transaction["price"]
            amount = transaction["amount"]
            timestamp = transaction["timestamp"]
            
            emoji = "💰" if tx_type == "BUY" else "💸"
            
            message += f"{i}. {emoji} {tx_type} {symbol}\n"
            message += f"   {quantity:.6f} @ ${price:.2f} = ${amount:.2f}\n"
            message += f"   Date: {timestamp}\n"
            
            if tx_type == "SELL" and "profit_loss" in transaction:
                profit_loss = transaction["profit_loss"]
                profit_loss_pct = transaction["profit_loss_percentage"]
                profit_emoji = "📈" if profit_loss >= 0 else "📉"
                
                message += f"   {profit_emoji} P/L: {'+'if profit_loss >= 0 else ''}{profit_loss_pct:.2f}% (${profit_loss:.2f})\n"
            
            message += "\n"
        
        return True, message