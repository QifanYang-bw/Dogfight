import sys

import pygame as pg


class Enemy(pg.sprite.Sprite):
    def __init__(self, centerpoint, *groups):
        super(Enemy, self).__init__(*groups)
        self.rect = pg.Rect(0, 0, 64, 64)
        self.rect.center = centerpoint
        self.pos = self.rect.center
        self.image = pg.Surface(self.rect.size)
        self.image.fill(pg.Color("dodgerblue"))
        self.speed = .1

    def move(self, dt):
        self.pos = self.pos[0] + (self.speed * dt), self.pos[1]
        self.rect.center = self.pos
        
    def update(self, dt):
        self.move(dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Game(object):
    def __init__(self):
        self.done = False
        self.screen = pg.display.set_mode((320, 240))
        self.screen_rect = self.screen.get_rect()
        self.fps = 120
        self.clock = pg.time.Clock()
        self.spawn_timer = 0
        self.spawn_frequency = 3000 #milliseconds
        self.enemies = pg.sprite.Group()

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done  = True

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_frequency:
            print("SPAWN")
            self.spawn_timer -= self.spawn_frequency
            Enemy(self.screen_rect.center, self.enemies)
        self.enemies.update(dt)

    def draw(self):
        self.screen.fill(pg.Color("gray10"))
        self.enemies.draw(self.screen)

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
    pg.quit()
    sys.exit()