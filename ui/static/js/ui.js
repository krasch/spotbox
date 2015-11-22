ui = {
}

ui.player = {
   update: function(track) {
        document.getElementById('player-title').innerHTML = track.title
        document.getElementById('player-artist').innerHTML = track.artist
        document.getElementById('player-album').innerHTML = track.album
        document.getElementById('player-img').src = track.cover
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
