__author__ = 'arian'
from flask import Flask,request,url_for,redirect
#from flask.ext.socketio import SocketIO

import kickassScraper

import os
app = Flask(__name__,static_url_path=os.getcwd()+'/')
#app.config['SECRET_KEY'] = 'secret!'
#socketio = SocketIO(app)

@app.route("/")
def index():
    #return redirect(url_for('static', filename='index.html'))
    return app.send_static_file("index.html")

@app.route("/download")
def download():
    magnet = request.args.get("mag")
    return magnet

@app.route("/scrape")
def scrape():
    text = request.args.get("text")
    scraper = kickassScraper.Scrape(text)
    return scraper


if __name__ == "__main__":
    #socketio.run(app)
    app.run()