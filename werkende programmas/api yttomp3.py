import os
import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp
from googleapiclient.discovery import build

# 🔹 Replace with your YouTube API key
YOUTUBE_API_KEY = "AIzaSyA6y-1vxAwx9F9TCTxbngfE0QXxtc5WcbI"

def search_youtube(query):
    """Search YouTube and return the first video URL."""
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(q=query, part="snippet", maxResults=1, type="video")
    response = request.execute()
    video_id = response["items"][0]["id"]["videoId"]
    return f"https://www.youtube.com/watch?v={video_id}"

def download_audio():
    """Download YouTube audio using yt-dlp."""
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Error", "Please enter a YouTube URL or search term!")
        return
    
    # If input is a search term, find the first video
    if "youtube.com" not in url and "youtu.be" not in url:
        url = search_youtube(url)
    
    save_path = filedialog.askdirectory()
    if not save_path:
        return
    
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    
    try:
        status_label.config(text="Downloading...", fg="blue")
        root.update_idletasks()
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        status_label.config(text="Download Complete!", fg="green")
        messagebox.showinfo("Success", "MP3 Downloaded Successfully!")
    except Exception as e:
        status_label.config(text="Error!", fg="red")
        messagebox.showerror("Error", str(e))

# 🔹 GUI Setup
root = tk.Tk()
root.title("YouTube to MP3 Converter")
root.geometry("400x250")

tk.Label(root, text="Enter YouTube URL or Search:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

btn_download = tk.Button(root, text="Download MP3", command=download_audio)
btn_download.pack(pady=10)

status_label = tk.Label(root, text="", fg="black")
status_label.pack(pady=5)

root.mainloop()