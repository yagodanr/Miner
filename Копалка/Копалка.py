from pygame import *
from random import shuffle
import math
from time import time as timer






#level = [
#       "c                    c                        c                      c",
#       "----------------------------------------------------------------------",
#       "cicccc                                                                ",
#       "ciccccci                                                              ",
#       "ciccccciccics                                                         ",
#       "ciccciciccicsssi                                                      ",
#       "ciciciciccicsssiisg                                                   ",
#       "ciciciciccicsssiisgs                                                  ",
#       "ciciciciccicsssiisgss                                                 ",
#       "ciciciciccicsssiisgssg                                                ",
#       "ciciciciccicsssiisgsssgis                                             ",
#       "ciciciciccicsssiisgsssgisis                                           ",
#       "ciciciciccicsssiisgsssgisisg                                          ",
#       "ciciciciccicsssiisgsssgisisgss                                        ",
#       "ciciciciccicsssiisgsssgisisgssg                                       ",
#       "ciciciciccicsssiisgsssgisisgssgsi                                     ",
#       "ciciciciccicsssiisgsssgisisgssgsiss                                   ",
#       "ciciciciccicsssiisgsssgisisgssgsissg                                  "]




level = [
       "c                    c  c      c",
       "--------------------------------",
       "ciciciciccicsssiisgsssgisis     ",
       "ciciciciccicsssiisgsssgisisg    ",
       "ciciciciccicsssiisgsssgisisgss  "]






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






#размер каждого блока в игре
cube_size = 90

#Создание изначального прохода
level[0] = level[0][0:6] + "-"*5 + level[0][6+5:]

level_width = len(level[0])*cube_size
level_hight = len(level)*cube_size







left = True

time_not_dig = 0.2
class Settings(sprite.Sprite):
    def __init__(self, x, y, w, h, speed, img, img_break = "images/Земля_ломается.png"):
        super().__init__()

        self.width = w
        self.height = h
        self.image = transform.scale(image.load(img), (self.width, self.height))
        self.image_broken = transform.scale(image.load(img_break), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed

        self.broken = False
        
        self.HP = 2
    def switch_image_to_broken(self):
        self.image = self.image_broken

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
    
    


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
        global cube_size, old_time, time_not_dig, stamina
        if stamina > 0:

            center_x = self.rect.x + self.width/2
            center_y = self.rect.y + self.height/2


            line_of_objekt = center_y/cube_size
            line_of_objekt = math.floor(line_of_objekt) #Округление только в меньшую сторону (было 6.5 - стало 6)
            line_of_objekt *= cube_size

            column_of_objekt = center_x/cube_size
            column_of_objekt = math.floor(column_of_objekt) #Округление только в меньшую сторону (было 6.5 - стало 6)
            column_of_objekt *= cube_size

            new_time = timer()
            
            keys = key.get_pressed()

            if keys[K_RIGHT]:
                if new_time-old_time >= time_not_dig:
                    old_time = timer()
                    for r in nearby:
                        if r.rect.x == column_of_objekt+cube_size and r.rect.y == line_of_objekt:
                            r.HP -= 1
                            stamina -= 1
                            if r.broken == False:
                                r.switch_image_to_broken()
                                r.broken = True
            if keys[K_LEFT]:
                if new_time-old_time >= time_not_dig:
                    old_time = timer()
                    for r in nearby:
                        if r.rect.x == column_of_objekt-cube_size and r.rect.y == line_of_objekt:
                            r.HP -= 1
                            stamina -= 1
                            if r.broken == False:
                                r.switch_image_to_broken()
                                r.broken = True


            if keys[K_UP]:
                if new_time-old_time >= time_not_dig:
                    old_time = timer()
                    for r in nearby:
                        if r.rect.x == column_of_objekt and r.rect.y == line_of_objekt-cube_size:
                            r.HP -= 1
                            stamina -= 1
                            if r.broken == False:
                                r.switch_image_to_broken()
                                r.broken = True
            if keys[K_DOWN]:
                if new_time-old_time >= time_not_dig:
                    old_time = timer()
                    for r in nearby:
                        if r.rect.x == column_of_objekt and r.rect.y == line_of_objekt+cube_size:
                            r.HP -= 1
                            stamina -= 1
                            if r.broken == False:
                                r.switch_image_to_broken()
                                r.broken = True





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













def city():
    global volleyball_court, city_background, W, H, game, cube_size, city_builded
    global font1, font2, stamina_max, stamina, money

    e_tap_to_relief = font2.render('press (e) to relief', True, (255, 0, 255))
    
    city_bg = transform.scale(image.load(city_background), (W, H))
    win.blit(city_bg, (0, 0))

    v_court = Settings(W-200, H-22-200, 200, 200, 0, volleyball_court)

    hero.rect.x = 300
    hero.rect.y = H - 22 - hero.height


    in_city = True
    while in_city and game:

        time.delay(15)


        for e in event.get():
            if e.type == QUIT:
                game = False


        win.blit(city_bg, (0, 0))
        v_court.reset()

        hero.r_l()

        hero.reset()


        if sprite.collide_rect(hero, v_court):
            win.blit(e_tap, (500, 50))

            keys = key.get_pressed()
            if keys[K_e]:
                if stamina < stamina_max:
                    money -= 30
                    stamina = stamina_max


        if hero.rect.x <= 10:
            in_city = False
            hero.rect.x = 7*cube_size
            hero.rect.y = 20



        money_text = font2.render("Money: " + str(money), True, (250, 235, 215))
        stamina_text = font2.render("Stamina: " + str(stamina), True, (250, 235, 215))
        
        win.blit(money_text, (20, 20))
        win.blit(stamina_text, (20, 80))


        display.update() 


















# створюємо вікно гри
W = 1280
H = 720
win = display.set_mode((W, H))

display.set_caption('Miner')



# додаємо текст в гру
font.init()

font1 = font.SysFont(('font/ariblk.ttf'), 200)


font2 = font.SysFont(('font/ariblk.ttf'), 60)
e_tap = font2.render('press (e)', True, (255, 0, 255))
k_need = font2.render('You need a key to open!', True, (255, 0, 255))
space = font2.render('press (space) to kill the enemy', True, (255, 0, 255))

font3 = font.SysFont(('font/calibrib.ttf'), 45)
wasd_b = font3.render('WASD - move buttons. You can only go up and down the stairs', True, (255, 0, 0))
space_b = font3.render('Space - shoot button. You are a wizard who only knows one spell', True, (255, 0, 0))
e_b = font3.render('E - interaction button. Open doors, collect keys, activate portals', True, (255, 0, 0))

font4 = font.SysFont(('font/ariblk.ttf'), 150)
done = font4.render('LEVEL DONE!', True, (0, 255, 0), (255, 100, 0))
lose = font4.render('YOU LOSE!', True, (255, 0, 0), (245, 222, 179))
pausa = font4.render('PAUSE', True, (255, 0, 0), (245, 222, 179))



# підвантажуємо картинки спрайтів

hero_image = "images/Шахтер в каске.png"
hero_image_l = "images/Шахтёр в каске_l.png"

ground = "images/Земля.png"
coal = "images/уголь.png"
iron = "images/Железо.png"
silver = "images/Серебро.png"
gold ="images/Золото.png"

ground_break = "images/Земля_ломается.png"
coal_break = "images/Уголь_ломается.png"
iron_break = "images/Железо_ломается.png"
silver_break = "images/Серебро_ломается.png"
gold_break = "images/Золото_ломается.png"




background = "images/Земля фон фулл.png"


volleyball_court = "images/Волейбольная площадка.png"

city_background = "images/Город.png"






items = sprite.Group()

coal_list = list()
iron_list = list()
silver_list = list()
gold_list = list()


# цикл, який малює рівень
x = y = 0
for line in level: # обираємо елемент зі списку level
    for c in line: # обираємо символ
        # якщо символ такий, замість нього промальовуємо таку картинку
        if c == "c": # Уголь
            r = Settings(x, y, cube_size, cube_size, 0, coal, coal_break)
            items.add(r)
            coal_list.append(r)
            r.HP = 3
        
        if c == "i": # Железо
            r = Settings(x, y, cube_size, cube_size, 0, iron, iron_break)
            items.add(r)
            iron_list.append(r)
            r.HP = 8

        if c == "s": # Серебро
            r = Settings(x, y, cube_size, cube_size, 0, silver, silver_break)
            items.add(r)
            silver_list.append(r)
            r.HP = 10
                
        if c == "g": # Золото
            r = Settings(x, y, cube_size, cube_size, 0, gold, gold_break)
            items.add(r)
            gold_list.append(r)
            r.HP = 20

        if c == " ":
            r = Settings(x, y, cube_size, cube_size, 0, ground, ground_break)
            items.add(r)

        x += cube_size # кожного разу зміщуємо малюнок на 40 ліворуч
    y += cube_size # вкінці, спускаємось на 1 ряд
    x = 0  # починаємо малювати спочатку  

    

    



hero = Player(7*cube_size, 20, 40, 60, 5, hero_image)
camera = Camera(camera_configure, level_width, level_hight)


bg = Settings(0, 0, level_width, level_hight, 0, background)

old_time = timer()#Используется для задержки между ударами кирки




game = True

#список соседних блоков
nearby = list()


money = 0
stamina = 30
stamina_max = 30

while game:
    

    time.delay(15)


    for e in event.get():
        if e.type == QUIT:
            game = False





    #Запоминаем координаты до перемещения героя
    hero_x = hero.rect.x 
    hero_y = hero.rect.y

    hero.move()
    




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




    nearby = list()
    
    camera.update(hero)
    win.blit(bg.image, camera.apply(bg))
    for r in items:
        win.blit(r.image, camera.apply(r))
        if abs(r.rect.x - hero.rect.x) < cube_size+30:
            if abs(r.rect.y - hero.rect.y) < cube_size+30:
                nearby.append(r)
        



        if r.HP <= 0:
            items.remove(r)

            if r in coal_list:
                coal_list.remove(r)
                money += 5
            if r in iron_list:
                iron_list.remove(r)
                money += 15
            if r in silver_list:
                silver_list.remove(r)
                money += 20
            if r in gold_list:
                gold_list.remove(r)
                money += 40


    
    if hero.rect.y <= 10:
        city()



        


    hero.dig()

        



    money_text = font2.render("Money: " + str(money), True, (250, 235, 215))
    stamina_text = font2.render("Stamina: " + str(stamina), True, (250, 235, 215))



    

    win.blit(hero.image, camera.apply(hero))
    win.blit(money_text, (20, 20))
    win.blit(stamina_text, (20, 80))


    
    display.update()