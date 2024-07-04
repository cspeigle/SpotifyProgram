import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials


# Authentication scope
scope = 'playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public'

# Authentication and authorization
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))
DumpList = 'SpotipySecondary'
playlist_name = 'SpotipyPrimary'
song_names = ["Brazil", "Hello","Goodbye","Greetings"]
song_name = "Hello"
#input("Enter song name")


       

#Function Definitions
def display_playlist_tracks(playlist_name):
    user_id = sp.me()['id']  # Get the current user's ID
    playlists = sp.user_playlists(user_id)
    
    # Search for the playlist named 'SpotipyPrimary' and get its ID
    playlist_id = None
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            break
    if playlist_id is None:
        print(f"Playlist '{playlist_name}' not found.")
        return
    
    tracks = sp.playlist_tracks(playlist_id)

    print(f"Tracks in playlist '{playlist_name}':")
    for idx, item in enumerate(tracks['items']):
        track = item['track']
        print(f"{idx+1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")

# Example usage:
playlist_name = 'SpotipyPrimary'
display_playlist_tracks(playlist_name)


def create_playlist_if_not_exists(playlist_name):
    user_id = sp.me()['id']  # Get the current user's ID
    playlists = sp.user_playlists(user_id)

    #Print names and ids of all existing playlists and add the names to a list
    for playlist in playlists['items']:
        print("Playlist Name: ",playlist['name'])
        print("Playlist ID: ", playlist['id'])
        if playlist['name'] == playlist_name:
            print("Playlist Exists")
            return playlist['id']
    # If the playlist doesn't exist, create it 
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    print('Playlist Created')
    return playlist['id']
                
            


# Function to search for a song and return its track ID
def get_track_id(song_name):
    trackids = []
    # Perform a search query
    results = sp.search(q=song_name, type='track', limit=1)
    if song_name == 'NoSong':
        return None
    # Extract the track ID from the search results
    if results['tracks']['items']:
        track_info = results['tracks']['items'][0]
        track_id = track_info['id']
        artist_names = ', '.join([artist['name'] for artist in track_info['artists']])                        
        print(f"Track ID for '{song_name}' by {artist_names}': {track_id}")
        trackids.append(track_id)
        return track_id
    else:
        print(f"No track found for '{song_name}'")
        return None


def add_songs_to_playlist(playlist_id, song_names):
    existing_tracks = set(item['track']['id'] for item in sp.playlist_items(playlist_id)['items'])
    for song_name in song_names:
        track_id = get_track_id(song_name)
        if track_id:
            if track_id in existing_tracks:
                print(f"Skipping adding '{song_name}' to the playlist because it's already present.")
            else:
                sp.playlist_add_items(playlist_id=playlist_id, items=[track_id])
        else:
            print(f"Skipping adding '{song_name}' to the playlist because no track ID was found.")








def SongTransferPrimaryToSecondary(PrimaryPlaylist_id, SecondaryPlaylist_id, song_name):
    # Get the IDs of the primary and secondary playlists 
    if PrimaryPlaylist_id is None or SecondaryPlaylist_id is None:
        print("One or both playlists not found.")
        return

    # Get the track ID of the song
    track_id = get_track_id(song_name)
    if track_id is None:
        print(f"No track found for '{song_name}'. Transfer aborted.")
        return

    # Check if the song is already in the secondary playlist
    secondary_playlist_tracks = set(item['track']['id'] for item in sp.playlist_items(SecondaryPlaylist_id)['items'])
    if track_id in secondary_playlist_tracks:
        print(f"Skipping adding '{song_name}' to '{SecondaryPlaylist_id}' because it's already present.")
        sp.playlist_remove_all_occurrences_of_items(playlist_id=PrimaryPlaylist_id, items=[track_id])
        return

    # Add the song to the secondary playlist
    sp.playlist_add_items(playlist_id=SecondaryPlaylist_id, items=[track_id])

    print(f"Song '{song_name}' transferred from '{PrimaryPlaylist_id}' to '{SecondaryPlaylist_id}'.")



#Function Calls 
PrimaryPlaylist_id = create_playlist_if_not_exists(playlist_name)
print (PrimaryPlaylist_id)
track_id = get_track_id(song_names)
print (track_id)


SecondaryPlaylist_id = create_playlist_if_not_exists(DumpList)
print (SecondaryPlaylist_id)

# Add the track to the playlist 
add_songs_to_playlist(PrimaryPlaylist_id, song_names)

//SongTransferPrimaryToSecondary(PrimaryPlaylist_id, SecondaryPlaylist_id, song_name)
