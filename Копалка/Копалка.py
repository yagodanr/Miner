from pygame import *
from random import shuffle
import math
from time import time as timer







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




#level = [
#    "c                    c  c      c",
#    "--------------------------------",
#    "ciciciciccicsssiisgsssgisis     ",
#    "ciciciciccicsssiisgsssgisisg    ",
#    "ciciciciccicsssiisgsssgisisgss  "]

# створюємо вікно гри
W = 1280
H = 720
win = display.set_mode((W, H))

display.set_caption('Miner')




# завантажуємо звуки
mixer.init()
money_in = mixer.Sound("sounds/Заработал денег.ogg")
money_out = mixer.Sound("sounds/Потратил деньги.ogg")

OST = mixer.Sound("sounds/Warframe - We All Lift Together.ogg")






# додаємо текст в гру
font.init()

font1 = font.SysFont(('font/ariblk.ttf'), 200)
gname = font1.render('ШАХТА', True, (250, 235, 215))

font2 = font.SysFont(('font/ariblk.ttf'), 60)
e_tap = font2.render('press (e)', True, (255, 0, 255))
hammer_lvl_text = font2.render('Молот', True, (255, 0, 255))
space = font2.render('press (space) to kill the enemy', True, (255, 0, 255))

font3 = font.SysFont(('font/calibrib.ttf'), 45)
wasd_b = font3.render('WASD - move buttons.', True, (255, 0, 0))
space_b = font3.render('ARROWS - dig buttons', True, (255, 0, 0))
e_b = font3.render('E - interaction button. Use it to have some rest at court', True, (255, 0, 0))


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
shop_bag = "images/На магазин.png"
shop_bg = "images/На окно магазина .png"
hammer = "images/Молоток на дамагу.png"
biceps = "images/Бицепс на выносливость2.png"
money_img = "images/Монетки.png"
cross = "images/Крестик.png"
buy_img = "images/Окно покупки.png"

city_background = "images/Город.png"






money = 45
stamina = 30
stamina_max = 30

stamina_lvl = 1
stamina_cost = 30

hammer_lvl = 1
hammer_cost = 100

money_lvl = 1
money_cost = 50

left = True

old_time = timer()#Используется для задержки между ударами кирки

#список соседних блоков
nearby = list()


bg = Settings(0, 0, W, H, 0, background)
nearby.append(bg)

game = True


    


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
        global cube_size, old_time, time_not_dig, stamina, hammer_lvl
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
                            r.HP -= hammer_lvl
                            stamina -= 1
                            if r.broken == False:
                                r.switch_image_to_broken()
                                r.broken = True
            if keys[K_LEFT]:
                if new_time-old_time >= time_not_dig:
                    old_time = timer()
                    for r in nearby:
                        if r.rect.x == column_of_objekt-cube_size and r.rect.y == line_of_objekt:
                            r.HP -= hammer_lvl
                            stamina -= 1
                            if r.broken == False:
                                r.switch_image_to_broken()
                                r.broken = True


            if keys[K_UP]:
                if new_time-old_time >= time_not_dig:
                    old_time = timer()
                    for r in nearby:
                        if r.rect.x == column_of_objekt and r.rect.y == line_of_objekt-cube_size:
                            r.HP -= hammer_lvl
                            stamina -= 1
                            if r.broken == False:
                                r.switch_image_to_broken()
                                r.broken = True
            if keys[K_DOWN]:
                if new_time-old_time >= time_not_dig:
                    old_time = timer()
                    for r in nearby:
                        if r.rect.x == column_of_objekt and r.rect.y == line_of_objekt+cube_size:
                            r.HP -= hammer_lvl
                            stamina -= 1
                            if r.broken == False:
                                r.switch_image_to_broken()
                                r.broken = True


class Button():
    def __init__(self, color, x, y, w, h, text, fsize, txt_color):

        self.width = w
        self.height = h
        self.color = color

        self.image = Surface([self.width, self.height])
        self.image.fill((color))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.fsize = fsize
        self.text = text
        self.txt_color = txt_color
        self.txt_image = font.Font('font/impact.ttf', fsize).render(text, True, txt_color)

    def draw(self, shift_x, shift_y): # цей метод малює кнопку із тектом в середині. Сам текст зміщенний на величини shift_x та shift_y
        win.blit(self.image, (self.rect.x, self.rect.y))
        win.blit(self.txt_image, (self.rect.x + shift_x, self.rect.y + shift_y))


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





# створюємо кнопки
btn_start = Button((178, 34, 34), 470, 300, 280, 70, 'START GAME', 50, (255, 255, 255))
btn_control = Button((178, 34, 34), 470, 450, 280, 70, 'HOW TO PLAY', 50, (255, 255, 255))
btn_exit = Button((178, 34, 34), 470, 600, 280, 70, 'EXIT GAME', 50, (255, 255, 255))
btn_menu = Button((178, 34, 34), 470, 600, 280, 70, 'BACK to MENU', 50, (255, 255, 255))
btn_restart = Button((178, 34, 34), 470, 450, 280, 70, 'RESTART', 50, (255, 255, 255))
btn_continue = Button((178, 34, 34), 470, 350, 280, 70, 'CONTINUE', 50, (255, 255, 255))
btn_pause = Button((178, 34, 34), 1200, 15, 50, 50, 'I I', 40, (255, 255, 255))




def menu(): # меню
    global font2, W, H, gname
    menu = True
    # фонова музика

    while menu:

        for e in event.get(): # закриваємо вікно гри
            if e.type == QUIT: 
                menu = False

        time.delay(15)
        pos_x, pos_y = mouse.get_pos() # де сховався вказівник?

        bg.reset()
        win.blit(gname, (350, 70))

        # відображення кнопок
        btn_start.draw(15, 5)
        btn_control.draw(10, 5)
        btn_exit.draw(37, 5)

        for e in event.get():
            # "Почати гру"
            if btn_start.rect.collidepoint((pos_x, pos_y)) and e.type == MOUSEBUTTONDOWN:
                #click.play()
                menu = False
                bg.reset()
                loading = font2.render("LOADING" , True, (236, 236, 35))
                win.blit(loading, (W-400, H-200))
                display.update()
                res_pos()
                lvl()
            # "Правила керування"
            if btn_control.rect.collidepoint((pos_x, pos_y)) and e.type == MOUSEBUTTONDOWN:
                #click.play()
                menu = False
                rules()
            # "Вихід з гри"
            if btn_exit.rect.collidepoint((pos_x, pos_y)) and e.type == MOUSEBUTTONDOWN:
                #click.play()
                menu = False
            # також вихід, але по натисканні на хрестик
            if e.type == QUIT:
                menu = False
        
        display.update()


def rules(): # правила

    rule = True

    while rule:

        for e in event.get(): # закриваємо вікно гри
            if e.type == QUIT: 
                rule = False

        time.delay(15)
        # відображення тексту з правилами керування
        bg.reset()
        win.blit(gname, (320, 70))
        win.blit(wasd_b, (50, 250))
        win.blit(space_b, (50, 350))
        win.blit(e_b, (50, 450))

        btn_menu.draw(0, 5)
        
        pos_x, pos_y = mouse.get_pos()

        for e in event.get():
            # повернення до меню
            if btn_menu.rect.collidepoint((pos_x, pos_y)) and e.type == MOUSEBUTTONDOWN:
                #click.play()
                rule = False
                menu()
            # закриваємо вікно
            if e.type == QUIT:
                rule = False

        display.update()










def city():
    global volleyball_court, city_background, W, H, game, cube_size, city_builded
    global font1, font2, font3, stamina_max, stamina, money, OST_start
    global hammer_lvl, hammer_cost, stamina_lvl, stamina_cost, money_lvl, money_cost
    global shop_bg, shop_bag, biceps, hammer, money_img, cross, buy_img

    e_tap_to_relief = font2.render('press (e) to relief', True, (255, 0, 255))
    
    
    city_bg = transform.scale(image.load(city_background), (W, H))
    win.blit(city_bg, (0, 0))   

    v_court = Settings(W-200, H-22-200, 200, 200, 0, volleyball_court)

    #shop
    shop_start = Settings(W-50, 0, 50, 50, 0, shop_bag)

    shop_back = Settings(0, 0, round((H-200)*0.798), H-200, 0, shop_bg) #730:915 = 0.798
    shop_back.rect.x = W - shop_back.width

    shop_stamina = Settings(0, 0+round((45*shop_back.width)/730), round((150*shop_back.width)/730), round((150*shop_back.width)/730), 0, biceps)#Вычисляем по пропорции     45:730=x:shop_back.width
    shop_stamina.rect.x = shop_back.rect.x+shop_stamina.rect.y
    shop_stamina.width = round((150*shop_back.width)/730)
    shop_stamina.height = round((150*shop_back.width)/730) #Опять пропорция
    buy_stamina = Settings(W-shop_stamina.rect.y - shop_stamina.width, shop_stamina.rect.y, shop_stamina.width, shop_stamina.height, 0, buy_img)


    shop_hammer = Settings(shop_stamina.rect.x, shop_stamina.rect.y + shop_stamina.height+20, shop_stamina.width, shop_stamina.height, 0, hammer)
    buy_hammer = Settings(W-shop_stamina.rect.y - shop_hammer.width, shop_hammer.rect.y, shop_hammer.width, shop_hammer.height, 0, buy_img)

    shop_money = Settings(shop_hammer.rect.x, shop_hammer.rect.y+shop_hammer.width, shop_hammer.width, shop_hammer.height, 0, money_img)
    buy_money = Settings(W-shop_stamina.rect.y - shop_hammer.width, shop_money.rect.y, shop_money.width, shop_money.height, 0, buy_img)

    shop_end = Settings(W-50, 0, 50, 50, 0, cross)


    hero.rect.x = 300
    hero.rect.y = H - 22 - hero.height


    in_city = True
    menu_shop = False
    while in_city and game:

        time.delay(15)

        pos_x, pos_y = mouse.get_pos() # де сховався вказівник?


        for e in event.get():
            if e.type == QUIT:
                game = False
            elif buy_hammer.rect.collidepoint((pos_x, pos_y)) and e.type == MOUSEBUTTONDOWN:
                if money >= hammer_cost:
                    hammer_lvl += 1
                    money -= hammer_cost
                    hammer_cost *= 3
                    money_out.play()

            elif buy_stamina.rect.collidepoint((pos_x, pos_y)) and e.type == MOUSEBUTTONDOWN:
                if money >= stamina_cost:
                    stamina_lvl += 1
                    stamina_max += 10
                    money -= stamina_cost
                    stamina_cost *= 2
                    money_out.play()

            elif buy_money.rect.collidepoint((pos_x, pos_y)) and e.type == MOUSEBUTTONDOWN:
                if money >= money_cost:
                    money_lvl += 1
                    money -= money_cost
                    money_cost *= 5
                    money_out.play()


            
            if menu_shop:
                if shop_end.rect.collidepoint((pos_x, pos_y)) and e.type == MOUSEBUTTONDOWN:
                    menu_shop = False
            else:
                if shop_start.rect.collidepoint((pos_x, pos_y)) and e.type == MOUSEBUTTONDOWN:
                    menu_shop = True



        OST_time = timer()

        if OST_time - OST_start >= 3*60+20:
            OST.stop()
            OST.play()
            OST_start = timer()



        win.blit(city_bg, (0, 0))
        v_court.reset()

        v_court_text = font2.render("REST COURT!" , True, (236, 236, 35))
        win.blit(v_court_text, (v_court.rect.x - 100, v_court.rect.y - 100))


        hero.r_l()

        hero.reset()


        if sprite.collide_rect(hero, v_court):
            win.blit(e_tap, (500, 50))

            keys = key.get_pressed()
            if keys[K_e]:
                if stamina < stamina_max:
                    money -= 30
                    stamina = stamina_max
                    money_out.play()


        if hero.rect.x <= 10:
            in_city = False
            hero.rect.x = 7*cube_size
            hero.rect.y = 20


        shop_start.reset()

        if menu_shop:
            shop_back.reset()

            shop_stamina.reset()
            buy_stamina.reset()


            stamina_lvl_text = font2.render('LVL: ' + str(stamina_lvl) , True, (236, 236, 35))
            win.blit(stamina_lvl_text, (shop_stamina.rect.x+shop_stamina.width+10, shop_stamina.rect.y))

            stamina_text = font3.render("+10ST" , True, (236, 236, 35))
            win.blit(stamina_text, (shop_stamina.rect.x+shop_stamina.width+10+20, shop_stamina.rect.y+45))

            stamina_cost_text = font2.render(str(stamina_cost) , True, (250, 235, 215))
            win.blit(stamina_cost_text, (buy_stamina.rect.x+15, buy_stamina.rect.y+25))



            shop_hammer.reset()
            buy_hammer.reset()

            hammer_lvl_text = font2.render('LVL: ' + str(hammer_lvl) , True, (236, 236, 35))
            win.blit(hammer_lvl_text, (shop_hammer.rect.x+shop_hammer.width+10, shop_hammer.rect.y))

            hammer_text = font3.render("+1Dig" , True, (236, 236, 35))
            win.blit(hammer_text, (shop_hammer.rect.x+shop_hammer.width+10+20, shop_hammer.rect.y+45))

            hammer_cost_text = font2.render(str(hammer_cost) , True, (250, 235, 215))
            win.blit(hammer_cost_text, (buy_hammer.rect.x+15, buy_hammer.rect.y+25))



            shop_money.reset()
            buy_money.reset()

            money_lvl_text = font2.render('LVL: ' + str(money_lvl) , True, (236, 236, 35))
            win.blit(money_lvl_text, (shop_money.rect.x+shop_money.width+10, shop_money.rect.y))

            money_text = font3.render("x2 ore cost" , True, (236, 236, 35))
            win.blit(money_text, (shop_money.rect.x+shop_money.width, shop_money.rect.y+45))

            money_cost_text = font2.render(str(money_cost) , True, (250, 235, 215))
            win.blit(money_cost_text, (buy_money.rect.x+15, buy_money.rect.y+25))



            shop_end.reset()

        else:
            shop_start.reset()



        money_text = font2.render("Money: " + str(money), True, (250, 235, 215))
        if stamina <= 1:
            stamina_text = font2.render("GO TO THE COURT!", True, (250, 0, 0))
        else:
            stamina_text = font2.render("Stamina: " + str(stamina), True, (250, 235, 215))
        

        




        win.blit(money_text, (20, 20))
        win.blit(stamina_text, (20, 80))
        


        display.update()














def res_pos():
    global coal, coal_break, iron, iron_break, silver, silver_break, gold, gold_break, ground, ground_break
    global cube_size, level_width, level_hight, time_not_dig
    global items, coal_list, iron_list, silver_list, gold_list
    global hero, camera, bg
    global hero_image, background
    
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



def lvl():
    global money, stamina, stamina_max, stamina_lvl, stamina_cost
    global hammer_lvl, hammer_cost, money_lvl, money_cost
    global left, nearby, game, OST_start

    
    OST.play()
    OST_start = timer()

    while game:
        

        time.delay(15)


        for e in event.get():
            if e.type == QUIT:
                game = False





        #Запоминаем координаты до перемещения героя
        hero_x = hero.rect.x 
        hero_y = hero.rect.y
        OST_time = timer()

        hero.move()
        


        if OST_time - OST_start >= 3*60+20:
            OST.stop()
            OST.play()
            OST_start = timer()



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
                money_in.play()
                if r in coal_list:
                    coal_list.remove(r)
                    money += 5*math.pow(2, money_lvl-1)
                if r in iron_list:
                    iron_list.remove(r)
                    money += 15*math.pow(2, money_lvl-1)
                if r in silver_list:
                    silver_list.remove(r)
                    money += 20*math.pow(2, money_lvl-1)
                if r in gold_list:
                    gold_list.remove(r)
                    money += 40*math.pow(2, money_lvl-1)


        
        if hero.rect.y <= 10:
            city()



            


        hero.dig()

            



        money_text = font2.render("Money: " + str(money), True, (250, 235, 215))
        if stamina <= 1:
            stamina_text = font2.render("GO UP!", True, (250, 0, 0))
        else:
            stamina_text = font2.render("Stamina: " + str(stamina), True, (250, 235, 215))





        

        win.blit(hero.image, camera.apply(hero))
        win.blit(money_text, (20, 20))
        win.blit(stamina_text, (20, 80))


        
        display.update()
     

menu()