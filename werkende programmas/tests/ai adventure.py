import pygame
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graphical Text Adventure")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)

# Fonts
font = pygame.font.Font(None, 36)

# Define the game world
rooms = {
    "forest": {"description": "You are in a dark forest. There is a path leading north.", "north": "cave", "hint": "Maybe there's something interesting in the cave?"},
    "cave": {"description": "You are in a damp cave. You see something shiny on the ground.", "south": "forest", "hint": "Try picking up the shiny object!"}
}

items = {"cave": "golden key"}
inventory = []
current_room = "forest"
input_text = ""
message = rooms[current_room]["description"]

def process_command(command):
    global message, current_room
    tokens = word_tokenize(command.lower())
    tokens = [word for word in tokens if word.isalnum() and word not in stopwords.words('english')]
    
    if "go" in tokens:
        for direction in ["north", "south", "east", "west"]:
            if direction in tokens and direction in rooms[current_room]:
                current_room = rooms[current_room][direction]
                message = rooms[current_room]["description"]
                return
        message = "You can't go that way."
    
    elif "look" in tokens:
        message = rooms[current_room]["description"]
    
    elif "take" in tokens or "pick" in tokens:
        if current_room in items:
            inventory.append(items[current_room])
            del items[current_room]
            message = "You picked up a golden key!"
        else:
            message = "There's nothing to take here."
    
    elif "inventory" in tokens:
        message = f"You have: {', '.join(inventory) if inventory else 'nothing'}"
    
    elif "hint" in tokens:
        message = rooms[current_room].get("hint", "No hints available here.")
    
    else:
        message = "I don't understand that command."

def draw_screen():
    screen.fill(WHITE)
    
    # Display message
    text_surface = font.render(message, True, BLACK)
    screen.blit(text_surface, (20, 20))
    
    # Display input box
    pygame.draw.rect(screen, BLUE, (20, HEIGHT - 50, 760, 30))
    input_surface = font.render(input_text, True, WHITE)
    screen.blit(input_surface, (30, HEIGHT - 45))
    
    pygame.display.flip()

running = True
while running:
    draw_screen()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                process_command(input_text)
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

pygame.quit()
