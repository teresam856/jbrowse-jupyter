from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

def launch():
    app.run()