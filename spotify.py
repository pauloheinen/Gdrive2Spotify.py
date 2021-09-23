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


# login into spotify profile
def login():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri
                                                   ))
    return sp


def search(playlists, id):
    while playlists:
        for i, item in enumerate(playlists['items']):
            print(str(i), playlist['name'])
        if item['id'] == id:
            return item
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None


def add(playlists):
    print("Add into which playlist? ")
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print(str(i), playlist['name'])
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
        opcao = int(input("Opção: "))
        search(playlist, )


def main():
    sp = login()  # sp (spotify) service
    user = sp.current_user()

    playlists = sp.current_user_playlists()
    add(playlists)


if __name__ == '__main__':
    main()
