<queue>
    <div each={ tracks }>{ artist + " - " + title}<br/></div>

    <script>
        var self = this;

        opts.on("queued", updateQueue);

        function updateQueue(queue) {
           queue = spotify.util.extractURIs(queue);
           spotify.util.resolveAll(queue, spotify.track.resolve)
                       .then(updateUI);
        }

        function updateUI(queue) {
            self.tracks = queue;
            self.update();
        }
    </script>
</queue>