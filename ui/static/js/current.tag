<current>
    <div>
        <img src="{track.cover}" height="200px">
        <div> {track.artist} </div>
        <div> {track.title} </div>
        <div> {track.album} </div>
    </div>

    <script>

        var self = this;
        var emptyTrack = {cover: "img/empty.png"}

        var controller = opts.controller;
        controller.on("track", updateCurrentlyPlaying);

        function updateCurrentlyPlaying(trackURI) {
            if (!trackURI)
                displayTrack(emptyTrack);
            else
                spotify.track.resolve(trackURI).then(displayTrack, handleError);
        }

        function displayTrack(track) {
            self.track = track;
            self.update();
        }
    </script>

</current>
