import tkinter as tk
from tkinter import messagebox
import random
import string
import json
import os

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
    
    new_data = {website: {"username": username, "password": password}}
    
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

# GUI Setup
root = tk.Tk()
root.title("Password Manager")
root.geometry("400x300")

tk.Label(root, text="Website:").pack(pady=5)
website_entry = tk.Entry(root, width=40)
website_entry.pack()

tk.Label(root, text="Username:").pack(pady=5)
username_entry = tk.Entry(root, width=40)
username_entry.pack()

tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, width=40)
password_entry.pack()

tk.Label(root, text="Password Length:").pack(pady=5)
length_entry = tk.Entry(root, width=10)
length_entry.insert(0, "12")
length_entry.pack()

generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.pack(pady=5)

save_button = tk.Button(root, text="Save Password", command=save_password)
save_button.pack(pady=5)

root.mainloop()
