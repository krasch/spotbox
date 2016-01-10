ui = {
   hideAll: function() {
        document.getElementById('search-tab').style.display = "none";
        document.getElementById('player-tab').style.display = "none";
        document.getElementById('uri-tab').style.display = "none";
   },

   showPlayer: function() {
        ui.hideAll();
        document.getElementById('player-tab').style.display = "block";
   },

   showSearch: function() {
        ui.hideAll();
        document.getElementById('search-tab').style.display = "block";
   },

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

ui.search = {
   getSearchPhrase: function() {
      return document.getElementById("search-phrase").value;
   },

   clear: function() {
      document.getElementById("search-phrase").value = '';
   },

   displayResults: function(albumUris) {

     ui.search.clearResults();

     var resultsElement =  document.getElementById('search-results');

     for (i in albumUris) {
        var uri = albumUris[i];

        spotify.album.resolve(uri)
               .then(function(album) {
                  var div = document.createElement("div");
                  resultsElement.appendChild(div);

                  var img = document.createElement("img");
                  img.width = "100";
                  img.src = album.cover;
                  img.addEventListener("click", function() {player.add(album["uri"]);});
                  img.className = img.className + " add-album-link";
                  div.appendChild(img);

                  div.appendChild(document.createElement("br"));

                  var text = document.createTextNode(album.artist + " - " +  album.title);
                  div.appendChild(text);
                  div.appendChild(document.createElement("br"));
                  div.appendChild(document.createElement("br"));
               })
     }
   },

   clearResults: function() {
       var resultsElement =  document.getElementById('search-results');
       while (resultsElement.firstChild) {
           resultsElement.removeChild(resultsElement.firstChild);
       }
   }
}

