from flask import Flask, request, jsonify
import logging
from model import query_ollama

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route("/", methods=["POST"])
def index():
    logger.debug("Received POST request")
    logger.debug(f"Headers: {dict(request.headers)}")
    
    try:
        user_input = request.json.get("user_input", "")
        logger.debug(f"Processing user input: {user_input}")
        
        code_output, title = query_ollama(user_input)
        logger.debug(f"Got response - title: {title}, code length: {len(code_output)}")
        
        return jsonify({"title": title, "code_output": code_output})
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True) 