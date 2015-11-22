from threading import Thread
from time import sleep
from queue import Queue, Empty
from collections import deque
import spotify

class Spotbox:
    def __init__(self, username, password):
        self.session = spotify.Session()
        self.session.login(username, password)
        self.cmd_queue = Queue()
        self.status_queue = Queue()
        self.play_queue = deque()
        self.running = True
        self.track = None
        self.next_track_prefetched = False
        self.audio = spotify.AlsaSink(self.session)
        self.playing = False
        self.session.on(spotify.SessionEvent.END_OF_TRACK, self.end_of_track)

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

    def end_of_track(self, not_used):
        self.next_track()

    def next_track(self):
        self.session.player.unload()
        if len(self.play_queue) == 0:
            self.send("track")
            self.send("paused")
        else:
            self.track = self.play_queue.popleft()
            self.next_track_prefetched = False

    def process_command(self, cmd):
        if cmd[0] == "track":
            self.track = self.session.get_link(cmd[1]).as_track()
        elif cmd[0] == "play":
            self.playing = True
        elif cmd[0] == "pause":
            self.playing = False
        elif cmd[0] == "add":
            self.play_queue.append(self.session.get_link(cmd[1]).as_track())
        elif cmd[0] == "clear":
            self.play_queue = deque()
        elif cmd[0] == "next":
            self.next_track()

    def process(self):

        if not self.next_track_prefetched and len(self.play_queue) > 0 and self.play_queue[0].is_loaded:
            self.session.player.prefetch(self.play_queue[0])
            self.next_track_prefetched = True

        if self.playing and self.session.player.state == spotify.PlayerState.UNLOADED and self.track == None and len(self.play_queue) > 0:
             self.next_track()

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
