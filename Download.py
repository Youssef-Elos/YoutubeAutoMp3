import os
import re
from flask_cors import CORS
from flask import Flask, request, render_template
import requests
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    # Get the list of tracks in the "downloads" folder
    tracks = []
    if os.path.exists("downloads"):
        tracks = os.listdir("downloads")
    return render_template("index.html", tracks=tracks)

@app.route("/download", methods=["POST"])
def download_track():
    try:
        url = request.form.get("url")
        print(f"Downloading track from {url}")

        # Check if the track is already downloaded
        if not os.path.exists("downloads"):
            os.mkdir("downloads")

        # Extract the video ID from the URL
        parsed_url = urlparse(url)
        video_id = parse_qs(parsed_url.query).get("v")
        if not video_id:
            return "Invalid YouTube URL. Please provide a valid URL."

        video_id = video_id[0]

        # Send request to YouTube MP3 download API
        api_url = "https://youtube-mp36.p.rapidapi.com/dl"
        querystring = {"id": video_id}
        headers = {
            "X-RapidAPI-Key": "",
            "X-RapidAPI-Host": "youtube-mp36.p.rapidapi.com"
        }
        response = requests.get(api_url, headers=headers, params=querystring)

        # Print the API response
        # print(f"API response: {response.text}")

        # Check if the request was successful
        if response.status_code != 200:
            return "Failed to download the track. Please try again."

        json_data = response.json()

        if json_data.get("status") != "ok":
            return "Failed to download the track. Please try again."

        download_link = json_data.get("link")
        track_title = json_data.get("title")

        if not download_link or not track_title:
            return "Failed to download the track. Please try again."

        # Save the downloaded track
        track_name = f"{track_title}.mp3"
        track_name = re.sub(r'[\\/:*?"<>|]', '', track_name)  # Remove invalid characters
        destination_path = os.path.join("downloads", track_name)

        if os.path.exists(destination_path):
            return "Track already downloaded."

        print(f"Downloading track from {download_link}")
        track_response = requests.get(download_link)
        if track_response.status_code == 200:
            with open(destination_path, "wb") as file:
                file.write(track_response.content)
            print(f"Track downloaded to {destination_path}")
            return "Track downloaded."

        return "Failed to download the track. Please try again."

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return "Failed to download the track. Please check the console for more details."

if __name__ == "__main__":
    app.run()
