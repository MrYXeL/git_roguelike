import pygame

WHITE = (255, 255, 255)
RED = (200, 50, 50)
YELLOW = (255, 255, 0)

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

        if (self.rect.right < 0 or self.rect.left > 1280 or
            self.rect.bottom < 0 or self.rect.top > 720):
            self.kill()

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.base_image = pygame.Surface((32, 32))
        self.base_image.fill(RED)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = 4
        self.health = 6
        self.max_health = 6

        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)

        self.shoot_cooldown = 0
        self.shoot_delay = 15

        self.invuln_frames = 0
        self.invuln_duration = 30

    def update(self, keys):
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

        # Limites écran
        self.position.x = max(16, min(1264, self.position.x))
        self.position.y = max(16, min(704, self.position.y))

        self.rect.center = self.position

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.invuln_frames > 0:
            self.invuln_frames -= 1
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
        direction = pygame.math.Vector2(0, 0)

        if keys[pygame.K_UP]:
            direction.y = -1
        elif keys[pygame.K_DOWN]:
            direction.y = 1
        elif keys[pygame.K_LEFT]:
            direction.x = -1
        elif keys[pygame.K_RIGHT]:
            direction.x = 1

        if direction.length() > 0:
            return self.shoot(direction)

        return None