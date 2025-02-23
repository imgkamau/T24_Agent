from typing import Dict, Any
import requests
from ..core.security import SecurityManager

class TemenosAPI:
    def __init__(self, config: Dict[str, Any]):
        self.base_url = config["base_url"]
        self.api_key = config["api_key"]
        self.security_manager = SecurityManager()
        
    async def get_balance(self, user_id: str, account: str) -> str:
        """
        Get account balance through Temenos API
        """
        headers = self._get_headers(user_id)
        
        try:
            response = requests.get(
                f"{self.base_url}/accounts/{account}/balance",
                headers=headers
            )
            response.raise_for_status()
            
            data = response.json()
            return f"Your balance is {data['currency']} {data['amount']}"
            
        except requests.exceptions.RequestException as e:
            return f"Sorry, I couldn't fetch your balance: {str(e)}"
            
    async def transfer_funds(self, user_id: str, from_account: str, 
                           to_account: str, amount: float) -> str:
        """
        Execute fund transfer through Temenos API
        """
        headers = self._get_headers(user_id)
        
        payload = {
            "fromAccount": from_account,
            "toAccount": to_account,
            "amount": amount
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/transfers",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            return f"Successfully transferred {amount} to account {to_account}"
            
        except requests.exceptions.RequestException as e:
            return f"Sorry, the transfer failed: {str(e)}"
            
    def _get_headers(self, user_id: str) -> Dict:
        """
        Generate headers for API requests
        """
        return {
            "Authorization": f"Bearer {self.security_manager.get_token(user_id)}",
            "Api-Key": self.api_key,
            "Content-Type": "application/json"
        } 