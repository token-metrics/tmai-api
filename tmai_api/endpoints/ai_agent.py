from tmai_api.base import BaseEndpoint

class AIAgentEndpoint(BaseEndpoint):
    """Endpoint for accessing the AI Agent (chatbot) for token insights"""
    
    def chat(self, messages):
        """Send a message to the Token Metrics AI chatbot.
        
        Args:
            messages (list): List of message objects, each containing a "user" key with the message text
            
        Returns:
            dict: AI chatbot response
        """
        payload = {
            'messages': messages
        }
        
        # Send a POST request with the JSON payload
        return self._request('post', 'tmai', json=payload)
    
    def ask(self, question):
        """Simplified method to ask a single question to the AI chatbot.
        
        Args:
            question (str): The question to ask
            
        Returns:
            dict: AI chatbot response
        """
        messages = [{"user": question}]
        return self.chat(messages)
    
    def get_answer_text(self, question):
        """Get just the answer text from the AI chatbot response.
        
        Args:
            question (str): The question to ask
            
        Returns:
            str: The answer text from the AI chatbot
        """
        response = self.ask(question)
        return response.get("answer", "")
