__author__ = 'arian'
from flask import Flask,request,url_for,redirect,render_template
from flask.ext.socketio import SocketIO,emit
import json
from threading import *
import random
import time
import client
import test
thread = Thread()
thread_stop_event = Event()
import kickassScraper

import os
app = Flask(__name__,static_url_path=os.getcwd()+"/static")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
Client = client.Torrent_Client(socketio)
@app.route("/")
def index():
    #return redirect(url_for('static', filename='index.html'))
    return render_template("index.html")

@app.route("/download")
def download():
    #global Client
    magnet = request.args.get("mag")
    #Client.add_torrent(magnet,"test")
    thread = MyThread(test.func,args=(magnet,socketio),name="test")
    thread.start()
    return "OK!"
@socketio.on('connect',namespace='/test')
def test_connect():
    #global thread
    print "client connected,ready to download"

    #if not thread.isAlive():
    #    print "Starting thread"
    #    thread = RandomThread()
    #    thread.start()

#@socketio.on('my event')
#def test_message(message):
#    emit('my response',{'data':'got it!'})


@app.route("/scrape")
def scrape():
    tt = "https://kickass.to/search/"
    text = request.args.get("text")
    #print text
    scraper = kickassScraper.Scrape(tt+text)
    #print "here is right"
    out = scraper.scrape(scraper.link)
    #print "out is",out
    return json.dumps(out)
class MyThread(Thread):
    def __init__(self,func,args,name=''):
        Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        print "args are:",self.args
        self.info = ''
    def run(self):
        self.func(*self.args)
    def get_info(self):
        return self.info

class RandomThread(Thread):
    def __self__(self):
        super(RandomThread,self).__init__()
    def randomNumberGenerator(self):
        print "making the number"
        while not thread_stop_event.is_set():
            number = round(random.random()*10,3)
            print number
            socketio.emit('newnumber',{'number':number},namespace='/test')
            time.sleep(1)
    def run(self):
        self.randomNumberGenerator()


if __name__ == "__main__":
    socketio.run(app,host="178.18.25.151",port=8070)
    #app.run()