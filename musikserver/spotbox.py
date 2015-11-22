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
        self.current_track = None
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
                    data = self.cmd_queue.get_nowait()
                    self.process_command(data['command'], data)
                except Empty:
                    t = min(timeout, 100)
                    sleep(t / 1000.0)
            timeout = self.session.process_events()

    def end_of_track(self, not_used):
        self.next_track()

    def next_track(self):
        self.session.player.unload()
        self.current_track = None
        if len(self.play_queue) == 0:
            self.send_playing()
            self.send_track()
        else:
            self.track = self.play_queue.popleft()
            self.next_track_prefetched = False
            self.send_queue()

    def process_command(self, cmd, data):
        if cmd == "track":
            self.track = self.session.get_link(data['uri']).as_track()
        elif cmd == "play":
            self.playing = True
        elif cmd == "pause":
            self.playing = False
        elif cmd == "add":
            self.play_queue.append(self.session.get_link(data['uri']).as_track())
            self.send_queue()
        elif cmd == "clear":
            self.play_queue = deque()
            self.send_queue()
        elif cmd == "next":
            self.next_track()
        elif cmd == "state":
            self.send_state()

    def process(self):

        if not self.next_track_prefetched and len(self.play_queue) > 0 and self.play_queue[0].is_loaded:
            self.session.player.prefetch(self.play_queue[0])
            self.next_track_prefetched = True

        if self.playing and self.session.player.state == spotify.PlayerState.UNLOADED and self.track == None and len(self.play_queue) > 0:
             self.next_track()

        if self.track != None and self.track.is_loaded:
            self.session.player.load(self.track)
            self.current_track = self.track
            self.send_track()
            self.track = None

        if self.playing and (self.session.player.state == spotify.PlayerState.LOADED or
                        self.session.player.state == spotify.PlayerState.PAUSED):
            self.send_playing()
            self.session.player.play()

        if not self.playing and self.session.player.state == spotify.PlayerState.PLAYING:
            self.send_playing()
            self.session.player.pause()

    def send_state(self):
        self.send_queue()
        self.send_playing()
        self.send_track()

    def send_playing(self):
        self.send("playing", {"state": self.playing})

    def send_track(self):
        if self.current_track != None:
            self.send("track", { "uri": self.current_track.link.uri })
        else:
            self.send("track")

    def send_queue(self):
        self.send("queued", {"tracks": [ { "uri" : t.link.uri } for t in self.play_queue ]})

    def send(self, event, data = {}):
        msg = data.copy()
        msg["event"] = event
        self.status_queue.put(msg)

    def command(self, cmd):
        self.cmd_queue.put(cmd)
