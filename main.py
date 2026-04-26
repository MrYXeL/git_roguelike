#run with: py -3.12 main.py

import pygame
import math

from player import Player, Projectile
from ennemi import Ennemi

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
ennemis = pygame.sprite.Group()


# Création du joueur
player = Player(640, 360)
all_sprites.add(player)

# Création d'un ennemi
ennemi = Ennemi(200, 200)
all_sprites.add(ennemi)
ennemis.add(ennemi)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Touches
    keys = pygame.key.get_pressed()

    player.update(keys)
    projectiles.update()
    for ennemi in ennemis:
        ennemi.update(player)

    # Dégâts de contact joueur <-> ennemi avec invulnérabilité
    for ennemi in ennemis:
        if player.rect.colliderect(ennemi.rect):
            if player.invuln_frames == 0:
                player.health -= 1
                player.invuln_frames = player.invuln_duration
                # Repousser le joueur pour éviter perte de vie instantanée
                direction = player.position - ennemi.position
                if direction.length() > 0:
                    direction = direction.normalize()
                    player.position += direction * 20
                    player.rect.center = player.position
                # Empêcher la vie de descendre sous 0
                if player.health < 0:
                    player.health = 0

    # Collision projectile <-> ennemi
    for projectile in projectiles:
        hit_list = pygame.sprite.spritecollide(projectile, ennemis, False)
        for ennemi in hit_list:
            if ennemi.invuln_frames == 0:
                ennemi.health -= 1
                ennemi.invuln_frames = ennemi.invuln_duration
                projectile.kill()
                if ennemi.health <= 0:
                    ennemi.kill()

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
