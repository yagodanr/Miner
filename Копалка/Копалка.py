from pygame import *
from random import shuffle







level = [
       "c                    c                        c                      c",
       "                                                                 ccccc",
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
    del text_list
    text_list = list()




level_width = len(level[0])*40
level_hight = len(level)*40

# створюємо вікно гри
W = 1280
H = 720
win = display.set_mode((W, H))
bg = transform.scale(image.load("images/Земля фон.png"), (W, H))
display.set_caption('Miner')

# додаємо текст в гру
font.init()

font1 = font.SysFont(('font/ariblk.ttf'), 200)
gname = font1.render('Blockada', True, (106, 90, 205), (250, 235, 215))

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

hero_image = "images/Шахтер.png"

ground = "images/Земля.png"
coal = "images/уголь.png"
iron = "images/Железо.png"
silver = "images/Серебро.png"
gold ="images/Золото.png"

win.blit(bg, (0, 0)) # задній фон



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
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player(Settings):
    def r_l(self):
        global hero_image, left, level_width
        keys = key.get_pressed()
        if keys[K_d]:
            if self.rect.x < level_width-20:
                self.rect.x += self.speed
                if left == False:
                    left = True
        if keys[K_a]:
            if self.rect.x > 20:
                self.rect.x -= self.speed
                if left:
                    left = False
    def u_d(self):
        global level_hight
        keys = key.get_pressed()
        if keys[K_s]:
            if self.rect.y < level_hight-50:
                self.rect.y += self.speed
        if keys[K_w]:
            if self.rect.y > 50:
                self.rect.y -= self.speed

    def move(self):
        self.r_l()
        self.u_d()

class Camera():
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)


    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def camera_configure(camera, target_rect):
    l, t, w_t, h_t = target_rect
    _, _, w, h = camera
    l, t = -l + W/2, -t + H/2

    l = min(0, l)
    l = max(-(camera.width-W), l)
    t = max(-(camera.height-H), t)
    t = min(0, t)

    return Rect(l, t, w, h)
    

    

hero = Player(300, 500, 50, 50, 5, hero_image)
camera = Camera(camera_configure, level_width, level_hight)



items = sprite.Group()


# цикл, який малює рівень
x = y = 0
for line in level: # обираємо елемент зі списку level
    for c in line: # обираємо символ
        # якщо символ такий, замість нього промальовуємо таку картинку
        if c == "c": # Уголь
            r = Settings(x, y, 40, 40, 0, coal)
            items.add(r)
        
        if c == "i": # Железо
            r = Settings(x, y, 40, 40, 0, iron)
            items.add(r)

        if c == "s": # Серебро
            r = Settings(x, y, 40, 40, 0, silver)
            items.add(r)
                
        if c == "g": # Золото
            r = Settings(x, y, 40, 40, 0, gold)
            items.add(r)

        x += 40 # кожного разу зміщуємо малюнок на 40 ліворуч
    y+= 40 # вкінці, спускаємось на 1 ряд
    x = 0  # починаємо малювати спочатку  






game = True

while game:
    

    time.delay(15)
    win.blit(bg, (0, 0)) # задній фон


    for e in event.get():
        if e.type == QUIT:
            game = False

    hero.move()
    


    camera.update(hero)
    for r in items:
        win.blit(r.image, camera.apply(r))

    win.blit(hero.image, camera.apply(hero))


    display.update()