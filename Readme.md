## Installation

Requires python > 3.4

    add repo as described here https://pyspotify.mopidy.com/en/latest/installation/
    sudo apt-get install libspotify-dev
    conda create -n spotbox python=3.5
    pip install pyspotify
    pip install pyalsaaudio
    pip install aiohttp
    pip install pyaml
    cd ui/static/3rdparty/js
    wget https://raw.githubusercontent.com/JMPerez/spotify-web-api-js/master/src/spotify-web-api.js

## Configuring server

Download a binary key from [spotify](https://devaccount.spotify.com/my-account/keys/) and put it into the `musikserver` directory.

Copy `musikservergitt` to  `musikserver/credentials.py" and set your spotify credentials:

## Running server

```
cd musikserver
python server.py
```
