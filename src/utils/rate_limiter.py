from fastapi import HTTPException
import time
from collections import defaultdict
from typing import Dict, Tuple

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
        
    def check_rate_limit(self, user_id: str):
        current_time = time.time()
        user_requests = self.requests[user_id]
        
        # Remove requests older than 1 minute
        user_requests = [req for req in user_requests 
                        if current_time - req < 60]
        
        if len(user_requests) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
            
        user_requests.append(current_time)
        self.requests[user_id] = user_requests 