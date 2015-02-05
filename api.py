__author__ = 'arian'
from flask import Flask,request,url_for,redirect


import os
app = Flask(__name__,static_url_path=os.getcwd())
@app.route("/")
def index():
    #return redirect(url_for('static', filename='index.html'))
    return app.send_static_file("index.html")
@app.route("/download")
def download():
    magnet = request.args.get("mag")
    return magnet


if __name__ == "__main__":
    app.run()