from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import logging
import os 
from dotenv import load_dotenv
import tm_api
from subscription_manager import SubscriptionManager
from scheduler import SignalScheduler
from portfolio_manager import PortfolioManager
import sys

# Load environment variables
load_dotenv()

# Configure logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get tokens from environment
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TM_API_KEY = os.getenv("TM_API_KEY")

# Initialize managers
subscription_manager = SubscriptionManager()
portfolio_manager = PortfolioManager()

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    
    welcome_text = (
        f"👋 Welcome to TM Signals Bot, {user.first_name}!\n\n"
        "I provide crypto trading signals powered by Token Metrics AI.\n\n"
        "📊 TRADING SIGNALS:\n"
        "/signal <symbol> - Get a trading signal for a specific token\n"
        "/top - Show top performing tokens right now\n"
        "/market - Get current market sentiment\n\n"
        "💰 PORTFOLIO SIMULATION:\n"
        "/portfolio - View your virtual portfolio\n"
        "/buy <symbol> <amount> - Buy a token\n"
        "/sell <symbol> <amount> - Sell a token\n\n"
        "🔔 NOTIFICATIONS:\n"
        "/subscribe - Receive hourly trading updates\n"
        "/unsubscribe - Stop receiving updates\n\n"
        "Developed for Token Metrics Innovation Challenge"
    )
    
    # Create keyboard with common actions
    keyboard = [
        [
            InlineKeyboardButton("📊 Top Tokens", callback_data="top"),
            InlineKeyboardButton("📈 Market", callback_data="market")
        ],
        [
            InlineKeyboardButton("💼 Portfolio", callback_data="portfolio"),
            InlineKeyboardButton("🔔 Subscribe", callback_data="subscribe")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate a trading signal for a specific token."""
    args = context.args
    
    if not args:
        await update.message.reply_text(
            "⚠️ Please specify a token symbol.\n"
            "Example: /signal btc"
        )
        return
    
    symbol = args[0].lower()
    await update.message.reply_text(f"⏳ Fetching signal for {symbol.upper()}...")
    
    signal_data = tm_api.generate_signal(symbol)
    
    if "error" in signal_data:
        await update.message.reply_text(f"❌ Error: {signal_data['error']}")
        return
    
    message = (
        f"📊 Token: {signal_data['symbol']}\n"
        f"Signal: {signal_data['action']}\n"
        f"Confidence: {signal_data['confidence']}%\n"
        f"Updated: {signal_data['updated_at']}"
    )
    
    # Add buy/sell buttons
    keyboard = [
        [
            InlineKeyboardButton(f"Buy ${100}", callback_data=f"buy_{signal_data['symbol']}_100"),
            InlineKeyboardButton(f"Buy ${500}", callback_data=f"buy_{signal_data['symbol']}_500"),
        ],
        [
            InlineKeyboardButton(f"View Portfolio", callback_data="portfolio"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, reply_markup=reply_markup)

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show top performing tokens."""
    await update.message.reply_text("⏳ Fetching top tokens...")
    
    # Using the alternative method to get top tokens from trading signals
    top_tokens = tm_api.get_alternative_top_tokens(limit=5)
    
    if "error" in top_tokens:
        await update.message.reply_text(f"❌ Error: {top_tokens['error']}")
        return
    
    message = "🔥 TOP TOKENS:\n\n"
    
    if "data" in top_tokens and top_tokens["data"]:
        tokens = []
        for i, token in enumerate(top_tokens["data"], 1):
            symbol = token.get("TOKEN_SYMBOL", "Unknown").upper()
            grade = token.get("TM_TRADER_GRADE", 0)
            
            # Determine signal based on TRADING_SIGNAL
            trading_signal = token.get("TRADING_SIGNAL", 0)
            if trading_signal == 1:
                signal = "BUY ✅"
            elif trading_signal == -1:
                signal = "SELL ❌"
            else:
                signal = "HOLD ⏹️"
            
            message += f"{i}. {symbol} – {signal} ({grade}%)\n"
            tokens.append(symbol)
    else:
        message += "No data available at this time."
        tokens = []
    
    # Add action buttons if we have tokens
    if tokens:
        keyboard = []
        
        # Add a row for each token with its signal button
        for symbol in tokens[:3]:  # Limit to first 3 tokens
            keyboard.append([
                InlineKeyboardButton(f"Signal {symbol}", callback_data=f"signal_{symbol}"),
                InlineKeyboardButton(f"Buy {symbol}", callback_data=f"buy_{symbol}_100")
            ])
            
        # Add portfolio button
        keyboard.append([InlineKeyboardButton("View Portfolio", callback_data="portfolio")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup)
    else:
        await update.message.reply_text(message)

async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current market sentiment."""
    await update.message.reply_text("⏳ Fetching market sentiment...")
    
    # Using get_market_metrics instead of get_market_indicator
    market_data = tm_api.get_market_metrics()
    
    if "error" in market_data:
        await update.message.reply_text(f"❌ Error: {market_data['error']}")
        return
    
    message = "📈 MARKET OVERVIEW:\n\n"
    
    if "data" in market_data and market_data["data"]:
        latest = market_data["data"][0]  # Get the most recent data
        
        # Updated to match v2 API response structure
        market_cap = latest.get("TOTAL_CRYPTO_MCAP", 0)
        date = latest.get("DATE", "Unknown")
        high_coins_percentage = latest.get("TM_GRADE_PERC_HIGH_COINS", 0)
        grade_signal = latest.get("TM_GRADE_SIGNAL", 0)
        
        # Calculate a sentiment score based on TM_GRADE_PERC_HIGH_COINS
        # Higher percentage of high-grade coins indicates more bullish sentiment
        sentiment_score = min(high_coins_percentage * 4, 100)  # Scale to 0-100
        
        fear_greed = "Extreme Fear" if sentiment_score < 25 else "Fear" if sentiment_score < 40 else "Neutral" if sentiment_score < 60 else "Greed" if sentiment_score < 80 else "Extreme Greed"
        
        message += f"Date: {date}\n"
        message += f"Market Cap: ${market_cap/1000000000:.2f}B\n"
        message += f"High Quality Tokens: {high_coins_percentage:.2f}%\n"
        message += f"Market Score: {sentiment_score:.0f}/100\n"
        message += f"Sentiment: {fear_greed}\n\n"
        
        # Interpret the TM_GRADE_SIGNAL
        if grade_signal == 1:
            message += "🟢 Market conditions are BULLISH. Consider accumulating quality assets."
        elif grade_signal == -1:
            message += "🔴 Market conditions are BEARISH. Consider caution and risk management."
        else:
            message += "🟡 Market conditions are NEUTRAL. Consider balanced portfolio strategies."
    else:
        message += "No market data available at this time."
    
    # Add portfolio and top tokens buttons
    keyboard = [
        [
            InlineKeyboardButton("View Portfolio", callback_data="portfolio"),
            InlineKeyboardButton("Top Tokens", callback_data="top")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, reply_markup=reply_markup)

# Portfolio Commands
async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manage user's portfolio."""
    user = update.effective_user
    
    # Check if user has a portfolio
    portfolio = portfolio_manager.get_portfolio(user.id)
    
    if not portfolio:
        # User doesn't have a portfolio yet, offer to create one
        message = (
            "🎮 Virtual Portfolio Simulator\n\n"
            "You don't have a virtual portfolio yet.\n"
            "Create one to practice trading with Token Metrics signals!\n\n"
            "• Start with $10,000 virtual money\n"
            "• Buy and sell crypto based on TM signals\n"
            "• Track your performance\n"
            "• No real money involved"
        )
        
        keyboard = [
            [InlineKeyboardButton("Create Portfolio", callback_data="portfolio_create")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup)
        return
    
    # User has a portfolio, show summary
    success, summary = await portfolio_manager.portfolio_summary(user.id)
    
    if not success:
        await update.message.reply_text(f"❌ Error: {summary}")
        return
    
    # Add action buttons
    keyboard = [
        [
            InlineKeyboardButton("Buy Tokens", callback_data="portfolio_buy"),
            InlineKeyboardButton("Sell Tokens", callback_data="portfolio_sell")
        ],
        [
            InlineKeyboardButton("Performance", callback_data="portfolio_performance"),
            InlineKeyboardButton("Transactions", callback_data="portfolio_transactions")
        ],
        [
            InlineKeyboardButton("Reset Portfolio", callback_data="portfolio_reset")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(summary, reply_markup=reply_markup)

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Buy tokens for the portfolio."""
    args = context.args
    
    if len(args) < 2:
        await update.message.reply_text(
            "⚠️ Please specify a token symbol and amount.\n"
            "Example: /buy btc 100"
        )
        return
    
    symbol = args[0].upper()
    amount = args[1]
    
    # Validate amount
    try:
        amount = float(amount)
        if amount <= 0:
            await update.message.reply_text("⚠️ Amount must be positive.")
            return
    except ValueError:
        await update.message.reply_text("⚠️ Invalid amount. Please provide a number.")
        return
    
    # Execute buy
    success, message = await portfolio_manager.buy(update.effective_user.id, symbol, amount)
    
    # Add portfolio button
    keyboard = [
        [InlineKeyboardButton("View Portfolio", callback_data="portfolio")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, reply_markup=reply_markup)

async def sell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sell tokens from the portfolio."""
    args = context.args
    
    if not args:
        await update.message.reply_text(
            "⚠️ Please specify a token symbol.\n"
            "Example: /sell btc (sells all)\n"
            "Example: /sell btc 0.5 (sells quantity)\n"
            "Example: /sell btc 50% (sells percentage)"
        )
        return
    
    symbol = args[0].upper()
    
    quantity = None
    percentage = None
    
    if len(args) > 1:
        value = args[1]
        
        if value.endswith('%'):
            # Percentage
            try:
                percentage = float(value.rstrip('%'))
            except ValueError:
                await update.message.reply_text("⚠️ Invalid percentage. Please provide a number.")
                return
        else:
            # Quantity
            try:
                quantity = float(value)
            except ValueError:
                await update.message.reply_text("⚠️ Invalid quantity. Please provide a number.")
                return
    
    # Execute sell
    success, message = await portfolio_manager.sell(update.effective_user.id, symbol, quantity, percentage)
    
    # Add portfolio button
    keyboard = [
        [InlineKeyboardButton("View Portfolio", callback_data="portfolio")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, reply_markup=reply_markup)

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Subscribe user to automated alerts."""
    user = update.effective_user
    user_id = user.id
    chat_id = update.effective_chat.id
    username = user.username
    
    if subscription_manager.is_subscribed(user_id):
        await update.message.reply_text("You're already subscribed to alerts! 📬")
        return
    
    success = subscription_manager.subscribe(user_id, chat_id, username)
    
    if success:
        await update.message.reply_text(
            "✅ You are now subscribed to trading signals!\n\n"
            "You'll receive:\n"
            "• Hourly top token signals\n"
            "• Daily market summaries\n\n"
            "You can unsubscribe anytime with /unsubscribe"
        )
    else:
        await update.message.reply_text("❌ Error subscribing. Please try again later.")

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unsubscribe user from automated alerts."""
    user = update.effective_user
    user_id = user.id
    
    if not subscription_manager.is_subscribed(user_id):
        await update.message.reply_text("You're not currently subscribed to any alerts.")
        return
    
    success = subscription_manager.unsubscribe(user_id)
    
    if success:
        await update.message.reply_text(
            "🛑 You've unsubscribed from all alerts.\n"
            "You will no longer receive automatic updates.\n\n"
            "You can subscribe again anytime with /subscribe"
        )
    else:
        await update.message.reply_text("❌ Error unsubscribing. Please try again later.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display help information."""
    help_text = (
        "🤖 TM Signals Bot - Help\n\n"
        "📊 TRADING SIGNALS:\n"
        "/signal <symbol> - Get a trading signal for a specific token\n"
        "/top - Show top performing tokens right now\n"
        "/market - Get current market sentiment\n\n"
        "💰 PORTFOLIO SIMULATION:\n"
        "/portfolio - View your virtual portfolio\n"
        "/buy <symbol> <amount> - Buy a token\n"
        "/sell <symbol> <amount> - Sell a token\n"
        "/sell <symbol> <percent>% - Sell a percentage of your holdings\n\n"
        "🔔 NOTIFICATIONS:\n"
        "/subscribe - Receive hourly trading updates\n"
        "/unsubscribe - Stop receiving updates\n\n"
        "Powered by Token Metrics API"
    )
    
    await update.message.reply_text(help_text)

# Callback Query Handler
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()  # Answer the callback query
    
    data = query.data
    
    if data == "top":
        # Handle top tokens callback
        await query.edit_message_reply_markup(reply_markup=None)
        
        # Instead of creating a new Update object, use the query message directly
        await query.message.reply_text("⏳ Fetching top tokens...")
        
        top_tokens = tm_api.get_alternative_top_tokens(limit=5)
        
        if "error" in top_tokens:
            await query.message.reply_text(f"❌ Error: {top_tokens['error']}")
            return
        
        message = "🔥 TOP TOKENS:\n\n"
        
        if "data" in top_tokens and top_tokens["data"]:
            tokens = []
            for i, token in enumerate(top_tokens["data"], 1):
                symbol = token.get("TOKEN_SYMBOL", "Unknown").upper()
                grade = token.get("TM_TRADER_GRADE", 0)
                
                # Determine signal based on TRADING_SIGNAL
                trading_signal = token.get("TRADING_SIGNAL", 0)
                if trading_signal == 1:
                    signal = "BUY ✅"
                elif trading_signal == -1:
                    signal = "SELL ❌"
                else:
                    signal = "HOLD ⏹️"
                
                message += f"{i}. {symbol} – {signal} ({grade}%)\n"
                tokens.append(symbol)
        else:
            message += "No data available at this time."
            tokens = []
        
        # Add action buttons if we have tokens
        if tokens:
            keyboard = []
            
            # Add a row for each token with its signal button
            for symbol in tokens[:3]:  # Limit to first 3 tokens
                keyboard.append([
                    InlineKeyboardButton(f"Signal {symbol}", callback_data=f"signal_{symbol}"),
                    InlineKeyboardButton(f"Buy {symbol}", callback_data=f"buy_{symbol}_100")
                ])
                
            # Add portfolio button
            keyboard.append([InlineKeyboardButton("View Portfolio", callback_data="portfolio")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(message, reply_markup=reply_markup)
        else:
            await query.message.reply_text(message)
    
    elif data == "market":
        # Handle market sentiment callback
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text("⏳ Fetching market sentiment...")
        
        market_data = tm_api.get_market_metrics()
        
        if "error" in market_data:
            await query.message.reply_text(f"❌ Error: {market_data['error']}")
            return
        
        message = "📈 MARKET OVERVIEW:\n\n"
        
        if "data" in market_data and market_data["data"]:
            latest = market_data["data"][0]  # Get the most recent data
            
            # Updated to match v2 API response structure
            market_cap = latest.get("TOTAL_CRYPTO_MCAP", 0)
            date = latest.get("DATE", "Unknown")
            high_coins_percentage = latest.get("TM_GRADE_PERC_HIGH_COINS", 0)
            grade_signal = latest.get("TM_GRADE_SIGNAL", 0)
            
            # Calculate a sentiment score based on TM_GRADE_PERC_HIGH_COINS
            sentiment_score = min(high_coins_percentage * 4, 100)  # Scale to 0-100
            
            fear_greed = "Extreme Fear" if sentiment_score < 25 else "Fear" if sentiment_score < 40 else "Neutral" if sentiment_score < 60 else "Greed" if sentiment_score < 80 else "Extreme Greed"
            
            message += f"Date: {date}\n"
            message += f"Market Cap: ${market_cap/1000000000:.2f}B\n"
            message += f"High Quality Tokens: {high_coins_percentage:.2f}%\n"
            message += f"Market Score: {sentiment_score:.0f}/100\n"
            message += f"Sentiment: {fear_greed}\n\n"
            
            # Interpret the TM_GRADE_SIGNAL
            if grade_signal == 1:
                message += "🟢 Market conditions are BULLISH. Consider accumulating quality assets."
            elif grade_signal == -1:
                message += "🔴 Market conditions are BEARISH. Consider caution and risk management."
            else:
                message += "🟡 Market conditions are NEUTRAL. Consider balanced portfolio strategies."
        else:
            message += "No market data available at this time."
        
        # Add portfolio and top tokens buttons
        keyboard = [
            [
                InlineKeyboardButton("View Portfolio", callback_data="portfolio"),
                InlineKeyboardButton("Top Tokens", callback_data="top")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(message, reply_markup=reply_markup)
    
    elif data == "portfolio":
        # Handle portfolio callback
        await query.edit_message_reply_markup(reply_markup=None)
        
        # Check if user has a portfolio
        user_id = query.from_user.id
        user_portfolio = portfolio_manager.get_portfolio(user_id)
        
        if not user_portfolio:
            # User doesn't have a portfolio yet, offer to create one
            message = (
                "🎮 Virtual Portfolio Simulator\n\n"
                "You don't have a virtual portfolio yet.\n"
                "Create one to practice trading with Token Metrics signals!\n\n"
                "• Start with $10,000 virtual money\n"
                "• Buy and sell crypto based on TM signals\n"
                "• Track your performance\n"
                "• No real money involved"
            )
            
            keyboard = [
                [InlineKeyboardButton("Create Portfolio", callback_data="portfolio_create")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(message, reply_markup=reply_markup)
            return
        
        # User has a portfolio, show summary
        success, summary = await portfolio_manager.portfolio_summary(user_id)
        
        if not success:
            await query.message.reply_text(f"❌ Error: {summary}")
            return
        
        # Add action buttons
        keyboard = [
            [
                InlineKeyboardButton("Buy Tokens", callback_data="portfolio_buy"),
                InlineKeyboardButton("Sell Tokens", callback_data="portfolio_sell")
            ],
            [
                InlineKeyboardButton("Performance", callback_data="portfolio_performance"),
                InlineKeyboardButton("Transactions", callback_data="portfolio_transactions")
            ],
            [
                InlineKeyboardButton("Reset Portfolio", callback_data="portfolio_reset")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(summary, reply_markup=reply_markup)
    
    elif data == "subscribe":
        # Handle subscribe callback
        await query.edit_message_reply_markup(reply_markup=None)
        
        user_id = query.from_user.id
        chat_id = query.message.chat.id
        username = query.from_user.username
        
        if subscription_manager.is_subscribed(user_id):
            await query.message.reply_text("You're already subscribed to alerts! 📬")
            return
        
        success = subscription_manager.subscribe(user_id, chat_id, username)
        
        if success:
            await query.message.reply_text(
                "✅ You are now subscribed to trading signals!\n\n"
                "You'll receive:\n"
                "• Hourly top token signals\n"
                "• Daily market summaries\n\n"
                "You can unsubscribe anytime with /unsubscribe"
            )
        else:
            await query.message.reply_text("❌ Error subscribing. Please try again later.")
    
    elif data.startswith("signal_"):
        # Handle signal request for a specific token
        symbol = data.split("_")[1]
        await query.edit_message_reply_markup(reply_markup=None)
        
        await query.message.reply_text(f"⏳ Fetching signal for {symbol.upper()}...")
        
        signal_data = tm_api.generate_signal(symbol)
        
        if "error" in signal_data:
            await query.message.reply_text(f"❌ Error: {signal_data['error']}")
            return
        
        message = (
            f"📊 Token: {signal_data['symbol']}\n"
            f"Signal: {signal_data['action']}\n"
            f"Confidence: {signal_data['confidence']}%\n"
            f"Updated: {signal_data['updated_at']}"
        )
        
        # Add buy/sell buttons
        keyboard = [
            [
                InlineKeyboardButton(f"Buy ${100}", callback_data=f"buy_{signal_data['symbol']}_100"),
                InlineKeyboardButton(f"Buy ${500}", callback_data=f"buy_{signal_data['symbol']}_500"),
            ],
            [
                InlineKeyboardButton(f"View Portfolio", callback_data="portfolio"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(message, reply_markup=reply_markup)
    
    elif data.startswith("buy_"):
        # Handle buy request for a specific token
        parts = data.split("_")
        symbol = parts[1]
        amount = float(parts[2])
        
        # Execute buy
        success, message = await portfolio_manager.buy(query.from_user.id, symbol, amount)
        
        # Add portfolio button
        keyboard = [
            [InlineKeyboardButton("View Portfolio", callback_data="portfolio")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)
    
    elif data == "portfolio_create":
        # Create a new portfolio
        success, message = portfolio_manager.create_portfolio(query.from_user.id)
        
        if success:
            # Portfolio created successfully, show it
            success, summary = await portfolio_manager.portfolio_summary(query.from_user.id)
            
            # Add action buttons
            keyboard = [
                [
                    InlineKeyboardButton("Buy Tokens", callback_data="portfolio_buy"),
                    InlineKeyboardButton("Top Tokens", callback_data="top")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(f"{message}\n\n{summary}", reply_markup=reply_markup)
        else:
            # Error creating portfolio
            await query.edit_message_text(message)
    
    elif data == "portfolio_reset":
        # Reset portfolio confirmation
        keyboard = [
            [
                InlineKeyboardButton("✅ Yes, reset", callback_data="portfolio_reset_confirm"),
                InlineKeyboardButton("❌ No, cancel", callback_data="portfolio")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "⚠️ Are you sure you want to reset your portfolio?\n\n"
            "This will delete all your holdings and transactions and start fresh with $10,000.",
            reply_markup=reply_markup
        )
    
    elif data == "portfolio_reset_confirm":
        # Reset the portfolio
        success, message = portfolio_manager.reset_portfolio(query.from_user.id)
        
        if success:
            # Portfolio reset successfully, show it
            success, summary = await portfolio_manager.portfolio_summary(query.from_user.id)
            
            # Add action buttons
            keyboard = [
                [
                    InlineKeyboardButton("Buy Tokens", callback_data="portfolio_buy"),
                    InlineKeyboardButton("Top Tokens", callback_data="top")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(f"{message}\n\n{summary}", reply_markup=reply_markup)
        else:
            # Error resetting portfolio
            await query.edit_message_text(message)
    
    elif data == "portfolio_buy":
        # Show popular tokens to buy
        top_tokens = tm_api.get_alternative_top_tokens(limit=5)
        
        message = "Select a token to buy:\n\n"
        
        keyboard = []
        
        if "data" in top_tokens and top_tokens["data"]:
            # Add buttons for top tokens
            for token in top_tokens["data"]:
                symbol = token.get("TOKEN_SYMBOL", "").upper()
                if symbol:
                    keyboard.append([
                        InlineKeyboardButton(f"Buy {symbol} $100", callback_data=f"buy_{symbol}_100"),
                        InlineKeyboardButton(f"Buy {symbol} $500", callback_data=f"buy_{symbol}_500")
                    ])
        
        # Add common tokens
        keyboard.append([
            InlineKeyboardButton("Buy BTC", callback_data="buy_BTC_100"),
            InlineKeyboardButton("Buy ETH", callback_data="buy_ETH_100")
        ])
        
        # Add back button
        keyboard.append([InlineKeyboardButton("Back to Portfolio", callback_data="portfolio")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup)
    
    elif data == "portfolio_sell":
        # Show user's holdings to sell
        user_portfolio = portfolio_manager.get_portfolio(query.from_user.id)
        
        if not user_portfolio or not user_portfolio.get("holdings", {}):
            await query.edit_message_text(
                "You don't have any holdings to sell.\n\n"
                "Use /buy <symbol> <amount> to buy tokens first.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back to Portfolio", callback_data="portfolio")]])
            )
            return
        
        message = "Select a token to sell:\n\n"
        
        keyboard = []
        
        # Add buttons for each holding
        for symbol in user_portfolio["holdings"]:
            keyboard.append([
                InlineKeyboardButton(f"Sell all {symbol}", callback_data=f"sell_{symbol}_all"),
                InlineKeyboardButton(f"Sell 50% {symbol}", callback_data=f"sell_{symbol}_50pct")
            ])
        
        # Add back button
        keyboard.append([InlineKeyboardButton("Back to Portfolio", callback_data="portfolio")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup)
    
    elif data.startswith("sell_"):
        # Handle sell request
        parts = data.split("_")
        symbol = parts[1]
        sell_type = parts[2]
        
        if sell_type == "all":
            # Sell all holdings
            success, message = await portfolio_manager.sell(query.from_user.id, symbol)
        elif sell_type == "50pct":
            # Sell 50%
            success, message = await portfolio_manager.sell(query.from_user.id, symbol, percentage=50)
        
        # Add portfolio button
        keyboard = [
            [InlineKeyboardButton("View Portfolio", callback_data="portfolio")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)
    
    elif data == "portfolio_performance":
        # Show portfolio performance
        success, message = await portfolio_manager.performance(query.from_user.id)
        
        # Add back button
        keyboard = [
            [InlineKeyboardButton("Back to Portfolio", callback_data="portfolio")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)
    
    elif data == "portfolio_transactions":
        # Show recent transactions
        success, message = portfolio_manager.recent_transactions(query.from_user.id)
        
        # Add back button
        keyboard = [
            [InlineKeyboardButton("Back to Portfolio", callback_data="portfolio")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)
                
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown commands."""
    await update.message.reply_text(
        "Sorry, I didn't understand that command. Try /help to see available commands."
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates."""
    logger.error(f"Exception while handling an update: {context.error}")
    
    # Send error message if this was triggered by a message
    if update and hasattr(update, 'effective_message'):
        await update.effective_message.reply_text(
            "❌ An error occurred while processing your request. Please try again later."
        )

def main():
    """Start the bot."""
    # Check for API keys
    if not BOT_TOKEN:
        logger.error("Telegram Bot Token not found. Please set the TELEGRAM_BOT_TOKEN environment variable.")
        sys.exit(1)
    
    if not TM_API_KEY:
        logger.error("Token Metrics API Key not found. Please set the TM_API_KEY environment variable.")
        sys.exit(1)
    
    # Create the Application
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("signal", signal))
    application.add_handler(CommandHandler("top", top))
    application.add_handler(CommandHandler("market", market))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add portfolio handlers
    application.add_handler(CommandHandler("portfolio", portfolio))
    application.add_handler(CommandHandler("buy", buy))
    application.add_handler(CommandHandler("sell", sell))
    
    # Add callback query handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add handler for unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Initialize and start the scheduler
    scheduler = SignalScheduler(application.bot, subscription_manager)
    scheduler.start()
    
    # Log startup info
    logger.info("🚀 TM Signals Bot is starting...")
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    # Stop the scheduler when the bot is stopped
    scheduler.shutdown()

if __name__ == "__main__":
    main()