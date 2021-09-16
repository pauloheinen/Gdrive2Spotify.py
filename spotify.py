'''
Client ID SPOTIFY 8ad707a87c8445b481c240424ad5998c
Client Secret SPOTIFY d00fda6a444f41cbb4e3bd5528fd8475
https://github.com/plamere/spotipy
https://developer.spotify.com/console/get-users-profile/
'''
import drive as drive

redirect_uri = 'http://localhost:8888/callback'
client_id = '8ad707a87c8445b481c240424ad5998c'
client_secret = 'd00fda6a444f41cbb4e3bd5528fd8475'

import spotipy
from spotipy.oauth2 import *
from Gdrive import Gdrive2Spotify

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri
                                               ))

'''atual = sp.user('paulo')
print(atual['external_urls'])'''



'''playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None'''
