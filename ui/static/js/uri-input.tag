<uri-input>
    <form onsubmit="{ add }">
       <input type="text" name="spotify_uri" placeholder="spotify uri">
       <input type="submit" value="Add">
    </form>

    <script>

        var self = this;
        var player = opts;

        add(uri) {
            player.add(self.spotify_uri.value);
            self.spotify_uri.value = "";
            self.update();
        }
    </script>

</uri-input>