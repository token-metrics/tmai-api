from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from datetime import datetime
import tm_api

class SignalScheduler:
    def __init__(self, bot, subscription_manager):
        """Initialize the scheduler with the bot and subscription manager."""
        self.bot = bot
        self.subscription_manager = subscription_manager
        self.scheduler = BackgroundScheduler()
        self._setup_jobs()
        
    def _setup_jobs(self):
        """Setup scheduled jobs."""
        # Schedule hourly signal updates
        self.scheduler.add_job(
            self.send_top_signals,
            IntervalTrigger(hours=1),
            id='hourly_signals',
            name='Send top signals every hour',
            replace_existing=True
        )
        
        # Schedule daily market summary
        self.scheduler.add_job(
            self.send_market_summary,
            IntervalTrigger(hours=24),
            id='daily_market_summary',
            name='Send daily market summary',
            replace_existing=True
        )
    
    async def send_top_signals(self):
        """Send top signals to all subscribers."""
        logging.info("Running scheduled job: send_top_signals")
        
        # Get active subscribers
        subscribers = self.subscription_manager.get_all_active_subscribers()
        if not subscribers:
            logging.info("No active subscribers for top signals")
            return
        
        # Get top tokens using the alternative method for v2 API
        top_tokens_data = tm_api.get_alternative_top_tokens(limit=3)
        
        if "error" in top_tokens_data:
            logging.error(f"Error fetching top tokens: {top_tokens_data['error']}")
            return
        
        # Prepare the message
        message = f"📊 HOURLY UPDATE ({datetime.now().strftime('%H:%M UTC')})\n\n🔝 TOP SIGNALS:\n"
        
        if "data" in top_tokens_data and top_tokens_data["data"]:
            for i, token in enumerate(top_tokens_data["data"], 1):
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
                
                message += f"{i}. {symbol}: {signal} ({grade}%)\n"
        else:
            message += "No signals available at this time.\n"
        
        # Send to each subscriber
        for user_id, user_data in subscribers.items():
            try:
                chat_id = user_data["chat_id"]
                await self.bot.send_message(chat_id=chat_id, text=message)
                logging.info(f"Sent top signals to user {user_id}")
            except Exception as e:
                logging.error(f"Error sending message to user {user_id}: {e}")
    
    async def send_market_summary(self):
        """Send daily market summary to all subscribers."""
        logging.info("Running scheduled job: send_market_summary")
        
        # Get active subscribers
        subscribers = self.subscription_manager.get_all_active_subscribers()
        if not subscribers:
            logging.info("No active subscribers for market summary")
            return
        
        # Get market metrics using v2 API
        market_data = tm_api.get_market_metrics()
        
        if "error" in market_data:
            logging.error(f"Error fetching market metrics: {market_data['error']}")
            return
        
        # Prepare the message
        message = f"📈 DAILY MARKET SUMMARY ({datetime.now().strftime('%d %b %Y')})\n\n"
        
        if "data" in market_data and market_data["data"]:
            latest = market_data["data"][0]  # Get the most recent data
            
            # Updated to match v2 API response structure
            market_cap = latest.get("TOTAL_CRYPTO_MCAP", 0)
            high_coins_percentage = latest.get("TM_GRADE_PERC_HIGH_COINS", 0)
            grade_signal = latest.get("TM_GRADE_SIGNAL", 0)
            
            # Calculate a sentiment score based on TM_GRADE_PERC_HIGH_COINS
            sentiment_score = min(high_coins_percentage * 4, 100)  # Scale to 0-100
            fear_greed = "Extreme Fear" if sentiment_score < 25 else "Fear" if sentiment_score < 40 else "Neutral" if sentiment_score < 60 else "Greed" if sentiment_score < 80 else "Extreme Greed"
            
            message += f"Market Cap: ${market_cap/1000000000:.2f}B\n"
            message += f"High Quality Tokens: {high_coins_percentage:.2f}%\n"
            message += f"Market Score: {sentiment_score:.0f}/100\n"
            message += f"Sentiment: {fear_greed}\n\n"
            
            # Interpret the TM_GRADE_SIGNAL
            if grade_signal == 1:
                message += "🟢 Market conditions are BULLISH. Consider accumulating quality assets.\n"
            elif grade_signal == -1:
                message += "🔴 Market conditions are BEARISH. Consider caution and risk management.\n"
            else:
                message += "🟡 Market conditions are NEUTRAL. Consider balanced portfolio strategies.\n"
        else:
            message += "No market data available at this time.\n"
        
        # Send to each subscriber
        for user_id, user_data in subscribers.items():
            try:
                chat_id = user_data["chat_id"]
                await self.bot.send_message(chat_id=chat_id, text=message)
                logging.info(f"Sent market summary to user {user_id}")
            except Exception as e:
                logging.error(f"Error sending message to user {user_id}: {e}")
    
    def start(self):
        """Start the scheduler."""
        if not self.scheduler.running:
            self.scheduler.start()
            logging.info("Scheduler started")
    
    def shutdown(self):
        """Shutdown the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logging.info("Scheduler shutdown")