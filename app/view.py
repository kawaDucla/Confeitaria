
from app import app
from flask import render_template


# Tela inicial
@app.route("/", methods=['GET', 'POST'])
def homepage ():
    return render_template("index.html")



