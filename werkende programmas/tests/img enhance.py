import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageEnhance, ImageTk

def enhance_image(image, sharpness, contrast, brightness, color):
    """Enhance image using given parameters."""
    image = ImageEnhance.Sharpness(image).enhance(sharpness)
    image = ImageEnhance.Contrast(image).enhance(contrast)
    image = ImageEnhance.Brightness(image).enhance(brightness)
    image = ImageEnhance.Color(image).enhance(color)
    return image

def upscale_image(image):
    """Use OpenCV to upscale image (Super Resolution)."""
    img = np.array(image)
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel("EDSR_x4.pb")  # Download OpenCV EDSR model
    sr.setModel("edsr", 4)  # Use 4x Super Resolution
    result = sr.upsample(img)
    return Image.fromarray(result)

def apply_enhancements():
    """Apply enhancements and update preview."""
    if not image_path:
        return
    img = Image.open(image_path)
    enhanced = enhance_image(
        img, sharpness_slider.get(), contrast_slider.get(), 
        brightness_slider.get(), color_slider.get()
    )
    preview_image(enhanced)

def save_image():
    """Save enhanced image."""
    if not image_path:
        messagebox.showwarning("No Image", "Please add an image first!")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
    if save_path:
        img = Image.open(image_path)
        enhanced = enhance_image(
            img, sharpness_slider.get(), contrast_slider.get(), 
            brightness_slider.get(), color_slider.get()
        )
        enhanced.save(save_path)
        messagebox.showinfo("Success", f"Image saved: {save_path}")

def add_image():
    """Open file dialog to select an image."""
    global image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if file_path:
        image_path = file_path
        preview_image(Image.open(image_path))

def drop_image(event):
    """Handle image drag & drop."""
    global image_path
    file = root.tk.splitlist(event.data)[0]
    if file.lower().endswith((".jpg", ".png", ".jpeg")):
        image_path = file
        preview_image(Image.open(image_path))

def preview_image(img):
    """Update preview with the enhanced image."""
    img.thumbnail((300, 300))  # Resize for preview
    img = ImageTk.PhotoImage(img)
    preview_label.config(image=img)
    preview_label.image = img

# GUI Setup
root = TkinterDnD.Tk()
root.title("Image Enhancer")
root.geometry("500x600")

image_path = None

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Drag & Drop Image or Click 'Add Image'").pack()

preview_label = tk.Label(root)
preview_label.pack(pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", drop_image)

tk.Label(root, text="Sharpness").pack()
sharpness_slider = ttk.Scale(root, from_=0.5, to=3.0, orient="horizontal")
sharpness_slider.set(1.0)
sharpness_slider.pack()

tk.Label(root, text="Contrast").pack()
contrast_slider = ttk.Scale(root, from_=0.5, to=3.0, orient="horizontal")
contrast_slider.set(1.0)
contrast_slider.pack()

tk.Label(root, text="Brightness").pack()
brightness_slider = ttk.Scale(root, from_=0.5, to=3.0, orient="horizontal")
brightness_slider.set(1.0)
brightness_slider.pack()

tk.Label(root, text="Color").pack()
color_slider = ttk.Scale(root, from_=0.5, to=3.0, orient="horizontal")
color_slider.set(1.0)
color_slider.pack()

btn_add = tk.Button(root, text="Add Image", command=add_image)
btn_add.pack(pady=5)

btn_apply = tk.Button(root, text="Apply Enhancements", command=apply_enhancements)
btn_apply.pack(pady=5)

btn_save = tk.Button(root, text="Save Enhanced Image", command=save_image)
btn_save.pack(pady=5)

root.mainloop()
