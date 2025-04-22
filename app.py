from flask import Flask, request , jsonify , render_template
from flask_cors import CORS
from model import query_ollama

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET" , "POST"])
def index():
    code_output = ""
    title = ""
    if request.method == "GET":
        return render_template("page.html")
    elif request.method == "POST":
        user_input = request.json.get("user_input", "")
        code_output, title = query_ollama(user_input)
        lines = code_output.strip().split('\n')
        title = lines[0] if lines[0].lower().startswith('title:') else "Generated Code"
        code_output = '\n'.join(lines[1:]) if title != "Generated Code" else code_output
        return jsonify({"title": title, "code_output": code_output})



if __name__ == "__main__":
    app.run(debug=True)
