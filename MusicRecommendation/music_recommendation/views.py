# music_recommendation/views.py
from django.shortcuts import render
import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = ""
CLIENT_SECRET = ""

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load similarity matrix and dataframe
def load_similarity_matrix():
    with open('music_recommendation/similarity.pkl', 'rb') as file:
        return pickle.load(file)

def load_dataframe():
    with open('music_recommendation/df.pkl', 'rb') as file:
        return pickle.load(file)

similarity_matrix = load_similarity_matrix()
df = load_dataframe()

def get_recommendations(song):
    # Ensure df is available
    if 'df' not in globals():
        global df
        df = load_dataframe()

    idx = df[df['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity_matrix[idx])), reverse=True, key=lambda x: x[1])

    songs = []
    for m_id in distances[1:11]:  # 10 best recommendations
        songs.append(df.iloc[m_id[0]].song)

    return songs

def recommend_songs(request):
    music_list = df['song'].values

    if request.method == 'POST':
        selected_song = request.POST.get('selected_song')
        recommendations = get_recommendations(selected_song)
        posters = [get_song_album_cover_url(song) for song in recommendations]
        artists = [get_artist(song) for song in recommendations]
        context = {'selected_song': selected_song, 'recommendations': zip(recommendations, artists, posters), 'music_list': music_list}
        return render(request, 'recommendations.html', context)

    return render(request, 'select_song.html', {'music_list': music_list})

def get_song_album_cover_url(song_name):
    search_query = f"track:{song_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def get_artist(song_name):
    search_query = f"track:{song_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        artist_name = results["tracks"]["items"][0]["artists"][0]["name"]
        return artist_name
    else:
        return "Unknown Artist"

def index(request):
    return render(request, 'index.html')
