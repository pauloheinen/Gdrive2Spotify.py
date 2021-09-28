import spotipy
from spotipy.oauth2 import *

client_id = '8ad707a87c8445b481c240424ad5998c'
client_secret = 'd00fda6a444f41cbb4e3bd5528fd8475'
redirect_uri = 'http://localhost:8888/callback'


class Spotify:

    def __init__(self, splogin):
        self.__user = splogin.current_user()
        self.playlist = splogin.current_user_playlists()

    def add(self, item, opcao):
        tracks = ['{}'.format(item)]
        try:
            splogin.playlist_add_items(opcao, tracks, None)
        except:
            print("I couldnt find: " + tracks[0])
            pass

    def playlists(self):
        print("Add into which playlist? ")
        for i, item in enumerate(self.playlist['items']):
            print(str(i + 1), item['name'])

        opcao = int(input("Opção: "))
        opcao = self.playlist['items'][opcao - 1]['id']
        return opcao


# login into spotify profile
def login():
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                        client_secret=client_secret,
                                                        redirect_uri=redirect_uri,
                                                        scope="user-library-read playlist-modify-private playlist-modify-public"
                                                        ))
    print("Logged")
    return spotify

splogin = login()  # take spotify's api methods
sp = Spotify(splogin)  # take my own build class methods
