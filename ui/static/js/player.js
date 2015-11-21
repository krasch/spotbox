socket = createSocket()

player = {

   playTrack: function(trackURI) {
       socket.send("track," + trackURI);
       setTimeout(function() {player.play()}, 100);

       spotify.getTrack(uri)
              .then(ui.player.update, handleError);
   },

   play: function() {
       socket.send("play");
   },

   pause: function() {
       socket.send("pause");
   },
}

function createSocket() {

    ws = new WebSocket("ws://localhost:8080/ws");

    ws.onopen = function() {
          console.log("Socket opened.")
        };

    ws.onmessage = function (evt) {
      var received_msg = evt.data;
      console.log("Received: " + received_msg);
    };

    ws.onclose = function() {
      console.log("Socket closed.");
    };

    return ws;
}