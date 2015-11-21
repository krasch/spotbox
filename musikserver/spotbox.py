from threading import Thread
from time import sleep
from queue import Queue, Empty
import spotify

class Spotbox(Thread):
    def __init__(self, username, password):
        super(Spotbox, self).__init__()
        self.session = spotify.Session()
        self.session.login(username, password)
        self.cmd_queue = Queue()
        self.running = True
        self.track = None
        self.audio = spotify.AlsaSink(self.session)

    def run(self):
        timeout = 0
        while self.running:
            if timeout != 0:
                if self.track != None and self.track.is_loaded:
                    print("Play")
                    self.session.player.load(self.track)
                    self.session.player.play()
                    self.track = None
                try:
                    cmd = self.cmd_queue.get_nowait()
                    self.process(cmd)
                except Empty:
                    t = min(timeout, 100)
                    sleep(t / 1000.0)
            print (self.track)
            timeout = self.session.process_events()

    def process(self, command):
        cmd, data = command
        if cmd == "track":
            print("Load")
            self.track = self.session.get_link(data).as_track()

    def command(self, cmd):
        self.cmd_queue.put(cmd)

