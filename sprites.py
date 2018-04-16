# THIS IS FOR ALL THE SPRITE CLASSES IN MY GAME
import pygame
from settings import *
vec = pygame.math.Vector2
# THIS IS FOR THE PLAYER MOVEMENT
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((30,40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        #you can only jump when on platform
        self.rect.x +=1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20


    def update(self):
        self.acc = vec(0, 0.8)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        #THIS IS FOR THE FRICTION OF THE PLAYER
        self.acc.x += self.vel.x * PLAYER_FRICTION
        #THIS TO SET THE MOTION OF THE PLAYER
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #THIS IS SO THAT THE PLAYER DOESNT GO OFF SCREEN
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        
        self.rect.midbottom = self.pos

#THIS IS FOR PLATFORMS
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(RED)
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    
