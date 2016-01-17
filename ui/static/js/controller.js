socketUri = "ws://"+window.location.host+"/ws"
socket = createSocket(socketUri)

controller = riot.observable()

controller.add = function(uri) {
    if (uri.indexOf("spotify:track") > -1)
        socket.send(JSON.stringify({"command": "add","uri": uri}));
    else if (uri.indexOf("spotify:album") > -1) {
        spotify.album.listTracks(uri)
            .then(function(tracks) {
                for (i in tracks)
                    socket.send(JSON.stringify({"command": "add","uri": tracks[i]}));
            })
    }
    setTimeout(function() {controller.play()}, 100);
}

controller.play = function() {
    socket.send(JSON.stringify({"command": "play"}));
}

controller.pause = function() {
    socket.send(JSON.stringify({"command": "pause"}));
},

controller.next = function() {
    socket.send(JSON.stringify({"command": "next"}));
}

controller.clear = function() {
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
            controller.trigger("track", msg["uri"])
        else if (msg["event"] == "queued")
            controller.trigger("queued", msg["tracks"])
        else
            console.log(msg);
    };

    ws.onclose = function() {
        console.log("Socket closed.");
    };

    return ws;
}
