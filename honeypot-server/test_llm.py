import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from llm import LLM, CircuitBreaker

# Mock the OpenAI client to avoid real API costs during tests
@pytest.fixture
def mock_llm():
    with patch("llm.AsyncOpenAI") as mock_openai:
        # Create instance with dummy key
        llm_instance = LLM(api_key="fake-key")
        
        # Mock the create method structure
        mock_create = AsyncMock()
        mock_openai.return_value.chat.completions.create = mock_create
        
        llm_instance.client.chat.completions.create = mock_create
        return llm_instance

@pytest.mark.asyncio
async def test_sanitization(mock_llm):
    # Setup mock to return unsafe markdown
    mock_response = AsyncMock()
    mock_response.choices[0].message.content = "```bash\nroot\n```"
    mock_llm.client.chat.completions.create.return_value = mock_response

    response = await mock_llm.answer("whoami")
    
    # Expect markdown stripping
    assert "```" not in response
    assert response.strip() == "root"

@pytest.mark.asyncio
async def test_circuit_breaker_activates(mock_llm):
    # Setup mock to raise exceptions
    mock_llm.client.chat.completions.create.side_effect = Exception("API Down")
    
    # Force the breaker to trip (threshold is 3)
    await mock_llm.answer("test1")
    await mock_llm.answer("test2")
    await mock_llm.answer("test3")
    
    assert mock_llm.circuit.state == "OPEN"
    
    # 4th request should not even try to hit the API mock
    response = await mock_llm.answer("test4")
    assert response == "Connection timed out"

@pytest.mark.asyncio
async def test_caching(mock_llm):
    # Setup mock to return a value
    mock_response = AsyncMock()
    mock_response.choices[0].message.content = "cached_response"
    mock_llm.client.chat.completions.create.return_value = mock_response
    
    # First call triggers API
    await mock_llm.answer("ls -la")
    assert mock_llm.client.chat.completions.create.call_count == 1
    
    # Second call should hit cache (API count stays 1)
    await mock_llm.answer("ls -la")
    assert mock_llm.client.chat.completions.create.call_count == 1