from typing import Optional
from fastapi import HTTPException

class T24AgentError(Exception):
    """Base exception class for T24 Agent"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class AuthenticationError(T24AgentError):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)

class ValidationError(T24AgentError):
    def __init__(self, message: str = "Invalid input"):
        super().__init__(message, status_code=400)

class TemenosAPIError(T24AgentError):
    def __init__(self, message: str = "Temenos API error"):
        super().__init__(message, status_code=502) 