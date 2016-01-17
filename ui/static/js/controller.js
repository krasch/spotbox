var socketUri = "ws://"+window.location.host+"/ws"

// placeholder, will be overwritten when socket has been created
socket = {}

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

function createSocket() {

    socket = new WebSocket(socketUri);

    socket.onopen = function() {
        console.log("Socket opened.")
    };

    socket.onmessage = function (evt) {
        var msg = JSON.parse(evt.data);
        if (msg["event"] == "track")
            controller.trigger("track", msg["uri"])
        else if (msg["event"] == "queued")
            controller.trigger("queued", msg["tracks"])
        else
            console.log(msg);
    };

    socket.onclose = function() {
        console.log("Socket closed.");
    };
}
