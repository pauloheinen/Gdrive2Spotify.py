'''
Client ID SPOTIFY 8ad707a87c8445b481c240424ad5998c
Client Secret SPOTIFY d00fda6a444f41cbb4e3bd5528fd8475
https://github.com/plamere/spotipy
https://developer.spotify.com/console/get-users-profile/
'''
import Gdrive as drive

redirect_uri = 'http://localhost:8888/callback'
client_id = '8ad707a87c8445b481c240424ad5998c'
client_secret = 'd00fda6a444f41cbb4e3bd5528fd8475'

import requests
import spotipy
from spotipy.oauth2 import *

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri
                                               ))

usr = sp.current_user()
opcao = 0
while (opcao != '30' or opcao != 31): # seta cima // baixo
    for item in usr:
        print('\r[' + item + ']')
    opcao = input()

playlists = sp.current_user_playlists()
opcao = []
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
    opcao = int(input("Seleção: "))
