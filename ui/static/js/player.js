socket = createSocket()

player = {

   add: function(uri) {
       if (uri.indexOf("spotify:track") > -1)
           socket.send(JSON.stringify({"command": "add","uri": uri}));
       else if (uri.indexOf("spotify:album") > -1) {
           spotify.getAlbumTracks(uri)
                  .then(function(tracks) {
                     for (i in tracks)
                        socket.send(JSON.stringify({"command": "add","uri": tracks[i]}));
                  })
       }
       setTimeout(function() {player.play()}, 100);
   },

   play: function() {
       socket.send(JSON.stringify({"command": "play"}));
   },

   pause: function() {
       socket.send(JSON.stringify({"command": "pause"}));
   },

   next: function() {
       socket.send(JSON.stringify({"command": "next"}));
   },

   clear: function() {
       socket.send(JSON.stringify({"command": "clear"}));
   }
}

function createSocket() {

    ws = new WebSocket("ws://localhost:8080/ws");

    ws.onopen = function() {
          console.log("Socket opened.")
        };

    ws.onmessage = function (evt) {
      var msg = JSON.parse(evt.data);

      if (msg["event"] == "track")
         ui.player.update(msg["uri"])
      else if (msg["event"] == "queued")
         ui.player.displayQueue(msg["tracks"])
      else
        console.log(msg);
    };

    ws.onclose = function() {
      console.log("Socket closed.");
    };

    return ws;
}