from flask import Flask, render_template, request
import os
import shutil
import spotipy
import re
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# Spotify API credentials
client_id = "38ad11381339443a98fc7aec061db864"
client_secret = "d367a3107db3469797a2a28f27917f33"


    # Authenticate with Spotify API
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


# Function to sanitize folder name
def sanitize_folder_name(name):
    # Remove invalid characters using regular expression
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '', name)
    return sanitized_name.strip()


# Function to get the artist/album for a given track name
def get_entity(track_name):
    results = sp.search(q=track_name, type='track', limit=1)
    if results['tracks']['items']:
        seed_track_id = results['tracks']['items'][0]['id']
        track_info = sp.track(seed_track_id)
        artist_name = track_info['artists'][0]['name']
        album_name = track_info['album']['name']
        return artist_name, album_name
    return "Unknown", "Unknown"


# Sort the tracks by genre/artist/album and move them to the destination folders
def sort_tracks(sorting_option, tracks_folder, destination_folder):
    for filename in os.listdir(tracks_folder):
        # Construct the full path to the file
        file_path = os.path.join(tracks_folder, filename)

        # Check if the file is a directory (to skip subdirectories)
        if os.path.isdir(file_path):
            continue

        # Extract the track name from the filename
        track_name = os.path.splitext(filename)[0]

        if sorting_option == 'genre':
            # Get the genre for the track
            entity = get_entity(track_name)[0]
        elif sorting_option == 'artist':
            # Get the artist for the track
            entity = get_entity(track_name)[0]
        elif sorting_option == 'album':
            # Get the album for the track
            entity = get_entity(track_name)[1]
        else:
            # Default to sorting by genre
            entity = get_entity(track_name)[0]

        # Sanitize the folder name
        folder_name = sanitize_folder_name(entity)

        # Create a folder for the genre/artist/album if it doesn't already exist
        entity_folder = os.path.join(destination_folder, folder_name)
        if not os.path.exists(entity_folder):
            os.makedirs(entity_folder)

        # Move the file to the genre/artist/album folder
        destination_path = os.path.join(entity_folder, filename)
        shutil.move(file_path, destination_path)


# Reverse the sorting and move the tracks back to the tracks folder
def reverse_sort_tracks(destination_folder, tracks_folder):
    for root, dirs, files in os.walk(destination_folder):
        for file in files:
            # Construct the full path to the file
            file_path = os.path.join(root, file)

            # Move the file to the tracks folder
            destination_path = os.path.join(tracks_folder, file)
            shutil.move(file_path, destination_path)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sorting_option = request.form.get('sorting_option')
        tracks_folder = r"C:\Users\bilga\Desktop\test_code\YoutubeAutoMp3\downloads"
        destination_folder = r"C:\Users\bilga\Desktop\test_code\YoutubeAutoMp3\playlists"

        if sorting_option == 'reverse':
            reverse_sort_tracks(destination_folder, tracks_folder)
            # Delete the genre/artist/album folders after reverse sorting
            for root, dirs, files in os.walk(destination_folder, topdown=False):
                for dir in dirs:
                    folder_path = os.path.join(root, dir)
                    os.rmdir(folder_path)
            return "Tracks sorted reversed successfully!"
        else:
            sort_tracks(sorting_option, tracks_folder, destination_folder)
            return "Tracks sorted successfully!"

    tracks_folder = r"C:\Users\bilga\Desktop\test_code\YoutubeAutoMp3\downloads"
    destination_folder = r"C:\Users\bilga\Desktop\test_code\YoutubeAutoMp3\playlists"

    tracks = []

    for root, dirs, files in os.walk(tracks_folder):
        folder_name = os.path.basename(root)
        folder_tracks = [file for file in files if not file.startswith('.')]
        folder_tracks = [os.path.splitext(file)[0] for file in folder_tracks]
        destination_path = os.path.join(destination_folder, folder_name)
        tracks.append((folder_name, folder_tracks, destination_path))

    return render_template('index.html', tracks=tracks)


@app.route('/play/<path:file_path>')
def play_file(file_path):
    tracks_folder = r"C:\Users\bilga\Desktop\test_code\YoutubeAutoMp3\playlists"
    file_path = os.path.join(tracks_folder, file_path)
    tracks = []

    for root, dirs, files in os.walk(tracks_folder):
        folder_name = os.path.basename(root)
        folder_tracks = [file for file in files if not file.startswith('.')]
        folder_tracks = [os.path.splitext(file)[0] for file in folder_tracks]
        destination_path = os.path.join(root, folder_name)
        tracks.append((folder_name, folder_tracks, destination_path))

    return render_template('index.html', tracks=tracks, current_track=file_path)


if __name__ == '__main__':
    app.run()