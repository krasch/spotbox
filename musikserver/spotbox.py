from threading import Thread
from time import sleep
from queue import Queue, Empty
import spotify

class Spotbox:
    def __init__(self, username, password):
        self.session = spotify.Session()
        self.session.login(username, password)
        self.cmd_queue = Queue()
        self.status_queue = Queue()
        self.running = True
        self.track = None
        self.audio = spotify.AlsaSink(self.session)
        self.playing = False

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
            self.playing = True
        elif cmd[0] == "pause":
            self.playing = False

    def process(self):
        if self.track != None and self.track.is_loaded:
            self.session.player.load(self.track)
            self.send("track", self.track.link.uri)
            self.track = None

        if self.playing and (self.session.player.state == spotify.PlayerState.LOADED or
                        self.session.player.state == spotify.PlayerState.PAUSED):
            self.send("playing")
            self.session.player.play()

        if not self.playing and self.session.player.state == spotify.PlayerState.PLAYING:
            self.send("paused")
            self.session.player.pause()

    def send(self, *msg):
        self.status_queue.put(msg)

    def command(self, cmd):
        self.cmd_queue.put(cmd)
