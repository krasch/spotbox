/* tiny wrapper around spotify-web-api */

var spotifyApi = new SpotifyWebApi();

spotify = {

   getTrack: function(trackURI) {
        var trackId = trackURI.replace("spotify:track:", "")
        return spotifyApi.getTrack(trackId)
                         .then(spotify.extractTrackInfo, handleError)
   },

   extractTrackInfo: function(trackData) {
      return {"uri": trackData["uri"],
              "artist": trackData["artists"][0]["name"],
              "album": trackData["album"]["name"],
              "title": trackData["name"],
              "cover": trackData["album"]["images"][0]["url"]}
    }
}