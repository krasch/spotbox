<current>
    <div>
        <img src="{track.cover}" height="200px">
        <div> {artist} </div>
        <div> {title} </div>
        <div> {album} </div>
    </div>

    <script>
        var self = this;
        self.track = {}
        self.track.cover = "img/empty.png"

        opts.on("track", updateCurrentlyPlaying);

        function updateCurrentlyPlaying(trackURI) {
            spotify.track.resolve(trackURI)
                         .then(function(track) {self.track = track;
                                                self.update();});
        }
    </script>

</current>