import pygame
import math

RED = (200, 50, 50)
GREEN = (50, 200, 50)

class Ennemi(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.base_image = pygame.Surface((32, 32))
        self.base_image.fill(GREEN)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
        self.health = 3
        self.position = pygame.math.Vector2(x, y)
        # Invulnérabilité et clignotement
        self.invuln_frames = 0
        self.invuln_duration = 15

    def update(self, player):
        # Déplacement simple vers le joueur
        direction = pygame.math.Vector2(player.rect.center) - self.position
        if direction.length() > 0:
            direction = direction.normalize()
            self.position += direction * self.speed
            self.rect.center = self.position

        # Invulnérabilité
        if self.invuln_frames > 0:
            self.invuln_frames -= 1
            # Clignotement
            if (self.invuln_frames // 3) % 2 == 0:
                self.image.set_alpha(60)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)
