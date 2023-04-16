from pygame import *    #подключить пай гейм
from random import randint  #подключить рандинт

mixer.init()    #подключить миксер
mixer.music.load('space.ogg')   #загрузить музыку
mixer.music.play()  #музыка должна проигрыватся
fire_sound = mixer.Sound('fire.ogg')    #проигрывание музыки при выстеле

font.init() #подключить шрифт
font2 = font.SysFont('Arial',36)  #шрифт 36
font1 = font.SysFont('Arial',80)  #шрифт 80
win = font1.render('мега хорош',True,(50,50,50))    #вывести надпись при победе
lose = font2.render('мега плох',True,(150,150,150)) #вывести надпись при проигрыше

lost = 0    #склько пропущено
scare = 0   #сколько сбито
goal = 10   #сколько надо сбить
max_lost = 10   #сколько можно пропустить

class GameSprite(sprite.Sprite):#класс родитель
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed#сверху написан плеер спид а селф делает это для всех и в спрайтах пишется скорость и потом относится к деф
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a]and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d]and self.rect.x  < 900:
            self.rect.x += self.speed
        if keys[K_w]and self.rect.y  > 5:
            self.rect.y -= self.speed
        if keys[K_s]and self.rect.y  < 500:
            self.rect.y += self.speed
    def bylit_up(self):
        bylit_up = Bullet('bylit_up.png',self.rect.centerx, self.rect.top, 15,20,-15)#расположение, расположение 2, размер х, размер у,с корость
        sprite3_1.add(bylit_up)
    def bylit_down(self):
        bylit_down = Bullet('bylit_down.png',self.rect.centerx, self.rect.botom, 15,20,15)
        sprite3_1.add(bylit_down)
    def bylit_left(self):
        bylit_left = Bullet('bylit_left.png',self.rect.left, self.rect.centery, 15,20,-15)
        sprite3_1.add(bylit_left)
    def bylit_right(self):
        bylit_right = Bullet('bylit_right.png',self.rect.right, self.rect.centery, 15,20,15)
        sprite3_1.add(bylit_right)
        
class Enemy (GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >600:
            self.rect.x = randint(0,950)
            self.rect.y = 0
            lost = lost + 1

class Enemy_2 (GameSprite):
    def update(self):
        self.rect.y -= self.speed
        global lost
        if self.rect.y < -100:
            self.rect.x = randint(0,950)
            self.rect.y = 700
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

window = display.set_mode((1000,600))#размер экрана
display.set_caption('Чёрная мерть')#название приложения
fon = transform.scale(image.load('fon.png'),(1000,600))#картинка фона и её размер

sprite1_1 = sprite.Group()
sprite1 = Player('igrok.png',450, 250, 100, 100, 5)#координаты  х у  ,размер высота ширина, скорость
sprite1_1.add(sprite1)

sprite2_1 = sprite.Group()
for i in range (5):
    sprite2 = Enemy('ufo.png',randint(0,950), -100, 40, 80, randint(1,2))#monsrt
    sprite2_1.add(sprite2)#monsrtS

sprite2_2 = sprite.Group()
for i in range (5):
    sprite2_3 = Enemy_2('pngegg.png',randint(0,950), 700, 80, 80, 1)
    sprite2_2.add(sprite2_3)

sprite3_1 = sprite.Group()

game = True  #run
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:#иначе выход, крестик кароче
            game = False
        elif e.type == KEYDOWN:#е.тепе это действие   кейдаун это опущения кнопка
            if e.key == [K_y]:
                fire_sound.play()
                sprite1_1.bylit_up()
            elif e.key == [K_h]:
                fire_sound.play()
                sprite1_1.bylit_down()
            elif e.key == [K_g]:
                fire_sound.play()
                sprite1_1.bylit_left()
            elif e.key == [K_j]:
                fire_sound.play()
                sprite1_1.bylit_right()

    if not finish:
        window.blit(fon,(0,0))
        text = font2.render('счёт:'+str(scare), 1, (255,255,255))
        text_lose = font2.render('пропущено:'+str(lost), 1, (255,255,255))
        window.blit(text,(10,70))
        window.blit(text_lose,(10,50))
        #движение спрайтов
        sprite1.update()
        sprite1.reset()

        sprite2_1.update()
        sprite2_1.draw(window)

        sprite2_2.update()
        sprite2_2.draw(window)

        sprite3_1.update()
        sprite3_1.draw(window)

        display.update()

    collides = sprite.groupcollide(sprite1_1, sprite2_1, True, True)
    collides = sprite.groupcollide(sprite2_2, sprite3_1, True, True)
    for c in collides:
        scare = scare + 1

        sprite2 = Enemy('ufo.png',randint(0,950), -100, 40, 80, randint(1,2))
        sprite2_1.add(sprite2)

        sprite2_3 = Enemy_2('pngegg.png',randint(0,950), 700, 80, 80, 1)
        sprite2_2.add(sprite2_3)

        if sprite.spritecollide(sprite1_1, sprite2_1, False,False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        if sprite.spritecollide(sprite1_1, sprite2_2, False,False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))  

        if scare >= goal:
            finish = True
            window.blit(win,(200,200))
        
    '''else:
        finish = False
        scare = 0
        lost = 0
        for d in sprite3_1:
            d.kill
        for n in sprite2_1:
            n.kill
        for b in sprite2_2:
            b.kill
        time.delay(3)

        for i in range (5):
            sprite2 = Enemy('ufo.png',randint(0,950), -100, 40, 80, randint(1,2))#monsrt
            sprite2_1.add(sprite2)#monsrtS

        for i in range (5):
            sprite2_3 = Enemy_2('pngegg.png',randint(0,950), 700, 80, 80, 1)
            sprite2_2.add(sprite2_3)
'''
    time.delay(1)