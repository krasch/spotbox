player = {
   playTrack: function(track) {
        document.getElementById('player-title').innerHTML = track.title
        document.getElementById('player-artist').innerHTML = track.artist
        document.getElementById('player-album').innerHTML = track.album
        document.getElementById('player-img').src = track.cover
        document.getElementById("track-uri").value = '';
   },


};