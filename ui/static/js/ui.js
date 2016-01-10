ui = {
   hideAll: function() {
   },

   showPlayer: function() {
        ui.hideAll();
        document.getElementById('player-tab').style.display = "block";
   },

   /*showSearch: function() {
        ui.hideAll();
        document.getElementById('search-tab').style.display = "block";
   },*/

   showUriInput: function() {
        ui.hideAll();
        document.getElementById('uri-tab').style.display = "block";
   }
}

ui.player = {
   update: function(trackURI) {
        spotify.track.resolve(trackURI)
                .then(function(track) {
                     document.getElementById('player-title').innerHTML = track.title
                     document.getElementById('player-artist').innerHTML = track.artist
                     document.getElementById('player-album').innerHTML = track.album
                     document.getElementById('player-img').src = track.cover
                });
   },

};

ui.uriSelection = {
   getUri: function() {
      return document.getElementById("uri-to-add").value;
   },

   clear: function() {
      document.getElementById("uri-to-add").value = '';
   }
}
