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


# login into spotify profile
def login():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri
                                                   ))
    return sp


def add(playlists, sp):
    print("Add into which playlist? ")
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print(str(i+1), playlist['name'])

        opcao = int(input("Opção: "))
        opcao = playlists['items'][opcao-1]['id']
        sp.user_playlist_add_tracks(sp.current_user(), opcao, '1pAyyxlkPuGnENdj4g7Y4f', 1)



def main():
    sp = login()  # sp (spotify) service
    user = sp.current_user()  # user

    playlists = sp.current_user_playlists()
    add(playlists, sp)


if __name__ == '__main__':
    main()
