/* tiny wrapper around spotify-web-api */

var spotifyApi = new SpotifyWebApi();

var trackInfoCache = {}

spotify = {

   getTrackInfo: function(trackURI) {

        if (trackURI in trackInfoCache)
            return trackInfoCache[trackURI];

        var trackId = trackURI.replace("spotify:track:", "")
        trackInfoCache[trackURI] = spotifyApi.getTrack(trackId)
                                             .then(spotify.extractTrackInfo, handleError);
        return trackInfoCache[trackURI];
   },

   getAlbumTracks: function(albumURI) {
       var albumId = albumURI.replace("spotify:album:", "")
       return spotifyApi.getAlbum(albumId)
                        .then(spotify.extractTracks, handleError);
   },

   extractTrackInfo: function(trackData) {
      return {"uri": trackData["uri"],
                   "artist": trackData["artists"][0]["name"],
                   "album": trackData["album"]["name"],
                   "title": trackData["name"],
                   "cover": trackData["album"]["images"][0]["url"]};
   },

   extractTracks: function(albumData) {
      // todo if album has more than 50 tracks also need to check the next page
      var tracks = albumData["tracks"]["items"];
      var uris = [];
      for (i in tracks){
          uris.push(tracks[i]["uri"]);
      }
      return uris;
   }
}