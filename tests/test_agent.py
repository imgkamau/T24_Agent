import pytest
from src.core.agent import T24Agent
from src.utils.errors import ValidationError

@pytest.fixture
def agent():
    config = {
        'temenos': {
            'base_url': 'http://test.api.temenos.com/v1',
            'api_key': 'test_key'
        }
    }
    return T24Agent(config)

async def test_process_message(agent):
    # Test valid message
    response = await agent.process_message(
        user_id="test_user",
        message="What's my account balance?"
    )
    assert isinstance(response, str)
    assert len(response) > 0

    # Test invalid message
    with pytest.raises(ValidationError):
        await agent.process_message(user_id="test_user", message="") 