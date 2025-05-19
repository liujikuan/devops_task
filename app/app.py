from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, world! This is a Flask app running in a Docker container." 


@app.route("/healthz")
def health():
    return "OK", 500


@app.route("/greet")
def greet():
    name = request.args.get("name", "Guest")
    safe_name = ''.join(c for c in name if c.isalnum() or c.isspace())
    return f"Hello, {safe_name}!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
