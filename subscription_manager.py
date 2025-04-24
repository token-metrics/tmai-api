import json
import os
import logging
from datetime import datetime

# Configure logs
logging.basicConfig(level=logging.INFO)

class SubscriptionManager:
    def __init__(self, storage_file="subscribers.json"):
        self.storage_file = storage_file
        self.subscribers = self._load_subscribers()
    
    def _load_subscribers(self):
        """Load subscribers from the JSON file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                logging.error(f"Error decoding {self.storage_file}. Starting with empty subscriber list.")
                return {}
        return {}
    
    def _save_subscribers(self):
        """Save subscribers to the JSON file."""
        try:
            with open(self.storage_file, 'w') as file:
                json.dump(self.subscribers, file)
        except Exception as e:
            logging.error(f"Error saving subscribers: {e}")
    
    def subscribe(self, user_id, chat_id, username=None):
        """Subscribe a user to receive alerts."""
        user_id = str(user_id)  # Convert to string for JSON compatibility
        
        self.subscribers[user_id] = {
            "chat_id": chat_id,
            "username": username,
            "subscribed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "active": True
        }
        
        self._save_subscribers()
        return True
    
    def unsubscribe(self, user_id):
        """Unsubscribe a user from alerts."""
        user_id = str(user_id)
        
        if user_id in self.subscribers:
            self.subscribers[user_id]["active"] = False
            self._save_subscribers()
            return True
        return False
    
    def is_subscribed(self, user_id):
        """Check if a user is subscribed."""
        user_id = str(user_id)
        return user_id in self.subscribers and self.subscribers[user_id]["active"]
    
    def get_all_active_subscribers(self):
        """Get all active subscribers."""
        return {uid: data for uid, data in self.subscribers.items() 
                if data.get("active", False)}
    
    def get_subscriber_count(self):
        """Get the count of active subscribers."""
        return len(self.get_all_active_subscribers())