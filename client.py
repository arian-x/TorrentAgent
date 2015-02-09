__author__ = 'arian'
import libtorrent as lt
import time
import os
import threading


class Torrent_Client:
    def __init__(self,socketio):
        #link = raw_input("input your magnet: ")
        self.socketio = socketio
        self.threads=[]
        self.ses = lt.session()
        self.ses.listen_on(6881, 6891)
        if not os.path.exists(os.getcwd()+'/downloads'):
            os.mkdir(os.getcwd()+'/downloads')
        self.params = {
            'save_path': os.getcwd()+'/downloads/',
            'storage_mode': lt.storage_mode_t(2),
            'paused': False,
            'auto_managed': True,
            'duplicate_is_error': True}

#link = "magnet:?xt=urn:btih:4MR6HU7SIHXAXQQFXFJTNLTYSREDR5EI&tr=http://tracker.vodo.net:6970/announce"
    def add_torrent(self,magnet,name):
        #new_thread = threading.Thread(target=self.download,args=(magnet,name))
        new_thread = MyThread(self.download,args=(magnet,name),name=name)
        new_thread.start()
        self.threads.append(new_thread)



    def download(self,link,name,parent):
        handle = lt.add_magnet_uri(self.ses, link, self.params)
        self.ses.start_dht()
        print 'downloading metadata...'
        waittime = 0

        while (not handle.has_metadata()):
            time.sleep(1)
            waittime += 1
            print "waiting:",waittime
            if waittime == 20:
                break


        if waittime < 20:
            print 'got metadata, starting torrent download...'
            while (handle.status().state != lt.torrent_status.seeding):
                s = handle.status()
    #print help(s)
                state_str = ['queued', 'checking', 'downloading metadata', \
                    'downloading', 'finished', 'seeding', 'allocating']
                parent.state = state_str[s.state]
                parent.info =  name,": ",'%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s %.3f' % \
                    (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                    s.num_peers, state_str[s.state], s.total_download/1000000)
                self.socketio.emit('newinfo',{'info':parent.info},namespace='/test')
        #time.sleep(5)


class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args + (self,)
        self.state = ''
        print "args are:",self.args
        self.info = ''
    def run(self):
        self.func(*self.args)
    def get_info(self):
        return self.info



#client = Torrent_Client()
#magnet = raw_input("input your magnet: ")
#name = raw_input("input your magnet's name: ")
#client.add_torrent(magnet,name)


# while magnet:
#     client.add_torrent(magnet,name)
#     magnet = raw_input("input your magnet: ")
#     name = raw_input("input your magnet's name: ")
# for i in client.threads:
#     i.join()
#for i in range(10):
#    time.sleep(4)
#    print client.get_info()

