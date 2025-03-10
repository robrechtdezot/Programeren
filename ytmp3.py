import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube
from pydub import AudioSegment

def download_audio():
    """Download YouTube video and convert to MP3."""
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Error", "Please enter a YouTube URL!")
        return

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()

        # Ask user where to save
        save_path = filedialog.askdirectory()
        if not save_path:
            return

        # Download audio
        status_label.config(text="Downloading...", fg="blue")
        root.update_idletasks()
        file_path = stream.download(output_path=save_path, filename="temp_audio.mp4")

        # Convert to MP3
        status_label.config(text="Converting to MP3...", fg="blue")
        root.update_idletasks()
        audio = AudioSegment.from_file(file_path)
        mp3_path = os.path.join(save_path, yt.title + ".mp3")
        audio.export(mp3_path, format="mp3")

        # Clean up temp file
        os.remove(file_path)

        status_label.config(text=f"Saved: {mp3_path}", fg="green")
        messagebox.showinfo("Success", f"MP3 Saved: {mp3_path}")

    except Exception as e:
        status_label.config(text="Error: Check URL!", fg="red")
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("YouTube to MP3 Converter")
root.geometry("400x200")

tk.Label(root, text="Enter YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

btn_download = tk.Button(root, text="Download MP3", command=download_audio)
btn_download.pack(pady=10)

status_label = tk.Label(root, text="", fg="black")
status_label.pack(pady=5)

root.mainloop()
