from random import randint

from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, image_name, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(image_name), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def update(self, screen):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < window_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 10, 20, 15)
        bullets.add(bullet)
class Enemy(GameSprite):

    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= window_height - 80:
            lost += 1
            self.rect.x = randint(0, window_width - 100)
            self.rect.y = 0
            self.speed = randint(1, 5)

class Bullet(GameSprite):

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

window_width = 700
window_height = 500

lost = 0

bullets = sprite.Group()
enemies = sprite.Group()
for i in range(5):
    rand_x = randint(0, window_width - 100)
    enemy = Enemy("ufo.png", rand_x, 0, 100, 80, randint(1, 5))
    enemies.add(enemy)

window_width = 700
window_height = 500
window = display.set_mode((window_width, window_height))

background = transform.scale(image.load("galaxy.jpg"), (window_width, window_height))

player = Player("rocket.png", 100, 400, 80, 100, 5)

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")


clock = time.Clock()
fps = 60

run = True
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN and e.key == K_SPACE:
            player.fire()
            fire_sound.play()


    window.blit(background, (0, 0))

    player.update(window)
    player.reset(window)

    enemies.update()
    enemies.draw(window)

    bullets.update()
    bullets.draw(window)

    display.update()
    clock.tick(fps)
