import requests
import sys
import time
import json
import os

def get_available_models():
    """Query Ollama API to get a list of available models"""

    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    

    if "://" in ollama_host and ":11434" not in ollama_host:
        ollama_host = f"{ollama_host}:11434"
    
    url = f"{ollama_host}/api/tags"
    
    try:

        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt+1}/{max_retries} to get models from Ollama at {url}")
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                models_data = response.json()

                if "models" in models_data:
                    return [model["name"] for model in models_data["models"]]
                return []
                
            except requests.exceptions.ConnectionError as e:
                if attempt < max_retries - 1:
                    print(f"Connection attempt {attempt+1} failed. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Error connecting to Ollama: {str(e)}", file=sys.stderr)
                    return []
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"Timeout on attempt {attempt+1}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("Timeout error connecting to Ollama", file=sys.stderr)
                    return []
    
    except Exception as e:
        print(f"Error getting models from Ollama: {str(e)}", file=sys.stderr)
        return []

def query_ollama(input_text, model="llama3.2"):

    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    

    if "://" in ollama_host and ":11434" not in ollama_host:
        ollama_host = f"{ollama_host}:11434"
    
    url = f"{ollama_host}/api/generate"
    

    print(f"Connecting to Ollama at: {url}")

    if(model == "tinyllama"):
        input_text_system = 'Write only Python code defining a Job class that extends Task, with run(self) and calculate_score(self) methods, no explanations or extra text.'
    else:
        input_text_system = '''You are a Python code generator.
Task:
- Given a user prompt, create:
  - First line: Title: [Short and meaningful title] (no stars, no formatting, just plain text).
  - Then: Directly write the full Python code without any markdown symbols like ```.

Rules:
- Import from s4e.config and s4e.task as needed.
- Always define a class named Job(Task).
- Implement run(self) and calculate_score(self) methods.
- Initialize self.output['detail'], self.output['compact'], and self.output['video'] in run(self).
- Follow the user prompt instructions carefully in the code.
- Use only Python standard libraries (requests, re, os, etc).
- Do NOT write any explanation, note, or additional comment after the code.

Very important:
- Do not wrap code inside triple backticks (```) or any markdown formatting.
- Do not add extra empty lines or decorative lines.
- Only output: first the title line, then the full code.
- Nothing else.

Example user prompt:
"Parse info.log file for username:password pattern and test login."

Example output:

Title: Parse Log File for Credentials and Test Login

from s4e.config import *
from s4e.task import Task
import re
import requests

class Job(Task):
    def run(self):
        asset = self.asset
        self.output['detail'] = []
        self.output['compact'] = []
        self.output['video'] = []

        log_contents = open('/path/to/info.log', 'r').read()
        pattern = r'(\w+:[\w@#$%^&]+)'
        matches = re.findall(pattern, log_contents)

        if matches:
            for match in matches:
                username, password = match.split(':')
                response = requests.post(f"https://auth.s4e.io/login", data={'username': username, 'password': password})
                if 'OK' in response.text:
                    self.output['detail'].append(f'Successful login with {username}:{password}')
                    self.output['compact'].append('Valid credentials found.')
                    self.output['video'].append('Performed login test.')

        else:
            self.output['detail'].append('No valid credentials found.')
            self.output['compact'].append('No success.')

    def calculate_score(self):
        successful = any('Successful login' in item for item in self.output['detail'])
        self.score = 10 if successful else 1


'''


    messages = [
        {"role": "system", "content": input_text_system},
        {"role": "user", "content": input_text}
    ]

    data = {
        "model": model,
        "prompt": input_text_system + "\n\n" + input_text,
        "stream": True  
    }

    try:

        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt+1}/{max_retries} to connect to Ollama at {url}")
                response = requests.post(url, json=data, timeout=60, stream=True)  # Increased timeout and enabled streaming
                response.raise_for_status()
                

                full_content = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            print(f"Received chunk: {len(line)} bytes")
                            
                            if "response" in chunk:
                                content = chunk["response"]
                                full_content += content
                            

                            if chunk.get("done", False):
                                break
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")
                            continue
                
                print(f"Final content length: {len(full_content)}")
                

                if full_content:
                    lines = full_content.strip().split('\n')
                    title = lines[0] if lines and lines[0].lower().startswith('title:') else "Generated Code"
                    code_output = '\n'.join(lines[1:]) if title != "Generated Code" else full_content
                    return code_output, title
                else:
                    error_msg = "No content received from Ollama"
                    print(error_msg, file=sys.stderr)
                    return error_msg, "Error"
                    
            except requests.exceptions.ConnectionError as e:
                if attempt < max_retries - 1:
                    print(f"Connection attempt {attempt+1} failed. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise e
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"Timeout on attempt {attempt+1}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise
    
    except Exception as e:
        error_message = f"Error connecting to Ollama: {str(e)}"
        print(error_message, file=sys.stderr)
        return error_message, "Error"
