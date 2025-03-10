name = input("What is your name? ")
print("Hello, " + name + ". It's time to play a game.")
print("You are in a dark, cold room.")
print("There are three doors in front of you.")
print("Which door do you want to open? (1, 2, or 3)")   
door = input()  
if door == "1":
    print("You open the door and see a treasure chest.")
    print("Do you want to open the chest? (yes or no)")
    chest = input()
    if chest == "yes":
        print("You open the chest and find a key.")
        print("You take the key and leave the room.")
        print("You find yourself in a hallway with three doors.")
        print("Which door do you want to open? (1, 2, or 3)")
        door = input()
        if door == "1":
            print("You open the door and see a dragon.")
            print("The dragon breathes fire and you are burned to a crisp.")
            print("Game over.")
        elif door == "2":
            print("You open the door and see a staircase.")
            print("You climb the staircase and find yourself in a garden.")
            print("You see a path leading to a castle.")
            print("Do you want to follow the path? (yes or no)")
            path = input()
            if path == "yes":
                print("You follow the path and reach the castle.")
                print("You use the key to unlock the castle door.")
                print("You enter the castle and find the princess.")
                print("Congratulations! You have rescued the princess.")
                print("You win!")
            elif path == "no":
                print("You decide not to follow the path.")
                print("You turn back and find yourself in the hallway.")
                print("You see three doors in front of you.")   


