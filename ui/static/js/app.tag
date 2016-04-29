<app>

    <div id="top-bar">
       <a href="#player"><button type="button">Player</button></a>
       <a href="#search"><button type="button">Search</button></a>
       <a href="#uri-input"><button type="button">Enter URI</button></a>
    </div>

    <div id="player">
        <current controller={ opts }></current> <br/>
        <player-control controller={ opts }></player-control> <br/><br/>
        <queue controller={ opts }></queue>
    </div>
    <search id="search" controller={ opts } style="display:none"></search>
    <uri-input id="uri-input" controller={ opts } style="display:none"></uri-input>

    <script>
        function showTab(tabId) {
            // extremely simple router - take a path and make tab with that id visible, make all other tabs invisible
            document.getElementById("player").style.display = "none";
            document.getElementById("search").style.display = "none";
            document.getElementById("uri-input").style.display = "none";
            document.getElementById(tabId).style.display = "block";
        }
	this.on("mount", function() {
            riot.route(showTab);
            riot.route.start(true)

            // player is the first page user will see
            riot.route('player');

            // only now create the socket connection. this makes sure that no messages are lost while tags are mounting
            createSocket();
        });
    </script>

</app>
