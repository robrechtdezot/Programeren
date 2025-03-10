import tkinter as tk
from tkinter import messagebox
import random
import string
import json
import os
import pyperclip
from cryptography.fernet import Fernet

# Function to load the encryption key from a file
def load_key():
    if os.path.exists("key.key"):
        with open("key.key", "rb") as key_file:
            return key_file.read()
    else:
        # If the key file doesn't exist, generate and save a new key
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        return key

# Initialize Fernet cipher with the loaded key
key = load_key()
cipher = Fernet(key)

# Encrypt the password
def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

# Decrypt the password
def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

# Password Generator Function
def generate_password():
    length = int(length_entry.get())
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# Save Password Function
def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    
    if not website or not username or not password:
        messagebox.showwarning("Warning", "Please fill all fields")
        return
    
    encrypted_password = encrypt_password(password)  # Encrypt password
    
    new_data = {website: {"username": username, "password": encrypted_password}}
    
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    
    data.update(new_data)
    
    with open("passwords.json", "w") as file:
        json.dump(data, file, indent=4)
    
    messagebox.showinfo("Success", "Password Saved Successfully")
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# Retrieve Password Function
def retrieve_password():
    website = website_entry.get()
    
    if not website:
        messagebox.showwarning("Warning", "Please enter a website")
        return
    
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            data = json.load(file)
            
        if website in data:
            username = data[website]["username"]
            encrypted_password = data[website]["password"]
            password = decrypt_password(encrypted_password)  # Decrypt password
            messagebox.showinfo("Password", f"Username: {username}\nPassword: {password}")
            pyperclip.copy(password)  # Copy password to clipboard
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Not Found", "Website not found in saved passwords")
    else:
        messagebox.showwarning("Not Found", "No saved passwords available")

# Toggle Password Visibility Function
def toggle_password_visibility():
    current = password_entry.cget('show')
    if current == '*':
        password_entry.config(show='')
    else:
        password_entry.config(show='*')

# GUI Setup
root = tk.Tk()
root.title("Password Manager")
root.geometry("400x400")

tk.Label(root, text="Website:").pack(pady=5)
website_entry = tk.Entry(root, width=40)
website_entry.pack()

tk.Label(root, text="Username:").pack(pady=5)
username_entry = tk.Entry(root, width=40)
username_entry.pack()

tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, width=40, show='*')
password_entry.pack()

tk.Label(root, text="Password Length:").pack(pady=5)
length_entry = tk.Entry(root, width=10)
length_entry.insert(0, "12")
length_entry.pack()

generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.pack(pady=5)

save_button = tk.Button(root, text="Save Password", command=save_password)
save_button.pack(pady=5)

retrieve_button = tk.Button(root, text="Retrieve Password", command=retrieve_password)
retrieve_button.pack(pady=5)

toggle_button = tk.Button(root, text="Show/Hide Password", command=toggle_password_visibility)
toggle_button.pack(pady=5)

root.mainloop()
