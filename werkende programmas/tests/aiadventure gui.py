import random
import nltk
import tkinter as tk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords



# Define the game world
rooms = {
    "forest": {"description": "You are in a dark forest. There is a path leading north.", "north": "cave"},
    "cave": {"description": "You are in a damp cave. You see something shiny on the ground.", "south": "forest"}
}

items = {"cave": "golden key"}
inventory = []
current_room = "forest"

def process_command(command):
    tokens = word_tokenize(command.lower())
    tokens = [word for word in tokens if word.isalnum() and word not in stopwords.words('english')]
    
    if "go" in tokens:
        for direction in ["north", "south", "east", "west"]:
            if direction in tokens and direction in rooms[current_room]:
                return move(direction)
        return "You can't go that way."
    
    elif "look" in tokens:
        return rooms[current_room]["description"]
    
    elif "take" in tokens or "pick" in tokens:
        return take_item()
    
    elif "inventory" in tokens:
        return f"You have: {', '.join(inventory) if inventory else 'nothing'}"
    
    return "I don't understand that command."

def move(direction):
    global current_room
    current_room = rooms[current_room][direction]
    return rooms[current_room]["description"]

def take_item():
    if current_room in items:
        inventory.append(items[current_room])
        del items[current_room]
        return "You picked up a golden key!"
    return "There's nothing to take here."

def send_command():
    command = entry.get()
    if command.lower() == "quit":
        root.destroy()
    else:
        response = process_command(command)
        text_area.insert(tk.END, "\n" + response)
    entry.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Text Adventure Game")
root.geometry("500x400")

text_area = tk.Text(root, height=15, width=50)
text_area.pack()
text_area.insert(tk.END, rooms[current_room]["description"])

entry = tk.Entry(root, width=50)
entry.pack()

button = tk.Button(root, text="Submit", command=send_command)
button.pack()

root.mainloop()
