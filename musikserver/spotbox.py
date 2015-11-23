import sys
from threading import Thread
from time import sleep
from queue import Queue, Empty, Full
from collections import deque
import spotify

class Spotbox:
    def __init__(self, username, password, buffer_size = 8):
        self.session = spotify.Session()
        self.session.login(username, password)
        self.cmd_queue = Queue()
        self.status_queue = Queue()
        self.sound_queue = Queue(buffer_size)
        self.play_queue = deque()
        self.running = True
        self.track = None
        self.current_track = None
        self.next_track_prefetched = False
        self.playing = False
        self.session.on(spotify.SessionEvent.END_OF_TRACK, self.end_of_track)
        self.session.on(spotify.SessionEvent.MUSIC_DELIVERY, self.music_delivery)

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

    def music_delivery(self, not_used, audio_format, frames, num_frames):
        try:
            self.sound_queue.put_nowait((audio_format.sample_rate, audio_format.channels, audio_format.frame_size(), frames, num_frames))
            return num_frames
        except Full:
            return 0

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

class Alsa:
    def __init__(self, sound_queue, device='default'):
        self._device_name = device

        import alsaaudio  # Crash early if not available
        self._alsaaudio = alsaaudio
        self._device = None
        self._sound_queue = sound_queue
        self.running = True

    def run(self):
        while(self.running):
            self._music_delivery(*self._sound_queue.get())

        if self._device is not None:
            self._device.close()
            self._device = None

    def _music_delivery(self, sample_rate, channels, frame_size, frames, num_frames):
        if self._device is None:
            if hasattr(self._alsaaudio, 'pcms'):  # pyalsaaudio >= 0.8
                self._device = self._alsaaudio.PCM(device=self._device_name)
            else:  # pyalsaaudio == 0.7
                self._device = self._alsaaudio.PCM(card=self._device_name)
            if sys.byteorder == 'little':
                self._device.setformat(self._alsaaudio.PCM_FORMAT_S16_LE)
            else:
                self._device.setformat(self._alsaaudio.PCM_FORMAT_S16_BE)
            self._device.setrate(sample_rate)
            self._device.setchannels(channels)
            self._device.setperiodsize(num_frames * frame_size)

        self._device.write(frames)
