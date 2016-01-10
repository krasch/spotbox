<queue>
    <div each={ tracks }>{ artist + " - " + title}<br/></div>

    <script>
        var self = this;

        opts.on("queued", updateQueue);

        function updateQueue(queue) {
           queue = spotify.util.extractURIs(queue);
           spotify.track.resolveAll(queue)
                        .then(showQueue);
        }

        function showQueue(queue) {
            self.tracks = queue;
            self.update();
        }
    </script>
</queue>