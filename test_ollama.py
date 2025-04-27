import requests
import logging
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_ollama_streaming():
    """Test the Ollama API using streaming response which is what Ollama actually returns"""
    url = "http://localhost:11434/api/chat"
    
    data = {
        "model": "tinyllama",
        "messages": [
            {
                "role": "user", 
                "content": "Write a simple hello world program in Python"
            }
        ],
        "stream": True
    }
    
    logger.debug(f"Sending request to Ollama at: {url}")
    try:
        response = requests.post(url, json=data, timeout=30, stream=True)
        response.raise_for_status()
        
        # Process the streaming response
        full_content = ""
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                logger.debug(f"Response chunk: {chunk}")
                if "message" in chunk:
                    content = chunk["message"].get("content", "")
                    full_content += content
                    logger.debug(f"Current content: {full_content}")
                if chunk.get("done", False):
                    break
        
        logger.debug(f"Final content: {full_content}")
        return full_content
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return f"Error: {str(e)}"

def test_ollama_non_streaming():
    """Test the Ollama API without streaming"""
    url = "http://localhost:11434/api/chat"
    
    data = {
        "model": "tinyllama",
        "messages": [
            {
                "role": "user", 
                "content": "Write a simple hello world program in Python"
            }
        ],
        "stream": False
    }
    
    logger.debug(f"Sending request to Ollama at: {url}")
    try:
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        logger.debug(f"API Response JSON: {result}")
        
        if "message" in result:
            content = result["message"]["content"]
            logger.debug(f"Content: {content}")
            return content
        else:
            logger.error(f"Unexpected response format: {result}")
            return f"Unexpected response format: {result}"
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Testing Ollama API with streaming...")
    streaming_result = test_ollama_streaming()
    print("\nStreaming result:", streaming_result)
    
    print("\nTesting Ollama API without streaming...")
    non_streaming_result = test_ollama_non_streaming()
    print("\nNon-streaming result:", non_streaming_result) 