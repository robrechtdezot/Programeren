import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('First Game')
sky = pygame.image.load('graphics/sky.png').convert()
sky = pygame.transform.scale(sky, (800, 600))
ground = pygame.image.load('graphics/Battleground1.png').convert()
ground = pygame.transform.scale(ground, (1000, 600))
test_font = pygame.font.Font("font/BreatheFireIii-PKLOB.ttf", 50)
clock = pygame.time.Clock()

test_surface = pygame.Surface((100, 100))
test_ground = ground.get_rect()
test_ground.topleft = (0, 400)
test_text = test_font.render('My game', True, (255, 140, 0, 255))

character_surface = pygame.image.load('graphics/3/3_enemies_1_attack_000.png').convert_alpha()
character_surface = pygame.transform.scale(character_surface, (200, 200))
character_rectangle = character_surface.get_rect(midbottom=(0, 400))

player_surf = pygame.image.load('graphics/5/5_enemies_1_attack_000.png').convert_alpha()
player_surf = pygame.transform.scale(player_surf, (200, 200))
player_surf = pygame.transform.flip(player_surf, True, False)
player_surf_rectangle = player_surf.get_rect(midbottom=(800, 400))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEMOTION:
            print(event.pos)

    screen.blit(sky, (0, 0))
    screen.blit(ground, (0, 50))
    screen.blit(test_text, (300, 20))

    character_rectangle.x += 2
    if character_rectangle.right > 800:
        character_rectangle.left = 0
    screen.blit(character_surface, (character_rectangle))

    player_surf_rectangle.x -= 2
    if player_surf_rectangle.left < 0:
        player_surf_rectangle.right = 800
    screen.blit(player_surf, (player_surf_rectangle))

    if character_rectangle.colliderect(player_surf_rectangle):
        character_rectangle.x = 0
        player_surf_rectangle.x = 800

    if player_surf_rectangle.collidepoint(pygame.mouse.get_pos()):
        player_surf_rectangle.x = 0
        print("collision")
        print(pygame.mouse.get_pressed())

    pygame.display.update()
    clock.tick(60)