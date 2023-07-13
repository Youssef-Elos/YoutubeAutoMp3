import os
import shutil
import spotipy
import re
from spotipy.oauth2 import SpotifyClientCredentials

# Define the path to the folder containing the tracks
tracks_folder = r"C:\Users\bilga\Desktop\test_code\YoutubeAutoMp3\downloads"

# Define the path to the destination folder for genre folders
destination_folder = r"C:\Users\bilga\Desktop\test_code\YoutubeAutoMp3\playlists"

# Spotify API credentials
client_id = ""
client_secret = ""

    # Sorting options: 'genre', 'artist', 'album'
sorting_option = "genre"

# Reverse sorting flag
reverse_sorting = False

# Authenticate with Spotify API
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


# Function to sanitize folder name
def sanitize_folder_name(name):
    # Remove invalid characters using regular expression
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '', name)
    return sanitized_name.strip()


# Function to get the genre/artist/album for a given track name
def get_entity(track_name):
    results = sp.search(q=track_name, type='track', limit=1)
    if results['tracks']['items']:
        seed_track_id = results['tracks']['items'][0]['id']
        track_info = sp.track(seed_track_id)
        artist_id = track_info['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        if sorting_option == 'genre':
            genres = artist_info['genres']
            if genres:
                return genres[0]
        elif sorting_option == 'artist':
            return artist_info['name']
        elif sorting_option == 'album':
            return track_info['album']['name']
    return "Unknown"


# Create the genre/artist/album folders and move the tracks
def sort_tracks():
    for filename in os.listdir(tracks_folder):
        # Construct the full path to the file
        file_path = os.path.join(tracks_folder, filename)
        
        # Check if the file is a directory (to skip subdirectories)
        if os.path.isdir(file_path):
            continue
        
        # Extract the track name from the filename
        track_name = os.path.splitext(filename)[0]
        
        # Get the genre/artist/album for the track
        entity = get_entity(track_name)
        
        # Sanitize the folder name
        folder_name = sanitize_folder_name(entity)
        
        # Create a folder for the genre/artist/album if it doesn't already exist
        entity_folder = os.path.join(destination_folder, folder_name)
        if not os.path.exists(entity_folder):
            os.makedirs(entity_folder)
        
        # Move the file to the genre/artist/album folder
        destination_path = os.path.join(entity_folder, filename)
        shutil.move(file_path, destination_path)
    
    print("Tracks sorted successfully!")


# Reverse the sorting and move the tracks back to their previous folders
def reverse_sort_tracks():
    for root, dirs, files in os.walk(destination_folder):
        for file in files:
            # Construct the full path to the file
            file_path = os.path.join(root, file)
            
            # Move the file to the tracks folder
            destination_path = os.path.join(tracks_folder, file)
            shutil.move(file_path, destination_path)
    
    print("Tracks sorted reversed successfully!")


# Sort or reverse sort based on the selected option
if not reverse_sorting:
    sort_tracks()
else:
    reverse_sort_tracks()

# Delete the genre/artist/album folders after reverse sorting
if reverse_sorting:
    for root, dirs, files in os.walk(destination_folder, topdown=False):
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            os.rmdir(folder_path)

print("Sorting process completed!")