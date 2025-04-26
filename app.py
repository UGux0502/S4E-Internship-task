from flask import Flask, request , jsonify , render_template
from flask_cors import CORS
from model import query_ollama

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("page.html")
    elif request.method == "POST":
        user_input = request.json.get("user_input", "")

        code_output, title = query_ollama(user_input)


        return jsonify({"title": title, "code_output": code_output})




if __name__ == "__main__":
    app.run(debug=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)