Requires python > 3.4

add repo here https://pyspotify.mopidy.com/en/latest/installation/
sudo apt-get install libspotify-dev
conda create -n spotbox python=3.5
pip install pyspotify
pip install pyalsaaudio
pip install aiohttp
cd ui/static/3rdparty/js
https://github.com/JMPerez/spotify-web-api-js/blob/master/src/spotify-web-api.js

## Configuring server
Download a binary key from [spotify](https://devaccount.spotify.com/my-account/keys/) and put it into the `musikserver` directory.

Create `musikserver/credentials.py` with your spotify credentials:
```
username = <your spotify username>
password = <your spotify password>
```

## Running server

```
cd musikserver
python server.py
```
