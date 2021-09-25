"""
Client ID SPOTIFY 8ad707a87c8445b481c240424ad5998c
Client Secret SPOTIFY d00fda6a444f41cbb4e3bd5528fd8475
https://github.com/plamere/spotipy
https://developer.spotify.com/console/get-users-profile/
"""

redirect_uri = 'http://localhost:8888/callback'
client_id = '8ad707a87c8445b481c240424ad5998c'
client_secret = 'd00fda6a444f41cbb4e3bd5528fd8475'

import spotipy
from spotipy.oauth2 import *


class Spotify:

    def __init__(self):
        self.sp = self.login(Spotify)
        self.user = self.sp.current_user()
        self.playlists = self.sp.current_user_playlists()

    # login into spotify profile
    def login(self):
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                       client_secret=client_secret,
                                                       redirect_uri=redirect_uri,
                                                       scope="user-library-read playlist-modify-private playlist-modify-public"
                                                       ))
        print("Logged")
        return sp

    def add(self, item, opcao):
        tracks = ['{}'.format(item)]
        self.sp.playlist_add_items(opcao, tracks, None)

    def playlists(self):
        print("Add into which playlist? ")
        for i, playlist in enumerate(self.playlists['items']):
            print(str(i + 1), playlist['name'])

        opcao = int(input("Opção: "))
        opcao = self.playlists['items'][opcao - 1]['id']
        return opcao


