#This game is called Hopster
import pygame
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        #for the game window
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Hopster")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)

    def new(self):
        # this starts a new game
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for platform in PLATFORM_LIST:
            p = Platform(*platform)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # this is for the game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        #this is for the updates in the game loop
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y= 0

        #This is for the camera to move up when going up the screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for platform in self.platforms:
                platform.rect.y += abs(self.player.vel.y)
                if platform.rect.top >= HEIGHT:
                    platform.kill()
                    self.score += 1

        #Death
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        #Spawing platforms
        while len(self.platforms) < 6:
            width = random.randrange(25, 100)
            p = Platform(random.randrange(0, WIDTH-width) ,
                         random.randrange(-75, -30),
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        # this is for the events in the game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key== pygame.K_SPACE:
                    self.player.jump()

    def draw(self):
        # this is for the drawing of stuff in the game loop
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 30, WHITE, WIDTH / 2, 15)
        pygame.display.flip()
        

    def show_start_screen(self):
        # this shows the start screen of the game
        self.screen.fill(BLACK)
        self.draw_text("Hopster", 50, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Move With Arrows, Jump With Space", 25, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a Key to Play", 25, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # this shows the game over screen
        if not self.running:
            return
        self. screen.fill(BLACK)
        self.draw_text("Game Over", 50, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score:" + str(self.score), 25, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a Key to Play Again", 25, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()


    def wait_for_key(self):
        #This is so that you can press a key to start
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        #This is to show the text on screen
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)    
            
            

   
    
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pygame.quit()
