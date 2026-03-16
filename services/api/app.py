from flask import Flask

app = Flask(__name__)

@app.route("/")
def status():
    return {"status": "NAACP tournament simulation API running"}
