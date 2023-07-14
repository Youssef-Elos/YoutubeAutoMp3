# YoutubeAutoMp3
A Combination Of An Extension That Send Youtube Urls to A Flask-based web application for downloading Automaticlly MP3 tracks from YouTube.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
## Introduction

The YouTube MP3 Downloader is A Combination Of An Extension That Send Youtube Urls to web application built with Flask that allows users to download MP3 tracks from YouTube Automaticlly. It utilizes the YouTube MP3 download API to convert YouTube videos into MP3 audio files. Users can Also enter a YouTube video URL and initiate the download process. The downloaded tracks are stored in a designated "downloads" folder.

## Features
- Download MP3 tracks from YouTube Automaticlly when the video is played When using the Extension UrlSender.
- Download MP3 tracks from YouTube by providing the video URL.
- Store downloaded tracks in the "downloads" folder.
- Display a list of downloaded tracks on the home page.
- Sort and organize music tracks based on genre, artist, or album.
- Reverse the sorting and move the tracks back to the original folder.
- Play the tracks directly from the application.

## Installation

1. Clone the repository:

2. Navigate to the project directory:
   cd youtube-mp3-downloader

4. Activate the virtual environment:
   
   For Windows:  env\Scripts\activate

   For macOS/Linux: source env/bin/activate

5. Install the required dependencies:
   pip install -r requirements.txt

6. Install the UrlSender Extension in a chromium based browser

7. Usage

    Start the Flask server: python Download.py

   play a Track of your chosing in youtube and you will find the Mp3 in the downloads folder

   if you want to download the Track by pasting the link :
         Open a web browser and visit http://localhost:5000.

    Enter a valid YouTube video URL in the provided input field.

    Click the "Download" button to initiate the download process.

    Check the console for download progress and status messages.

    The downloaded tracks will be stored in the "downloads" folder.

8. Important Step !!!!
 !! Note That The Download Script And the Sort Script Are Using The YoutubeMP3 API and The Spotify API , You Have to Provide A Valid API KEY For both if you want the Scripts To work Properly !!
  ** Modify the following variables at the beginning of the script to customize the behavior: **

    tracks_folder: Define the path to the folder containing the tracks.
    destination_folder: Define the path to the destination folder for genre folders.
    sorting_option: Specify the sorting option: 'genre', 'artist', or 'album'.
    reverse_sorting: Set it to True to reverse the sorting and move the tracks back to their previous folders.
    client_id: Set it to your Spotify API client ID.
    client_secret: Set it to your Spotify API client secret.
    
    Obtain a Spotify API key:

    Visit the Spotify for Developers page and create a new application.
    Note down the client ID and client secret.

    Obtain a YoutubeMP3 API key:

    Visit the https://rapidapi.com/ page for the YoutubeMP3 and Create a new Key and Past it in "X-RapidAPI-Key" Variable.
    https://youtube-mp36.p.rapidapi.com/dl

## Author

The Youtube Music Track Downloader and Organizer is developed by [Youssef-Elos](https://github.com/Youssef-Elos).


Contributing

Contributions to the YouTube MP3 Downloader project are welcome. If you encounter any issues or have suggestions for improvements, please submit an issue on the GitHub repository. If you'd like to contribute code, feel free to open a pull request with your changes.

Please ensure that your contributions adhere to the existing code style and follow best practices. Include detailed information about the changes and any necessary documentation updates.
License

This project is licensed under the MIT License.
