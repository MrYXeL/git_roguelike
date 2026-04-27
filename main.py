import pygame
import random

from player import Player
from ennemi import Ennemi

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Etats du jeu
GAME = "game"
GAME_OVER = "game_over"
VICTORY = "victory"

game_state = GAME
current_room = 0
max_rooms = 3

# Groupes
all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
ennemis = pygame.sprite.Group()

# Joueur
player = Player(640, 360)

# Fonction génération de salle
def spawn_room(room_id):
    ennemis.empty()
    projectiles.empty()
    all_sprites.empty()

    all_sprites.add(player)

    player.position = pygame.math.Vector2(640, 360)
    player.rect.center = player.position

    nb_ennemis = 2 + room_id * 2

    for _ in range(nb_ennemis):
        x = random.randint(50, 1230)
        y = random.randint(50, 670)
        ennemi = Ennemi(x, y)
        ennemis.add(ennemi)
        all_sprites.add(ennemi)

spawn_room(current_room)

font = pygame.font.SysFont(None, 80)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if game_state == GAME:

        player.update(keys)
        projectiles.update()

        for ennemi in ennemis:
            ennemi.update(player)

        # Collision joueur / ennemi
        for ennemi in ennemis:
            if player.rect.colliderect(ennemi.rect):
                if player.invuln_frames == 0:
                    player.health -= 1
                    player.invuln_frames = player.invuln_duration

                    direction = player.position - ennemi.position
                    if direction.length() > 0:
                        direction = direction.normalize()
                        player.position += direction * 20
                        player.rect.center = player.position

                    if player.health < 0:
                        player.health = 0

        # Collision projectiles
        for projectile in projectiles:
            hit_list = pygame.sprite.spritecollide(projectile, ennemis, False)
            for ennemi in hit_list:
                if ennemi.invuln_frames == 0:
                    ennemi.health -= 1
                    ennemi.invuln_frames = ennemi.invuln_duration
                    projectile.kill()

                    if ennemi.health <= 0:
                        ennemi.kill()

        # Tir
        projectile = player.handle_shooting(keys)
        if projectile:
            all_sprites.add(projectile)
            projectiles.add(projectile)

        # Passage salle
        if len(ennemis) == 0:
            current_room += 1

            if current_room >= max_rooms:
                game_state = VICTORY
            else:
                spawn_room(current_room)

        # Game Over
        if player.health <= 0:
            game_state = GAME_OVER

    # Rendu
    screen.fill("black")
    all_sprites.draw(screen)

    # Barre de vie
    for i in range(player.max_health):
        color = (200, 50, 50) if i < player.health else (60, 60, 60)
        pygame.draw.rect(screen, color, (20 + i * 36, 20, 32, 24))
        pygame.draw.rect(screen, (255,255,255), (20 + i * 36, 20, 32, 24), 2)

    # Textes
    if game_state == GAME_OVER:
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (420, 300))

    elif game_state == VICTORY:
        text = font.render("VICTOIRE !", True, (0, 255, 0))
        screen.blit(text, (420, 300))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()