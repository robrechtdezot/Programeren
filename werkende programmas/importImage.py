import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk

def resize_image(image, width, height):
    """Resize image while maintaining aspect ratio."""
    img_ratio = image.width / image.height
    new_width, new_height = int(width), int(height)  # Convert to int

    if width == 0 and height > 0:  # Adjust width based on height
        new_width = int(height * img_ratio)
    elif height == 0 and width > 0:  # Adjust height based on width
        new_height = int(width / img_ratio)
    elif width == 0 and height == 0:
        return image  # No resizing

    return image.resize((new_width, new_height), Image.LANCZOS)

def resize_and_save():
    if not images:
        messagebox.showwarning("No Images", "Please add images first!")
        return
    
    output_folder = filedialog.askdirectory()
    if not output_folder:
        return

    width = int(width_slider.get())  # Convert float to int
    height = int(height_slider.get())  # Convert float to int

    for img_path in images:
        img = Image.open(img_path)
        resized_img = resize_image(img, width, height)

        # Save resized image
        filename = os.path.basename(img_path)
        save_path = os.path.join(output_folder, f"resized_{filename}")
        resized_img.save(save_path)

    messagebox.showinfo("Success", f"Images saved in: {output_folder}")

def add_images():
    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    for path in file_paths:
        if path not in images:
            images.append(path)
            listbox.insert(tk.END, os.path.basename(path))
            update_preview(path)

def clear_list():
    images.clear()
    listbox.delete(0, tk.END)
    preview_label.config(image="")

def drop_files(event):
    files = root.tk.splitlist(event.data)
    for file in files:
        if file.lower().endswith((".jpg", ".png", ".jpeg")) and file not in images:
            images.append(file)
            listbox.insert(tk.END, os.path.basename(file))
            update_preview(file)

def update_preview(image_path):
    """Update preview with the first selected image."""
    img = Image.open(image_path)
    img.thumbnail((200, 200))  # Resize preview to fit label
    img = ImageTk.PhotoImage(img)
    preview_label.config(image=img)
    preview_label.image = img

# GUI Setup
root = TkinterDnD.Tk()
root.title("Image Resizer")
root.geometry("500x500")

images = []

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Drag & Drop Images or Use 'Add Images'").pack()

listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", drop_files)

preview_label = tk.Label(root)
preview_label.pack(pady=10)

tk.Label(root, text="Width (px)").pack()
width_slider = ttk.Scale(root, from_=100, to=2000, orient="horizontal")
width_slider.set(800)  # Default value
width_slider.pack()

tk.Label(root, text="Height (px)").pack()
height_slider = ttk.Scale(root, from_=100, to=2000, orient="horizontal")
height_slider.set(600)  # Default value
height_slider.pack()

btn_add = tk.Button(root, text="Add Images", command=add_images)
btn_add.pack(pady=5)

btn_resize = tk.Button(root, text="Resize & Save", command=resize_and_save)
btn_resize.pack(pady=5)

btn_clear = tk.Button(root, text="Clear List", command=clear_list)
btn_clear.pack(pady=5)

root.mainloop()
