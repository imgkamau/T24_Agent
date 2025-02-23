from typing import Dict, Any
import openai
from ..integrations.temenos_api import TemenosAPI
from ..core.nlp_processor import NLPProcessor
from ..core.security import SecurityManager

class T24Agent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.nlp_processor = NLPProcessor()
        self.temenos_api = TemenosAPI(config['temenos'])
        self.security_manager = SecurityManager()
        
    async def process_message(self, user_id: str, message: str) -> str:
        """
        Process incoming user message and return appropriate response
        """
        # Verify user authentication
        if not self.security_manager.is_authenticated(user_id):
            return "Please authenticate first."
            
        # Process natural language
        intent, entities = await self.nlp_processor.analyze(message)
        
        # Handle different intents
        response = await self._handle_intent(intent, entities, user_id)
        
        return response
        
    async def _handle_intent(self, intent: str, entities: Dict, user_id: str) -> str:
        """
        Handle different user intents
        """
        if intent == "check_balance":
            account = entities.get("account")
            return await self.temenos_api.get_balance(user_id, account)
            
        elif intent == "transfer_funds":
            return await self._handle_transfer(entities, user_id)
            
        # Add more intent handlers as needed
        
        return "I'm not sure how to help with that. Could you please rephrase?"
        
    async def _handle_transfer(self, entities: Dict, user_id: str) -> str:
        """
        Handle fund transfer intent
        """
        required_fields = ["from_account", "to_account", "amount"]
        
        # Check if all required fields are present
        if not all(field in entities for field in required_fields):
            return "Please provide all transfer details: from account, to account, and amount."
            
        # Perform transfer through Temenos API
        result = await self.temenos_api.transfer_funds(
            user_id,
            entities["from_account"],
            entities["to_account"],
            entities["amount"]
        )
        
        return result 