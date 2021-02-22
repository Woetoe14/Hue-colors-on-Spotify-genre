from SwSpotify import spotify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from phue import Bridge

# All the genres and the HSV colors (we're working on the color schemes)
genres_to_c = {"dance pop":255, "pop":120, "alternative r&b": 255, "latin": 255}

# Change the values according to your needs
b = Bridge('192.168.1.0') #The ip of your hue bridge
client_id = '' #Your spotify client id, get one from https://developer.spotify.com/dashboard
client_secret = '' #Your spotify client secret, get one from https://developer.spotify.com/dashboard
lights_to_change = ['kitchen', 'Bedroom'] #The name of the lights you want to change

# Connect to the spotify api
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
b.get_api()

while True:
    # Get the current playing song and artist
    song, artist= spotify.current()
    print("song: "+song)
    print("artist: "+artist)

    # Get info about the song and print it
    result = sp.search(song)
    track = result['tracks']['items'][0]
    artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
    album = sp.album(track["album"]["external_urls"]["spotify"])
    print("artist genres:", artist["genres"])
    print("album genres:", album["genres"])
    print("album release-date:", album["release_date"])

    # Something with the color lol need to change this later
    light_names = b.get_light_objects('name')
    try:
        for light in lights_to_change:
            light_names[light].on = True
            light_names[light].brightness = 254
            light_names[light].saturation = 254
            light_names[light].hue = (genres_to_c[artist["genres"][0]]) * 182.0416666666667
    except KeyError:
        print("Whoops we didn't find your genre in the color list")
