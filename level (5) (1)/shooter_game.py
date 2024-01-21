#Створи власний Шутер!

from typing import Any 
from pygame import * 
from random import randint 

mixer.init()  
mixer.music.load("space.ogg")  
mixer.music.play()  
fire_sound = mixer.Sound('fire.ogg') 
 
font.init() 
font1 = font.Font(None, 100) 
win  = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', False, (180, 0, 0))
font2 = font.SysFont('Arial', 40) 

img_back = "fon.png" 
img_hero = "mario.png" 
img_enemy = "grub.png" 
img_bullet = "rose.png" 
img_enemy2 = "money.png"
 
goal = 15 
score = 0 
lost = 0 
max_lost = 5 
 
class GameSprite(sprite.Sprite): 
    def __init__(self, player_imege, player_x, player_y, size_x, size_y, player_speed): 
        sprite.Sprite.__init__(self) 
        self.image = transform.scale(image.load(player_imege), (size_x, size_y)) 
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y 
 
    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y)) 
 
class Player(GameSprite): 
    def update(self): 
        keys = key.get_pressed() 
        if keys[K_LEFT] and self.rect.x > 5: 
            self.rect.x -= self.speed 
        if keys[K_RIGHT] and self.rect.x < win_width - 80: 
            self.rect.x += self.speed 
 
    def fire(self): 
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15) 
        bullets.add(bullet) 
 
class Enemy(GameSprite): 
    def update(self): 
        self.rect.y += self.speed 
        global lost  
        if self.rect.y > win_height: 
            self.rect.x = randint(80, win_width -80) 
            self.rect.y = 0 
            lost += 1 
 
class Bullet(GameSprite): 
    def update(self): 
        self.rect.y += self.speed 
        if self.rect.y < 0: 
            self.kill() 
 
win_width = 700  
win_height = 500  
display.set_caption("Shooter")  
window = display.set_mode((win_width, win_height))  
background = transform.scale(image.load(img_back), (win_width, win_height))  
 
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10) 
monsters = sprite.Group() 
for i in range(1, 6): 
    monster = Enemy(img_enemy, randint(80, win_width -80), -40, 80, 50, randint(1, 5)) 
    monster = Enemy(img_enemy2, randint(80, win_width -80), -40, 80, 50, randint(1, 5)) 
    monsters.add(monster) 
 
bullets = sprite.Group() 
 
finish = False 
 
run = True  
 
while run: 
    for e in event.get(): 
        if e.type == QUIT: 
            run = False 
 
        elif e.type == KEYDOWN: 
            if e.key == K_SPACE: 
                fire_sound.play() 
                ship.fire() 
 
    if not finish: 
        window.blit(background, (0, 0)) 
        text = font2.render("Рахунок: " + str(score), 4, (255, 255, 255)) 
        window.blit(text, (10, 20)) 
 
        text2 = font2.render("Монети: " + str(lost), 1, (255, 255, 255)) 
        window.blit(text2, (10, 50)) 
 
        ship.update() 
        monsters.update() 
        bullets.update() 
 
        ship.reset() 
        monsters.draw(window) 
        bullets.draw(window) 
 
        collides = sprite.groupcollide(monsters, bullets, True, True) 
        for c in collides: 
            score = score + 1 
            monster = Enemy(img_enemy, randint(80, win_width -80), -40, 80, 50, randint(1, 5)) 
            monsters.add(monster) 

        collides = sprite.groupcollide(monsters, bullets, True, True) 
        for c in collides: 
            score = score + 1
            monster = Enemy(img_enemy2, randint(80, win_width -80), -40, 80, 50, randint(1, 5)) 
            monsters.add(monster) 
 
        if sprite.spritecollide(ship, monsters, True) or lost >= max_lost: 
            finish =False
            
         
        if score >= goal: 
            finish = False
            window.blit(win, (200, 200)) 
 
        display.update() 
 
    time.delay(40)