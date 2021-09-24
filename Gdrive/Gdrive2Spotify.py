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
    print(sp.me)
    return sp


def add(user, playlists, sp):
    print("Add into which playlist? ")
    while playlists:
        # https://developer.spotify.com/documentation/web-api/reference/#category-playlists
        for i, playlist in enumerate(playlists['items']):
            print(str(i+1), playlist['name'])

        opcao = int(input("Opção: "))
        opcao = playlists['items'][opcao-1]['id']
        print(opcao)
        sp.user_playlist_add_tracks(user=user, playlist_id=opcao, tracks="3479kk78dx3GFt048Udq54")



def main():
    sp = login()  # sp (spotify) service
    user = sp.current_user()  # user

    playlists = sp.current_user_playlists()
    add(user, playlists, sp)


if __name__ == '__main__':
    main()
