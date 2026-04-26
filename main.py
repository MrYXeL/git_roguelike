#run with: py -3.12 main.py

import pygame
import math
from player import Player, Projectile

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GREEN = (50, 200, 50)
YELLOW = (255, 255, 0)

# Initialisation
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Groupes de sprites
all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Création du joueur
player = Player(640, 360)
all_sprites.add(player)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Touches
    keys = pygame.key.get_pressed()
    player.update(keys)
    projectiles.update()

    # Gestion tir avec flèches
    projectile = player.handle_shooting(keys)
    if projectile:
        all_sprites.add(projectile)
        projectiles.add(projectile)


    # Rendu
    screen.fill("black")
    all_sprites.draw(screen)

    # Affichage de la vie du joueur (barres rouges)
    for i in range(player.max_health):
        color = (200, 50, 50) if i < player.health else (60, 60, 60)
        pygame.draw.rect(screen, color, (20 + i * 36, 20, 32, 24))
        pygame.draw.rect(screen, (255,255,255), (20 + i * 36, 20, 32, 24), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
