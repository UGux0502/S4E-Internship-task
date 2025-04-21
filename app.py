from flask import Flask
from flask import Flask, render_template, request , jsonify
from model import query_ollama
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    code_output = ""
    title = ""

    if request.method == "POST":
        user_input = request.form["user_input"]
        code_output, title = query_ollama(user_input)
        lines = code_output.strip().split('\n')
        title = lines[0] if lines[0].lower().startswith('title:') else "Generated Code"
        code_output = '\n'.join(lines[1:]) if title != "Generated Code" else code_output
    return render_template("index.html", code_output=code_output, title=title)




if __name__ == "__main__":
    app.run(debug=True)
