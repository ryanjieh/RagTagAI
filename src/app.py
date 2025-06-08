from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rate", methods=["POST"])
def rate():
    # placeholder
    return {
        "result": "sample result 10/10 fit 🔥🔥"
    }

if __name__ == "__main__":
    app.run(debug=True)