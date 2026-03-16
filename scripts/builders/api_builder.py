from utils.file_utils import write_file

def build_api():

    code = """

from flask import Flask

app = Flask(__name__)

@app.route("/")
def status():

    return {"status":"ok"}

"""

    write_file("services/api/app.py", code)