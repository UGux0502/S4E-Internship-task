import requests

def query_ollama(input_text):
    url = "http://localhost:11434/v1/chat/completions"
    
    
    input_text_system = (
        "You are an AI assistant specialized in generating Python code. "
        "Your task is to write Python code based on the user's description. "
        "The response must include a title summarizing the task, followed by the Python code. "
        "The Python code should be well-formatted and functional. "
        "Do not include any explanations, comments, or additional text outside the title and code. "
        "Ensure the code is syntactically correct and adheres to best practices. "
        "If the user's description is unclear, make reasonable assumptions to generate the code. "
        "Always include a title prefixed with 'Title:' on the first line of the response."
    )
    
    
    messages = [
        {"role": "system", "content": input_text_system},
        {"role": "user", "content": input_text}
    ]
    
    
    data = {
        "model": "llama3",
        "messages": messages,
        "stream": False
    }
    
    
    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()
    print("API Response JSON:", result)


    
    if "choices" in result and len(result["choices"]) > 0:
        content = result["choices"][0]["message"]["content"]
        lines = content.strip().split('\n')
        title = lines[0] if lines[0].lower().startswith('title:') else "Generated Code"
        code_output = '\n'.join(lines[1:]) if title != "Generated Code" else content
        return code_output, title
    