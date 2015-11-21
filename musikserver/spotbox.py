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
                self.process()
                try:
                    cmd = self.cmd_queue.get_nowait()
                    self.process_command(cmd)
                except Empty:
                    t = min(timeout, 100)
                    sleep(t / 1000.0)
            timeout = self.session.process_events()

    def process_command(self, cmd):
        if cmd[0] == "track":
            self.track = self.session.get_link(cmd[1]).as_track()
        elif cmd[0] == "play":
            self.session.player.play()
        elif cmd[0] == "pause":
            self.session.player.pause()

    def process(self):
        if self.track != None and self.track.is_loaded:
            self.session.player.load(self.track)
            self.track = None

    def command(self, cmd):
        self.cmd_queue.put(cmd)
