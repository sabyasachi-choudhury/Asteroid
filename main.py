import pygame
import random
import math
from pygame.locals import (QUIT, K_ESCAPE, KEYDOWN, K_SPACE)

# Initialize
pygame.init()


# Creating player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.transform.smoothscale(pygame.image.load("spaceship_small_red.png").convert(), (40, 40))
        self.og_surf = self.surf
        self.rect = self.surf.get_rect(center=(s_len / 2, s_len / 2))
        self.surf.set_colorkey(black)

    def look_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        trig_x, trig_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180/math.pi) * -math.atan2(trig_y, trig_x) - 90
        self.surf = pygame.transform.rotate(self.og_surf, angle)
        self.rect = self.surf.get_rect(center=self.rect.center)


# Creating asteroids
class Asteroids(pygame.sprite.Sprite):
    def __init__(self):
        super(Asteroids, self).__init__()
        # Picking sides
        sides = ['t', 'b', 'l', 'r']
        side = random.choice(sides)
        if side == 't':
            self.surf = pygame.transform.smoothscale(pygame.image.load("Asteroid_top.png").convert(), (70, 70))
            self.rect = self.surf.get_rect(center=(random.randint(0, s_len), 0))

        elif side == 'b':
            self.surf = pygame.transform.smoothscale(pygame.image.load("Asteroid_bottom.png").convert(), (70, 70))
            self.rect = self.surf.get_rect(center=(random.randint(0, s_len), s_len))

        elif side == 'l':
            self.surf = pygame.transform.smoothscale(pygame.image.load("Asteroid_left.png").convert(), (70, 70))
            self.rect = self.surf.get_rect(center=(0, random.randint(0, s_len)))

        elif side == 'r':
            self.surf = pygame.transform.smoothscale(pygame.image.load("Asteroid_right.png").convert(), (70, 70))
            self.rect = self.surf.get_rect(center=(s_len, random.randint(0, s_len)))

        self.rev_speed = 40
        self.step_x = int((s_len/2 - self.rect.centerx)/self.rev_speed)
        self.step_y = int((s_len/2 - self.rect.centery)/self.rev_speed)

    def fly(self):
        self.rect.move_ip(self.step_x, self.step_y)


# Missile class
class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super(Missile, self).__init__()
        self.surf = pygame.transform.smoothscale(pygame.image.load("new_bullet.png").convert(), (30, 30))
        self.rect = self.surf.get_rect(center=(s_len/2, s_len/2))
        self.surf.set_colorkey(black)
        self.rev_shoot_speed = 30
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.shoot_x = (mouse_x - s_len / 2) / self.rev_shoot_speed
        self.shoot_y = (mouse_y - s_len / 2) / self.rev_shoot_speed
        if self.shoot_y == 0 and self.shoot_x == 0:
            self.shoot_y = random.choice([-1, 1])
            self.shoot_x = random.choice([-1, 1])

    def shoot(self):
        self.rect.move_ip(self.shoot_x, self.shoot_y)


# Setting vars
run = True
s_len = 800
screen = pygame.display.set_mode((s_len, s_len))
score = 0
ast_timer = 1200
coll_sound = pygame.mixer.Sound("bounce.wav")
game_speed = 25

# Naming colors for simplicity
black = (0, 0, 0)

# Making player sprite
player = Player()

# Making groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Asteroid event
add_ast = pygame.USEREVENT + 1
pygame.time.set_timer(add_ast, ast_timer)

# Speed increase event
speed_inc = pygame.USEREVENT + 2
pygame.time.set_timer(speed_inc,  3000)

# Background music
pygame.mixer.Sound("Scientific music brief.mp3").play(loops=-1)

# Main loop
while run:
    # Screen fill
    screen.fill(black)

    # Event detection
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
            if event.key == K_SPACE:
                bullet = Missile()
                all_sprites.add(bullet)
                bullets.add(bullet)
        if event.type == add_ast:
            ast = Asteroids()
            all_sprites.add(ast)
            asteroids.add(ast)
        if event.type == speed_inc:
            game_speed = game_speed + 1 

    # Player looking
    player.look_mouse()

    # bullet shooting
    for bull in bullets:
        bull.shoot()

    # Asteroids moving
    for asteroid in asteroids:
        asteroid.fly()

    # Collisions
    if pygame.sprite.spritecollideany(player, asteroids):
        run = False

    for proj in bullets:
        for ast in asteroids:
            if pygame.sprite.spritecollideany(proj, asteroids):
                coll_sound.play()
                proj.kill()
                ast.kill()
                score += 1

    # Rendering
    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)
        if sprite.rect.top > s_len or sprite.rect.left > s_len or sprite.rect.right < 0 or sprite.rect.bottom < 0:
            sprite.kill()

    # display.flip
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(game_speed)

# Quitting
pygame.quit()
print(score)