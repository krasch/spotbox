socketUri = "ws://"+window.location.host+"/ws"
socket = createSocket(socketUri)

player = riot.observable()
player.add = function(uri) {
    if (uri.indexOf("spotify:track") > -1)
        socket.send(JSON.stringify({"command": "add","uri": uri}));
    else if (uri.indexOf("spotify:album") > -1) {
        spotify.album.listTracks(uri)
            .then(function(tracks) {
                for (i in tracks)
                    socket.send(JSON.stringify({"command": "add","uri": tracks[i]}));
            })
    }
    setTimeout(function() {player.play()}, 100);
}

player.play = function() {
    socket.send(JSON.stringify({"command": "play"}));
}

player.pause = function() {
    socket.send(JSON.stringify({"command": "pause"}));
},

player.next = function() {
    socket.send(JSON.stringify({"command": "next"}));
}

player.clear = function() {
    socket.send(JSON.stringify({"command": "clear"}));
}

function createSocket(uri) {

    ws = new WebSocket(uri);

    ws.onopen = function() {
        console.log("Socket opened.")
    };

    ws.onmessage = function (evt) {
        var msg = JSON.parse(evt.data);

        if (msg["event"] == "track")
            player.trigger("track", msg["uri"])
        else if (msg["event"] == "queued")
            player.trigger("queued", msg["tracks"])
        else
            console.log(msg);
    };

    ws.onclose = function() {
        console.log("Socket closed.");
    };

    return ws;
}
