import pygame
from sys import exit

pygame.init() #basis
screen = pygame.display.set_mode((800, 600)) #screen size
pygame.display.set_caption('First Game') #title
icon = pygame.image.load('sample.png') #icon
icon = pygame.transform.scale(icon, (800, 600)) #icon
screen.blit(icon, (0, 0)) #achtergrond
clock = pygame.time.Clock() #fps
            
test_surface = pygame.Surface((100, 100)) #surface
test_surface.fill((255, 0, 0)) #color
screen.blit(test_surface, (100, 100)) #position

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    #draw elements
    #update screen
    pygame.display.update() #update screen
    clock.tick(60) #fps 60