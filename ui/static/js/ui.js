ui = {
}

ui.player = {
   update: function(trackURI) {
        spotify.getTrackInfo(trackURI)
                .then(function(track) {
                     document.getElementById('player-title').innerHTML = track.title
                     document.getElementById('player-artist').innerHTML = track.artist
                     document.getElementById('player-album').innerHTML = track.album
                     document.getElementById('player-img').src = track.cover
                });
   },

   displayQueue: function(queue) {
        console.log(queue);
        var queueElement =  document.getElementById('queue');

        // empty the old queue
       while (queueElement.firstChild) {
           queueElement.removeChild(queueElement.firstChild);
       }

        for (i in queue) {
           var uri = queue[i]["uri"];

           var div = document.createElement("div");
           queueElement.appendChild(div);

           spotify.getTrackInfo(uri)
                  .then(function(track) {
                      var text = document.createTextNode(track.artist + " - " +  track.title);
                      div.appendChild(text);
                      div.appendChild(document.createElement("br"));
                  });

        }
   }

};

ui.uriSelection = {
   getUri: function() {
      return document.getElementById("uri-to-add").value;
   },

   clear: function() {
      document.getElementById("uri-to-add").value = '';
   }
}
