from pygame import *
from random import shuffle
import math
from time import time as timer






level = [
       "c                    c                        c                      c",
       "----------------------------------------------------------------------",
       "cicccc                                                                ",
       "ciccccci                                                              ",
       "ciccccciccics                                                         ",
       "ciccciciccicsssi                                                      ",
       "ciciciciccicsssiisg                                                   ",
       "ciciciciccicsssiisgs                                                  ",
       "ciciciciccicsssiisgss                                                 ",
       "ciciciciccicsssiisgssg                                                ",
       "ciciciciccicsssiisgsssgis                                             ",
       "ciciciciccicsssiisgsssgisis                                           ",
       "ciciciciccicsssiisgsssgisisg                                          ",
       "ciciciciccicsssiisgsssgisisgss                                        ",
       "ciciciciccicsssiisgsssgisisgssg                                       ",
       "ciciciciccicsssiisgsssgisisgssgsi                                     ",
       "ciciciciccicsssiisgsssgisisgssgsiss                                   ",
       "ciciciciccicsssiisgsssgisisgssgsissg                                  "]


#перемешивание букв в каждой строке списка

lines_number = 0
text_list = list()






for line in level:
    for letter in line:
        text_list.append(letter)
    shuffle(text_list)
    line = ""
    for letter in text_list:
        line += letter
    level[lines_number] = line
    lines_number += 1
    text_list = list()






# створюємо вікно гри
W = 1280
H = 720
win = display.set_mode((W, H))

display.set_caption('Miner')



# підвантажуємо картинки спрайтів

hero_image = "images/Шахтер в каске.png"
hero_image_l = "images/Шахтёр в каске_l.png"

ground = "images/Земля.png"
coal = "images/уголь.png"
iron = "images/Железо.png"
silver = "images/Серебро.png"
gold ="images/Золото.png"

background = "images/Земля фон фулл.png"





left = True
class Settings(sprite.Sprite):
    def __init__(self, x, y, w, h, speed, img):
        super().__init__()

        self.width = w
        self.height = h
        self.image = transform.scale(image.load(img), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed


        self.HP = 2


class Player(Settings):
    def r_l(self):
        global hero_image, hero_image_l, left, level_width
        keys = key.get_pressed()
        if keys[K_d]:
            if self.rect.x <= level_width-20:
                self.rect.x += self.speed
                if left == False:
                    self.image = transform.scale(image.load(hero_image), (self.width, self.height))
                    left = True
        if keys[K_a]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed
                if left:
                    self.image = transform.scale(image.load(hero_image_l), (self.width, self.height))
                    left = False
    def u_d(self):
        global level_hight
        keys = key.get_pressed()
        if keys[K_s]:
            if self.rect.y < level_hight-50:
                self.rect.y += self.speed
        if keys[K_w]:
            if self.rect.y > 0:
                self.rect.y -= self.speed

    def move(self):
        self.r_l()
        self.u_d()



    def dig(self):
        global cube_size, old_time


        center_x = self.rect.x + self.width
        center_y = self.rect.y + self.height


        line_of_objekt = center_y/cube_size
        line_of_objekt = math.floor(line_of_objekt) #Округление только в меньшую сторону (было 6.5 - стало 6)
        line_of_objekt *= cube_size

        column_of_objekt = center_x/cube_size
        column_of_objekt = math.floor(column_of_objekt) #Округление только в меньшую сторону (было 6.5 - стало 6)
        column_of_objekt *= cube_size

        new_time = timer()
        
        keys = key.get_pressed()

        if keys[K_RIGHT]:
            if new_time-old_time >= 0.5:
                old_time = timer()
                for r in nearby:
                    if r.rect.x == column_of_objekt+cube_size and r.rect.y == line_of_objekt:
                        r.HP -= 1
        if keys[K_LEFT]:
            if new_time-old_time >= 0.5:
                old_time = timer()
                for r in nearby:
                    if r.rect.x == column_of_objekt-cube_size and r.rect.y == line_of_objekt:
                        r.HP -= 1


        if keys[K_UP]:
            if new_time-old_time >= 0.5:
                old_time = timer()
                for r in nearby:
                    if r.rect.x == column_of_objekt and r.rect.y == line_of_objekt-cube_size:
                        r.HP -= 1
        if keys[K_DOWN]:
            if new_time-old_time >= 0.5:
                old_time = timer()
                for r in nearby:
                    if r.rect.x == column_of_objekt and r.rect.y == line_of_objekt+cube_size:
                        r.HP -= 1








class Camera():
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)


    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + W/2, -t + H/2

    l = min(0, l)
    l = max(-(camera.width-W), l)
    t = max(-(camera.height-H), t)
    t = min(0, t)

    return Rect(l, t, w, h)
    

    




#размер каждого блока в игре
cube_size = 90

#Создание изначального прохода
level[0] = level[0][0:6] + "-"*5 + level[0][6+5:]

level_width = len(level[0])*cube_size
level_hight = len(level)*cube_size

items = sprite.Group()

# цикл, який малює рівень
x = y = 0
for line in level: # обираємо елемент зі списку level
    for c in line: # обираємо символ
        # якщо символ такий, замість нього промальовуємо таку картинку
        if c == "c": # Уголь
            r = Settings(x, y, cube_size, cube_size, 0, coal)
            items.add(r)
        
        if c == "i": # Железо
            r = Settings(x, y, cube_size, cube_size, 0, iron)
            items.add(r)

        if c == "s": # Серебро
            r = Settings(x, y, cube_size, cube_size, 0, silver)
            items.add(r)
                
        if c == "g": # Золото
            r = Settings(x, y, cube_size, cube_size, 0, gold)
            items.add(r)

        if c == " ":
            r = Settings(x, y, cube_size, cube_size, 0, ground)
            items.add(r)

        x += cube_size # кожного разу зміщуємо малюнок на 40 ліворуч
    y += cube_size # вкінці, спускаємось на 1 ряд
    x = 0  # починаємо малювати спочатку  







hero = Player(7*cube_size, 10, 40, 60, 5, hero_image)
camera = Camera(camera_configure, level_width, level_hight)


bg = Settings(0, 0, level_width, level_hight, 0, background)

old_time = timer()#Используется для задержки между ударами кирки




game = True

#список соседних блоков
nearby = list()
while game:
    

    time.delay(15)


    for e in event.get():
        if e.type == QUIT:
            game = False





    #Запоминаем координаты до перемещения героя
    hero_x = hero.rect.x 
    hero_y = hero.rect.y

    hero.move()
    




    camera.update(hero)
    win.blit(bg.image, camera.apply(bg))
    for r in items:
        win.blit(r.image, camera.apply(r))
        if abs(r.rect.x - hero.rect.x) < cube_size+30:
            if abs(r.rect.y - hero.rect.y) < cube_size+30:
                nearby.append(r)


    for f in nearby:
        #вичисляем из какой строки в списке level объект f
        line_of_level_f = hero_y/cube_size
        line_of_level_f = math.floor(line_of_level_f) #Округление только в меньшую сторону (было 6.5 - стало 6)
        line_of_level_f *= cube_size

        column_of_level_f = hero_x/cube_size
        column_of_level_f = math.floor(column_of_level_f) #Округление только в меньшую сторону (было 6.5 - стало 6)
        column_of_level_f *= cube_size
        
        if f.rect.y != line_of_level_f: 
            if sprite.collide_rect(hero, f):
                hero.rect.y = hero_y
        if f.rect.x != column_of_level_f:
            if sprite.collide_rect(hero, f):
                hero.rect.x = hero_x



        if f.HP <= 0:
            items.remove(f)

    hero.dig()

        










    win.blit(hero.image, camera.apply(hero))


    nearby = list()
    display.update()