import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image

def resize_image(image, max_width, max_height):
    """Resize image while maintaining aspect ratio."""
    img_ratio = image.width / image.height
    new_width, new_height = max_width, max_height

    if image.width > max_width or image.height > max_height:
        if img_ratio > 1:
            new_height = int(max_width / img_ratio)
        else:
            new_width = int(max_height * img_ratio)
    
    return image.resize((new_width, new_height), Image.LANCZOS)

def convert_to_pdf():
    if not images:
        messagebox.showwarning("No Images", "Please add images first!")
        return
    
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if not output_path:
        return

    # Ask for max width and height
    max_width = simpledialog.askinteger("Resize Images", "Enter Max Width (px)", minvalue=100, initialvalue=800)
    max_height = simpledialog.askinteger("Resize Images", "Enter Max Height (px)", minvalue=100, initialvalue=1200)

    image_objects = []
    for img_path in images:
        img = Image.open(img_path).convert("RGB")
        resized_img = resize_image(img, max_width, max_height)
        image_objects.append(resized_img)

    # Save as PDF
    image_objects[0].save(output_path, save_all=True, append_images=image_objects[1:])
    
    messagebox.showinfo("Success", f"PDF saved: {output_path}")

def add_images():
    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    for path in file_paths:
        if path not in images:
            images.append(path)
            listbox.insert(tk.END, os.path.basename(path))

def clear_list():
    images.clear()
    listbox.delete(0, tk.END)

def drop_files(event):
    files = root.tk.splitlist(event.data)
    for file in files:
        if file.lower().endswith((".jpg", ".png", ".jpeg")) and file not in images:
            images.append(file)
            listbox.insert(tk.END, os.path.basename(file))

# GUI Setup
root = TkinterDnD.Tk()
root.title("Image to PDF Converter")
root.geometry("400x450")

images = []

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Drag & Drop Images or Use 'Add Images'").pack()

listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", drop_files)

btn_add = tk.Button(root, text="Add Images", command=add_images)
btn_add.pack(pady=5)

btn_convert = tk.Button(root, text="Convert to PDF", command=convert_to_pdf)
btn_convert.pack(pady=5)

btn_clear = tk.Button(root, text="Clear List", command=clear_list)
btn_clear.pack(pady=5)

root.mainloop()
