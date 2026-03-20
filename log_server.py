from flask import Flask
import os

app = Flask(__name__)

# path to your honeypot logs
LOG_FILE = "logs/sessions.log"


@app.route("/")
def home():
    return "<h2>Honeypot Log Server Running</h2><p>Go to /logs</p>"


@app.route("/logs")
def view_logs():

    if not os.path.exists(LOG_FILE):
        return "<h3>Log file not found</h3>"

    with open(LOG_FILE, "r") as f:
        data = f.read()

    # show nicely in browser
    return f"<pre>{data}</pre>"


@app.route("/logs/raw")
def raw_logs():

    if not os.path.exists(LOG_FILE):
        return "Log file not found"

    with open(LOG_FILE, "r") as f:
        return f.read()


@app.route("/logs/json")
def logs_json():

    if not os.path.exists(LOG_FILE):
        return {"error": "Log file not found"}

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    return {"logs": lines}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
