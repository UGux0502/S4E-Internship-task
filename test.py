import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def test_ollama():
    prompt = "Write a Python function that reverses a string"
    model = "llama3"  # or "mistral" or whatever you pulled

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:
        result = response.json()["response"]
        print("✅ Ollama response:\n")
        print(result)
    else:
        print("❌ Error from Ollama:")
        print(response.text)

if __name__ == "__main__":
    test_ollama()