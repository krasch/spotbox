<search>
    <form onsubmit="{ search }">
        <input type="text" name="artist" placeholder="artist name">
        <input type="submit" value="Search">
    </form>

    <br/>

    <div each={ results }>
         <img width="100" src={ cover } class="add-album-link" onclick={addToQueue}> <br/>
         { artist + " - " + title} <br/> <br/>
    </div>


    <script>

        var self = this;
        var controller = opts;

        search() {
            spotify.album.search(self.artist.value, handleError)
                         .then(spotify.album.resolveAll, handleError)
                         .then(showResults);
        }

        function showResults(results) {
            self.results = results;
            self.artist.value = "";
            self.update();
        }

        addToQueue(album) {
            controller.add(album.item.uri);
        }
</script>

</search>