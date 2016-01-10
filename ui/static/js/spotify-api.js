/* tiny wrapper around spotify-web-api */

var spotifyApi = new SpotifyWebApi();

var spotify = {}

spotify.cache = {}

spotify.track = {

   resolve: function(trackURI) {

        if (!(trackURI in spotify.cache)) {
            var trackId = trackURI.replace("spotify:track:", "")
            spotify.cache[trackURI] = spotifyApi.getTrack(trackId)
                                                .then(spotify.track.summarize, handleError);
        }

        return spotify.cache[trackURI];
   },

   summarize: function(trackData) {
      return {"uri": trackData["uri"],
              "artist": trackData["artists"][0]["name"],
              "album": trackData["album"]["name"],
              "title": trackData["name"],
              "cover": trackData["album"]["images"][0]["url"]};
   },
}

spotify.album = {
   listTracks: function(albumURI) {
       var albumId = albumURI.replace("spotify:album:", "")
       return spotifyApi.getAlbum(albumId)
                        .then(function (data) {return spotify.util.extractURIs(data["tracks"]["items"])})
                        .catch(handleError)
   },

    search: function(artist) {
        return spotifyApi.searchAlbums('artist:'+artist)
                         .then(function (data) {return spotify.util.extractURIs(data["albums"]["items"])})
                         .catch(handleError)
    },

    resolve: function(albumURI) {
        if (!(albumURI in spotify.cache)) {
            var albumId = albumURI.replace("spotify:album:", "")
            spotify.cache[albumURI] = spotifyApi.getAlbum(albumId)
                                                .then(spotify.album.summarize, handleError);
        }

        return spotify.cache[albumURI];
    },

    summarize: function(albumData) {
      return {"uri": albumData["uri"],
              "artist": albumData["artists"][0]["name"],
              "title": albumData["name"],
              "cover": albumData["images"][0]["url"]};
    }
}

spotify.util = {
    extractURIs: function(items) {
        var uris = [];
        for (i in items){
              uris.push(items[i]["uri"]);
        }
        return uris;
    },

    resolveAll: function(uris, resolverFunction) {
        var resolvers = []
        for (i in uris) {
            resolvers.push(resolverFunction(uris[i]));
        }
        return Promise.all(resolvers)
   }
}
