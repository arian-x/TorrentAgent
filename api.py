__author__ = 'arian'
from flask import Flask,request,url_for,redirect,render_template
from flask.ext.socketio import SocketIO,emit
import json
from threading import *
import libtorrent as lt
import random
import time
import client
import test
from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

thread = Thread()
thread_stop_event = Event()
import kickassScraper
import os
app = Flask(__name__,static_url_path=os.getcwd()+"/static")
app.config['SECRET_KEY'] = 'secret!'
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)
socketio = SocketIO(app)
Client = client.Torrent_Client(socketio)
@app.route("/")
def index():
    #return redirect(url_for('static', filename='index.html'))
    return render_template("index.html")
@celery.task()
def func(magnet,socketio):
        ses = lt.session()
        ses.listen_on(6881, 6891)
        if not os.path.exists(os.getcwd()+'/downloads'):
            os.mkdir(os.getcwd()+'/downloads')
        params = {
            'save_path': os.getcwd()+'/downloads/',
            'storage_mode': lt.storage_mode_t(2),
            'paused': False,
            'auto_managed': True,
            'duplicate_is_error': True}

        handle = lt.add_magnet_uri(ses,magnet,params)
        ses.start_dht()
        print 'downloading metadata...'
        waittime = 0
        while (not handle.has_metadata()):
            time.sleep(1)
            waittime += 1
            print "waiting:",waittime
            if waittime == 60:
                break
        if waittime < 60:
            print 'got metadata, starting torrent download...'
            while (handle.status().state != lt.torrent_status.seeding):
                s = handle.status()
                state_str = ['queued', 'checking', 'downloading metadata', \
                        'downloading', 'finished', 'seeding', 'allocating']
                state = state_str[s.state]
                info = '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s %.3f' % \
                       (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                        s.num_peers, state_str[s.state], s.total_download/1000000)
                print info
                socketio.emit('newinfo',{'info':info},namespace='/test')

@app.route("/download")
def download():
    #global Client
    magnet = request.args.get("mag")
    #Client.add_torrent(magnet,"test")
    #func(magnet,socketio)
    func(magnet,socketio)
    #thread = MyThread(func,args=(magnet,socketio),name="test")
    #thread.start()
    #thread.join()
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