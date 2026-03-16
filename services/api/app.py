from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def root():
    return jsonify({
        "status": "ok",
        "service": "naacp tournament simulation api"
    })

@app.get("/health")
def health():
    return jsonify({"healthy": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
