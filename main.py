import pygame
import random
import os
# Player
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, gravity):

        # Player dimensions and position

        self.gravity = gravity

        # Player image and animation
        self.images = []
        self.images.append(pygame.image.load('Assets/space.png'))
        self.images.append(pygame.image.load('Assets/spaceship_red.png'))
        #~ self.images.append(pygame.image.load(os.path.join('ball1.png'))
        #~ self.images.append(pygame.image.load(os.path.join('ball2.png'))
        self.maxImage = len(self.images)
        self.currentImage = 0

        #~ self.rect = pygame.Rect(x, y, 80, 80)
        self.rect = self.images[0].get_rect()
        self.rect.x = x
        self.rect.y = y

        self.timeTarget = 10
        self.timeNum = 0

        self.velX = 0
        self.velY = 0

        # Jump and gravity
        self.vSpeed = 1
        self.jumpForce = 8
        self.maxVspeed = 3
        self.isJumping = False

    # Jump inputs
    def handle_events(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                if not self.isJumping:
                    self.isJumping = True

            elif event.key == pygame.K_a:
                self.velX = -5

            elif event.key == pygame.K_d:
                self.velX = +5

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d):
                self.velX = 0 

        print ("isJumping:"), self.isJumping

    # PLayer updates
    def update(self, ground):

        # Jumping

        self.vSpeed -= self.gravity

        if self.vSpeed > self.maxVspeed:
            self.vSpeed = self.maxVspeed

        self.rect.y -= self.vSpeed

        if self.isJumping:
            self.vSpeed -= self.jumpForce

        if self.rect.bottom >= ground.y:
            self.vSpeed = 0
            self.rect.bottom = ground.y
            self.isJumping = False


        # Animations

        if self.timeNum == self.timeTarget:
            self.currentImage += 1
            if self.currentImage >= self.maxImage:
                self.currentImage = 0
            self.timeNum = 0

        self.rect.centerx += self.velX
        self.rect.centery += self.velY

        # Screen wrap
        if self.rect.right > 1280:
            self.rect.left = 0

        elif self.rect.left < 0:
            self.rect.right = 1280

    # Player rendering
    def render(self, surface):
        surface.blit(self.images[self.currentImage], self.rect)

#----------------------------------------------------------------------

class Zombie():

    def __init__(self, x, y):

        self.image = pygame.image.load(os.path.join('Assets/space.png')
        #~ self.image = pygame.image.load(os.path.join('ball2.png')
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.direction_left = True

    def update(self, surface_rect):
        if self.direction_left:
            self.rect.x -= 1
            if self.rect.left <= surface_rect.left:
                self.direction_left = not self.direction_left
        else:
            self.rect.x += 1
            if self.rect.right >= surface_rect.right:
                self.direction_left = not self.direction_left

    def render(self, surface):
        surface.blit(self.image, self.rect)

#----------------------------------------------------------------------

class Background():

    def __init__(self):

        self.image = pygame.image.load(os.path.join('Assets/space.png')
        #~ self.image = pygame.image.load(os.path.join('background.jpg')
        self.rect = self.image.get_rect()

    def render(self, surface):
        surface.blit(self.image, self.rect)

#----------------------------------------------------------------------

class Game():

    def __init__(self):
        pygame.init()

        # A few variables
        self.gravity = .50
        self.ground = pygame.Rect(0, 720, 0, 0)

        # Screen
        size = (1280, 720)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Moon Survival!')

        # Moon / Background
        self.moon = Background()

        # Zombies
        self.zombies = []
        for i in range(10):
            self.zombies.append( Zombie(random.randint(0,1280), random.randint(0,720)) )

        # Player
        self.player = Player(25, 320, self.gravity)

        # Font for text
        self.font = pygame.font.SysFont(None, 72)

        # Pause - center on screen
        self.pause_text = self.font.render("PAUSE", -1, (255,0,0))
        self.pause_rect = self.pause_text.get_rect(center = self.screen.get_rect().center)

    def run(self):

        clock = pygame.time.Clock()

        # "state machine" 
        RUNNING   = True
        PAUSED    = False 
        GAME_OVER = False

        # Game loop
        while RUNNING:

            # (all) Events

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    RUNNING = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        RUNNING = False

                    elif event.key == pygame.K_p:
                        PAUSED = not PAUSED

                # Player/Zomies events  

                if not PAUSED and not GAME_OVER:
                    self.player.handle_events(event)

            # (all) Movements / Updates

            if not PAUSED and not GAME_OVER:
                self.player.update(self.ground)
                for z in self.zombies:
                    z.update(self.screen.get_rect())

            # (all) Display updating

            self.moon.render(self.screen)

            for z in self.zombies:
                z.render(self.screen)

            self.player.render(self.screen)

            if PAUSED:
                self.screen.blit(self.pause_text, self.pause_rect)

            pygame.display.update()

            # FTP

            clock.tick(75)

        # --- the end ---
        pygame.quit()

#---------------------------------------------------------------------

Game().run()
