import requests

def query_ollama(input_text):
    url = "http://localhost:11434/v1/chat/completions"
    
    input_text_system = (
        "you are a helpful assistant. "
        "You Write python code for the user. "
        "Generate the code based on the description below. "
        "Return only Python code and a title summarizing the job."
        "Just answer for code question nothing else. "
        "Do not include any explanation or additional information. "
     )
    data = {
        "model": "codellama",
        "prompt": f"{input_text_system}\n\nUser prompt: {input_text}",
        "stream": False
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()
    print("api data: ", response)
    if "choices" in result and len(result["choices"]) > 0:
        content = result["choices"][0]["message"]["content"]
        lines = content.strip().split('\n')
        title = lines[0] if lines[0].lower().startswith('title:') else "Generated Code"
        code_output = '\n'.join(lines[1:]) if title != "Generated Code" else content
        return code_output, title
    else:
        raise ValueError("Unexpected response format: {}".format(result))