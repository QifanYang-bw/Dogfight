import pygame
import random

WIDTH = 640  # width of our game window
HEIGHT = 480 # height of our game window
FPS = 30 # frames per second

clock = pygame.time.Clock()

 # Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
IMAGE = pygame.image.load('resources/plane1.png').convert_alpha()

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        # Store a reference to the original to preserve the image quality.
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)

        self.angle = 0
        self.angle_change = 0

    def update(self):
        if self.angle_change != 0:
            self.angle += self.angle_change
            # I prefer rotozoom because it looks smoother.
            self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
            self.rect = self.image.get_rect(center = self.rect.center)

# initialize pygame and create window
pygame.init()
# pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()
player = Player((WIDTH / 2, HEIGHT / 2), IMAGE)
all_sprites.add(player)

# Game loop
running = True
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Set the rotation speed of the car sprite.
            if event.key == pygame.K_RIGHT:
                player.angle_change = -3
            elif event.key == pygame.K_LEFT:
                player.angle_change = 3
        elif event.type == pygame.KEYUP:
            # Stop rotating if the player releases the keys.
            if event.key == pygame.K_RIGHT and player.angle_change < 0:
                player.angle_change = 0
            elif event.key == pygame.K_LEFT and player.angle_change > 0:
                player.angle_change = 0

    all_sprites.update()

    screen.fill(BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()


    # # keep loop running at the right speed
    # clock.tick(FPS)
    # # Process input (events)
    # for event in pygame.event.get():
    #     # check for closing window
    #     if event.type == pygame.QUIT:
    #         running = False

    # # Update
    # all_sprites.update()

    # # Draw / render
    # screen.fill(BLACK)
    # all_sprites.draw(screen)
    # # *after* drawing everything, flip the display
    # pygame.display.flip()
