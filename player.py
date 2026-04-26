import pygame
import math

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GREEN = (50, 200, 50)
YELLOW = (255, 255, 0)

# Classe Projectile (nécessaire pour le tir du joueur)
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.speed = 8
        
    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        
        # Supprimer si hors écran
        if (self.rect.right < 0 or self.rect.left > 1280 or
            self.rect.bottom < 0 or self.rect.top > 720):
            self.kill()

# Classe Joueur
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.base_image = pygame.Surface((32, 32))
        self.base_image.fill(RED)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Stats
        self.speed = 4
        self.health = 6
        self.max_health = 6
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)

        # Tir
        self.shoot_cooldown = 0
        self.shoot_delay = 15  # frames entre chaque tir

        # Invulnérabilité
        self.invuln_frames = 0
        self.invuln_duration = 30  # frames d'invulnérabilité après un coup
        

    def update(self, keys):
        # Mouvement
        self.velocity.x = 0
        self.velocity.y = 0

        if keys[pygame.K_z] or keys[pygame.K_w]:
            self.velocity.y = -self.speed
        if keys[pygame.K_s]:
            self.velocity.y = self.speed
        if keys[pygame.K_q] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
        if keys[pygame.K_d]:
            self.velocity.x = self.speed

        self.position += self.velocity
        self.rect.center = self.position

        # Cooldown tir
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Invulnérabilité et clignotement
        if self.invuln_frames > 0:
            self.invuln_frames -= 1
            # Clignotement
            if (self.invuln_frames // 3) % 2 == 0:
                self.image.set_alpha(60)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)
            
    def shoot(self, direction):
        if self.shoot_cooldown == 0 and direction.length() > 0:
            self.shoot_cooldown = self.shoot_delay
            direction = direction.normalize()
            return Projectile(self.rect.centerx, self.rect.centery, direction)
        return None
    
    def handle_shooting(self, keys):
        """Gestion du tir avec les flèches du clavier"""
        shoot_direction = pygame.math.Vector2(0, 0)
        if keys[pygame.K_UP]:
            shoot_direction.y = -1
        elif keys[pygame.K_DOWN]:
            shoot_direction.y = 1
        elif keys[pygame.K_LEFT]:
            shoot_direction.x = -1
        elif keys[pygame.K_RIGHT]:
            shoot_direction.x = 1
        
        if shoot_direction.length() > 0:
            return self.shoot(shoot_direction)
        return None