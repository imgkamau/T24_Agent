from typing import Dict, Tuple
from openai import OpenAI

class NLPProcessor:
    def __init__(self):
        self.conversation_history = []
        self.client = OpenAI()
        
    async def analyze(self, message: str) -> Tuple[str, Dict]:
        """
        Analyze user message to determine intent and extract entities
        """
        # Add message to conversation history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Use OpenAI to analyze the message
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """
                You are a banking assistant. Analyze the user message and extract:
                1. The main intent (e.g., check_balance, transfer_funds, etc.)
                2. Relevant entities (account numbers, amounts, etc.)
                Return your analysis in a structured format.
                """},
                *self.conversation_history
            ]
        )
        
        # Process the response to extract intent and entities
        analysis = self._parse_gpt_response(response.choices[0].message.content)
        
        return analysis["intent"], analysis["entities"]
        
    def _parse_gpt_response(self, response: str) -> Dict:
        """
        Parse GPT response into structured format
        """
        # Implement parsing logic here
        # This is a simplified example
        return {
            "intent": "check_balance",
            "entities": {"account": "main"}
        } 