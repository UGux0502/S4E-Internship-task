from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from model import query_ollama, get_available_models
import logging
import os

def warm_up_ollama():
    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    if "://" in ollama_host and ":11434" not in ollama_host:
        ollama_host = f"{ollama_host}:11434"

    url = f"{ollama_host}/api/generate"

    try:
        response = requests.post(url, json={
            "model": "tinyllama",  # veya sen hangi modeli kullanıyorsan
            "prompt": "Say Hello",
            "stream": False
        }, timeout=10)
        
        print("Warm-up response:", response.status_code)
    
    except Exception as e:
        print("Warm-up failed:", str(e))
    
app = Flask(__name__)
warm_up_ollama()
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure logging
logging.basicConfig(level=logging.DEBUG)

    
@app.route("/", methods=["GET", "POST"])
def index():
    app.logger.debug(f"Received {request.method} request")
    app.logger.debug(f"Headers: {dict(request.headers)}")
    
    if request.method == "GET":
        # Get available models for the dropdown
        models = get_available_models()
        app.logger.debug(f"Available models: {models}")
        return render_template("page.html", models=models)
    elif request.method == "POST":
        app.logger.debug("Received POST request with data: %s", request.get_data())
        try:
            user_input = request.json.get("user_input", "")
            selected_model = request.json.get("model", "llama3.2")
            app.logger.debug(f"Processing user input with model: {selected_model}")
            
            code_output, title = query_ollama(user_input, selected_model)
            app.logger.debug("Got response - title: %s, code length: %d", title, len(code_output))
            
            return jsonify({"title": title, "code_output": code_output})
        except Exception as e:
            app.logger.error("Error processing request: %s", str(e), exc_info=True)
            return jsonify({"error": str(e)}), 500

@app.route("/models", methods=["GET"])
def get_models():
    """API endpoint to get available models"""
    try:
        models = get_available_models()
        return jsonify({"models": models})
    except Exception as e:
        app.logger.error("Error fetching models: %s", str(e), exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)