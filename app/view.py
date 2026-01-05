from app import app
from flask import render_template, request

@app.route("/", methods=["GET"])
def homepage():
    termo = request.args.get("q")  
    return render_template("index.html", termo=termo)
