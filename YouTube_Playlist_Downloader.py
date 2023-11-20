import os
from pathlib import Path
from pytube import Playlist, YouTube
from tqdm import tqdm


# Function to create the folder if it doesn't exist
def create_download_folder():
    # Define the path to the desktop folder
    desktop_dir = Path.home() / "Desktop"
    # Create a subfolder called 'playlist_download'
    folder_path = desktop_dir / "playlist_download"

    # Check if the folder exists, and if not, create it
    if not folder_path.exists():
        folder_path.mkdir(parents=True)

    return folder_path


# Function to sanitize a string to make it a valid file name
def sanitize_filename(filename):
    # Define a set of characters to remove or replace
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")  # Replace with underscores

    return filename


if __name__ == "__main__":
    # Get the user's YouTube playlist URL for download
    print("Welcome to YouTube_playlist_downloader ")
    print("Make sure your playlist is public when downloading!\n")
    playlist_url = input("Enter the YouTube playlist URL to download: ")

    try:
        # Create the download folder
        folder_path = create_download_folder()
        playlist = Playlist(playlist_url)

        # Display the playlist title
        print(f"Playlist Title: {playlist.title}")

        # Iterate over each video in the playlist and download it
        for video in tqdm(playlist.videos, desc="Downloading", unit="video"):
            video_title = sanitize_filename(video.title)  # Sanitize the title

            # Get the highest resolution stream
            yd = video.streams.get_highest_resolution()
            # Define the file name using the sanitized title
            file_name = f"{video_title}.mp4"
            # Download the video to the folder with the specified file name
            yd.download(output_path=folder_path, filename=file_name)

        print(f"All videos downloaded successfully and saved in: {folder_path}\n")
        input("Press Enter to close the program.")

    except Exception as e:
        print(f"An error occurred: {e}")
