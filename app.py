from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    """
    Simple home endpoint.
    """
    return "Hello from Python Static Site!", 200


@app.route("/health")
def health():
    """
    Health check endpoint.
    """
    return jsonify(status="ok"), 200


if __name__ == "__main__":
    # Dev mode; in Docker we’ll use gunicorn
    app.run(host="0.0.0.0", port=8000)
