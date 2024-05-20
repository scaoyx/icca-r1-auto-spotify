import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import pandas as pd


################################################################################ 
#
# Set environment variables to avoid "immortalizing your credentials in the source code"
#
#   1. Find your client ID, client secret on Spotify for developers
#   2. Open terminal (Linux/MacOS) or command line (Windows)
#   3. On Linux/MacOS, type
#       export SPOTIPY_CLIENT_ID='<fill in your client ID>'
#       export SPOTIPY_CLIENT_SECRET='<fill in your client secret>'
#       export SPOTIPY_REDIRECT_URI='<fill in your redirect URL>'
#      On Windows, type
#       setx SPOTIPY_CLIENT_ID '<fill in your client ID>'
#       setx SPOTIPY_CLIENT_SECRET '<fill in your client secret>'
#       setx SPOTIPY_REDIRECT_URI '<fill in your redirect URL>'
# 
# Or if you don't really care and just want less trouble:
import os
os.environ["SPOTIPY_CLIENT_ID"] = "8c8abb33d65d4a399a6fe5aa89a4f132"
os.environ["SPOTIPY_CLIENT_SECRET"] = "06c5b9d857e645fd9546c04a138cb971"
os.environ["SPOTIPY_REDIRECT_URI"] = "https://open.spotify.com/"
#
################################################################################

# export SPOTIPY_CLIENT_ID='b555cedc613a47eca6f50f5d6d2de81e'
# export SPOTIPY_CLIENT_SECRET='b615451877ad408f9bb80f8c6d2c3f04'
# export SPOTIPY_REDIRECT_URI='http://localhost:8080'


# To Modify
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSZCsgHwx1aOunn4QOXe9U1bjruNQmjv5P9Nfh-BzOIZp5UyppHahM7X4BFjScbrrt-XblauzWcrzYR/pub?gid=1263478570&single=true&output=csv"


# Spotify API setup
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

df = pd.read_csv(sheet_url)



# Catch songs not added to either df
# TODO

# get track id from url
# https://open.spotify.com/track/3pHkh7d0lzM2AldUtz2x37
# df['last_dash'] = df['Spotify Link'].str.rindex('/')
# tune this better
df['id'] = df['Spotify Link'].str[31:]
df['id'] = df['id'].str.split("?")
df['id'] = df['id'].str[0]

# deal with NaN
df['id'] = df['id'].fillna('').apply(str)


icca_df = df[df['Set?'] != 'R1']
r1_df = df[df['Set?'] == 'R1']


scope = "playlist-read-private", "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
user_id = sp.me()["id"]

# ICCA playlist
icca_playlist = sp.user_playlist_create(user=f"{user_id}", name="ICCALL", public=False,
                                      description="ICCA raw suggestions!")
icca_id_list = []
for song_id in icca_df['id']:
    icca_id_list.append(str(song_id))

try:
    for each_id in icca_id_list:
        if each_id:
            sp.playlist_add_items(icca_playlist['id'], [each_id], position=None)
except Exception as e:
    print(f"Error processing song {each_id} - {e}")


# R1 playlist
r1_playlist = sp.user_playlist_create(user=f"{user_id}", name="F25 R1 Raw", public=False,
                                      description="r1 raw suggestions!")
r1_id_list = []
for song_id in r1_df['id']:
    r1_id_list.append(str(song_id))

try:
    for each_id in r1_id_list:
        if each_id:
            sp.playlist_add_items(r1_playlist['id'], [each_id], position=None)
except Exception as e:
    print(f"Error processing song {each_id} - {e}")