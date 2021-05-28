from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=["POST", "GET"])
def index():
    return render_template("index.html")

@app.route("/archive")
def view_archive():
    return render_template("archive.html", title="archive")
        
        

if __name__=='__main__':
    app.run(debug=True)