__author__ = 'arian'
import libtorrent as lt
import time
import os
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
            #socketio.emit('newinfo',{'info':info},namespace='/test')
        #time.sleep(5)

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
thread = MyThread(func,args=("magnet:?xt=urn:btih:A35B445EEEB0A4304C25C2AE25FA3A264822FFD8&dn=the+rewrite+2014+720p+brrip+x264+yify&tr=udp%3A%2F%2F9.rarbg.com%3A2710%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.com%3A1337",None),name='test')
thread.start()

#func("magnet:?xt=urn:btih:A35B445EEEB0A4304C25C2AE25FA3A264822FFD8&dn=the+rewrite+2014+720p+brrip+x264+yify&tr=udp%3A%2F%2F9.rarbg.com%3A2710%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.com%3A1337",None)