import pygame.sprite
from pygame import *
from random import *


class Spritik(sprite.Sprite):
    def __init__(self, s_image, x, y, speed, weight, high):
        super().__init__()
        self.image = transform.scale(image.load(s_image), (weight, high))

        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(Spritik):
    def move(self):
        pressed_keys = key.get_pressed()

        if pressed_keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if pressed_keys[K_d] and self.rect.x < 1215:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 15, 20)
        bullets.add(bullet)


class Enemy(Spritik):
    def update(self):
        global loose_ino
        self.rect.y += self.speed
        if self.rect.y > 720:
            self.rect.x = randint(0, 1230)
            self.rect.y = -(randint(0, 50))
            loose_ino += 1


class Asteroid(Spritik):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 720:
            self.rect.x = randint(0, 1230)
            self.rect.y = -(randint(0, 50))


class Bullet(Spritik):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


window = display.set_mode((1280, 720))
display.set_caption('шутер')

background = transform.scale(image.load('galaxy.jpg'), (1280, 720))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0)
mixer.music.play()
sound = mixer.Sound('fire.ogg')

player = Player('rocket.png', 740, 600, 8, 80, 120)

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(0, 1230), -(randint(0, 50)), randint(1, 4), 80, 50)
    monsters.add(monster)

asteroids = sprite.Group()
asteroid = Asteroid('asteroid.png', randint(0, 1230), -(randint(0, 50)), randint(1, 4), 50, 50)
asteroids.add(asteroid)
clock = time.Clock()

game = 1
finish = False
loose_ino = 0
schot_int = 0
health = 3
font.init()
font1 = font.SysFont('Arial', 90)
win = font1.render('You win!', True, (0, 255, 180))
loose = font1.render('You loose!', True, (0, 255, 180))
font2 = font.SysFont('Arial', 30)
loose_inoplanetans = font2.render('пропущено:' + str(loose_ino), True, (0, 255, 180))
schot = font2.render('счёт:' + str(schot_int), True, (0, 255, 180))

while game:
    for i in event.get():
        if i.type == QUIT:
            game = 0
        if i.type == KEYDOWN and i.key == K_SPACE:
            player.fire()
    if not finish:
        window.blit(background, (0, 0))

        sprites_list = sprite.groupcollide(bullets, monsters, True, True)
        for colide in sprites_list:
            schot_int += 1
            monster = Enemy('ufo.png', randint(0, 1230), -(randint(0, 50)), randint(1, 4), 80, 50)
            monsters.add(monster)
        # if schot_int >= 10:
        #     window.blit(win, (500, 320))
        #     finish = True

        sprite.groupcollide(bullets, asteroids, True, False)

        if loose_ino >= 15 or health == 0:
            finish = True
            window.blit(loose, (500, 320))

        if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, asteroids, True):
            health -= 1

        loose_inoplanetans = font2.render('пропущено:' + str(loose_ino), True, (0, 255, 180))
        schot = font2.render('счёт:' + str(schot_int), True, (0, 255, 180))
        health_schot = font2.render('жизни:' + str(health), True, (0, 255, 180))

        window.blit(loose_inoplanetans, (5, 5))
        window.blit(schot, (5, 35))
        window.blit(health_schot, (5, 65))

        monsters.update()
        monsters.draw(window)

        asteroids.update()
        asteroids.draw(window)

        bullets.update()
        bullets.draw(window)

        player.move()
        player.reset()

        clock.tick(60)
        display.update()
