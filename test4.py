import pygame


pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
CAR_IMAGE = pygame.Surface((45, 90), pygame.SRCALPHA)
CAR_IMAGE.fill((150, 20, 0))


class Car(pygame.sprite.Sprite):

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
            self.rect = self.image.get_rect(center=self.rect.center)


all_sprites = pygame.sprite.Group()
f1_car = Car((300, 300), CAR_IMAGE)
all_sprites.add(f1_car)

carryOn = True

while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.KEYDOWN:
            # Set the rotation speed of the car sprite.
            if event.key == pygame.K_RIGHT:
                f1_car.angle_change = -3
            elif event.key == pygame.K_LEFT:
                f1_car.angle_change = 3
        elif event.type == pygame.KEYUP:
            # Stop rotating if the player releases the keys.
            if event.key == pygame.K_RIGHT and f1_car.angle_change < 0:
                f1_car.angle_change = 0
            elif event.key == pygame.K_LEFT and f1_car.angle_change > 0:
                f1_car.angle_change = 0

    all_sprites.update()

    screen.fill(WHITE)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()