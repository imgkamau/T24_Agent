from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import yaml
from core.agent import T24Agent
from dotenv import load_dotenv
from utils.logger import setup_logger
from utils.rate_limiter import RateLimiter

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger(__name__)

# Initialize rate limiter
rate_limiter = RateLimiter(requests_per_minute=60)

app = FastAPI(
    title="T24 Agent API",
    description="AI-powered banking assistant integrated with Temenos T24",
    version="1.0.0"
)

# Load configuration
with open("config/config.yaml") as f:
    config = yaml.safe_load(f)

# Initialize agent
agent = T24Agent(config)

class Message(BaseModel):
    user_id: str
    content: str

@app.post("/chat", 
    response_model=dict,
    summary="Process chat message",
    description="Process a user message and return appropriate banking information")
async def chat(message: Message):
    try:
        # Check rate limit
        rate_limiter.check_rate_limit(message.user_id)
        
        logger.info(f"Processing message for user {message.user_id}")
        response = await agent.process_message(message.user_id, message.content)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 