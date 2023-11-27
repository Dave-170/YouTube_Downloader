# Import necessary modules
import os
import customtkinter as ctk
from pytube import YouTube, Playlist
from tkinter import filedialog, StringVar, ttk


# Define the main application class inheriting from customtkinter.CTk
class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        # Initialize the main application window
        super().__init__()

        # Set the title and default size for the application window
        self.title("YouTube Downloader")
        self.geometry("700x400")

        # Set the default color theme for customtkinter
        ctk.set_default_color_theme("green")

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Labels, entry widgets, and buttons for URL, download path, format selection, and download
        self.url_label = ctk.CTkLabel(self, text="YouTube URL:")
        self.url_entry = ctk.CTkEntry(self)
        self.path_label = ctk.CTkLabel(self, text="Download Path:")
        self.path_entry = ctk.CTkEntry(self, state="disabled")
        self.browse_button = ctk.CTkButton(
            self, text="Browse", command=self.browse_path
        )
        self.format_label = ctk.CTkLabel(self, text="Download Format:")
        self.format_var = StringVar(value="Video")
        self.format_video_radio = ctk.CTkRadioButton(
            self, text="Video", variable=self.format_var, value="Video"
        )
        self.format_audio_radio = ctk.CTkRadioButton(
            self, text="Audio Only", variable=self.format_var, value="Audio Only"
        )
        self.download_button = ctk.CTkButton(
            self, text="Download", command=self.download
        )

        # Textbox for displaying messages
        self.message_textbox = ctk.CTkTextbox(
            master=self, width=400, corner_radius=0, state="disabled", wrap="none"
        )
        self.message_textbox.grid(row=5, column=0, columnspan=3, sticky="nsew")

        # Labels and progress bar for download progress
        self.progress_label = ctk.CTkLabel(self, text="Download Progress:")
        self.progress_bar = ttk.Progressbar(self, mode="determinate")
        self.progress_bar["maximum"] = 100
        self.progress_bar["value"] = 0

        # Grid layout for arranging widgets
        self.url_label.grid(row=0, column=0, sticky="w", pady=(10, 0), padx=(10, 5))
        self.url_entry.grid(
            row=0, column=1, columnspan=2, pady=(10, 0), padx=(5, 10), sticky="we"
        )
        self.path_label.grid(row=1, column=0, sticky="w", pady=(10, 0), padx=(10, 5))
        self.path_entry.grid(row=1, column=1, pady=(10, 0), padx=(5, 10), sticky="we")
        self.browse_button.grid(
            row=1, column=2, pady=(10, 0), padx=(5, 10), sticky="we"
        )
        self.format_label.grid(row=2, column=0, sticky="w", pady=(10, 0), padx=(10, 5))
        self.format_video_radio.grid(
            row=2, column=1, pady=(10, 0), padx=(5, 10), sticky="we"
        )
        self.format_audio_radio.grid(
            row=2, column=2, pady=(10, 0), padx=(5, 10), sticky="we"
        )
        self.download_button.grid(
            row=3, column=0, columnspan=3, pady=(10, 0), padx=(10, 10), sticky="we"
        )
        self.progress_label.grid(
            row=4, column=0, sticky="w", pady=(10, 0), padx=(10, 5)
        )
        self.progress_bar.grid(
            row=4, column=1, columnspan=2, pady=(10, 0), padx=(5, 10), sticky="we"
        )

        # Configure column and row weights for resizing
        for i in range(3):
            self.columnconfigure(i, weight=1)
        for i in range(6):
            self.rowconfigure(i, weight=1)

    def browse_path(self):
        # Function to handle browsing and selecting download path
        download_path = filedialog.askdirectory()
        self.path_entry.configure(state="normal")
        self.path_entry.delete(0, ctk.END)
        self.path_entry.insert(0, download_path)
        self.path_entry.configure(state="disabled")

    def download(self):
        # Function to handle the download process
        url = self.url_entry.get()
        download_path = self.path_entry.get()
        download_format = self.format_var.get()

        try:
            if "playlist" in url.lower():
                playlist = Playlist(url)
                self.download_playlist(playlist, download_path, download_format)
            else:
                self.download_video(url, download_path, download_format)

        except Exception as e:
            self.display_message(f"Error: {str(e)}")
            self.progress_bar.stop()

    def download_playlist(self, playlist, download_path, download_format):
        # Function to handle downloading a playlist
        try:
            for video_url in playlist.video_urls:
                self.download_video(video_url, download_path, download_format)

            self.display_message(
                f"Download of playlist completed successfully. Saved at {download_path}"
            )

        except Exception as e:
            self.display_message(f"Error: {str(e)}")
            self.progress_bar.stop()

    def download_video(self, video_url, download_path, download_format):
        # Function to handle downloading a single video
        try:
            yt = YouTube(video_url, on_progress_callback=self.progress_callback)
            if download_format == "Video":
                stream = yt.streams.get_highest_resolution()
            else:
                stream = yt.streams.filter(only_audio=True).first()

            if stream:
                self.progress_bar["value"] = 0
                self.progress_bar.start()
                self.update_idletasks()

                stream.download(download_path)

                self.progress_bar.stop()
                self.progress_label.configure(text="Download Progress: Complete")

                self.display_message(
                    f"Download of video completed successfully. Saved at {download_path}"
                )

            else:
                self.display_message(
                    f"The specified URL does not have a suitable stream: {video_url}",
                    error=True,
                )

        except Exception as e:
            self.display_message(f"Error: {str(e)}")
            self.progress_bar.stop()

    def progress_callback(self, stream, chunk, remaining):
        # Callback function for updating the download progress
        try:
            file_size = stream.filesize
            downloaded = file_size - remaining
            percent = (downloaded / file_size) * 100
            self.progress_bar["value"] = percent
            self.update_idletasks()
        except Exception as e:
            self.display_message(f"Error: {str(e)}")
            self.progress_bar.stop()

    def display_message(self, message, error=False):
        # Function to display messages
        if error:
            self.message_textbox.configure(text_color="red")
        else:
            self.message_textbox.configure(text_color="black")
        self.message_textbox.configure(state="normal")
        self.message_textbox.insert("end", message + "\n")
        self.message_textbox.configure(state="disabled")


if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
