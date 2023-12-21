import pygame
import pgzrun
import random
#розмір вікна
WIDTH = 800
HEIGHT = 800
#кути повороту
UP = 180
DOWN = 0
LEFT = 270
RIGHT = 90
#швидкість кулі
BULLET_SPEED = 30
#спрайти
pacman = Actor("heroi")
bg = Actor("fon")
bullet = Actor("bullet2")
#чи вистрелена куля
bullet_fired = False 
# здоровя
HP = 1000 
# позиція ГГ на екрані
pacman.pos = 250, 250 
#вороги та їх швидкість
zombie_list = [] 
ZOMBIE_SPEED = 1 
#очки
score = 0
#чи завершена гра
game_over = False 
#їжа1
apple = Actor("salo")
x = random.randint(10, 490)
y = random.randint(10, 490)
apple.pos = x, y

#їжа2
mouse = Actor("borsh")
x1 = random.randint(10, 490)
y1 = random.randint(10, 490)
mouse.pos = x1, y1
#напрямок ГГ
direction = "down" 
#змінна-лічильник
i = 0

def draw():
    #простір екрану = наша гра, повноекранний режим.
    screen.surface = pygame.display.set_mode((500, 500), pygame.FULLSCREEN)
#відмальовка спрайтів якщо не кінець гри
    if not game_over:
        screen.clear()
        bg.draw()
        pacman.draw()
        apple.draw()
        mouse.draw()
        bullet.draw()
        clock.schedule(shoot_bullet, 1) # таймер який кожний кадр запускає механіку пострілу - def shoot_bullet

        clock.schedule(create_zombies, 5) #запуск по таймеру механіки виклику зомбі - def create_zombies 
        move_zombie() # механіка переміщення зомбі, типу найпростіший AІ ))
        screen.draw.text(f"score: {score} ", (10, 10)) # кількість очок
        screen.draw.text(f"health: {HP} ", (10, 30)) # кількість од здоров*я
# якщо гру завершено то відмальовуємо екран з повідомленням про це та рахунком.
    else:
        screen.fill("blue")
        screen.draw.text(f"GAME OVER, Your score: {score} vbitih rusachkov", (250, 250))
        screen.draw.text(f"UKRMAN - the game", (250, 400))
        screen.draw.text(f"Created by Witch_ka & Arina.", (150, 470))


def update():
    global bullet_fired
    global direction
    global HP
    #програмуємо клавіші
    if keyboard.a:
        direction = "left"

        pacman.angle = LEFT
    elif keyboard.d:
        direction = "right"
        pacman.angle = RIGHT
    elif keyboard.w:
        direction = "up"
        pacman.angle = UP
    elif keyboard.s:
        direction = "down"
        pacman.angle = DOWN

    global game
#програмуємо переміщення ГГ по екрану
    if direction == "right":
        pacman.x += 2
    elif direction == "left":
        pacman.x -= 2
    elif direction == "up":
        pacman.y -= 2
    elif direction == "down":
        pacman.y += 2
    #програмуємо натискання на пробіл і відмальовку випущеної ГГ кулі перед ним а не по центру його спрайту
    if keyboard.space:
        if not bullet_fired:
            bullet_fired = True
            sounds.shoot.play() #програвання звуку пострілу
            if pacman.angle == LEFT:
                bullet.x = pacman.x - 30
                bullet.y = pacman.y
            elif pacman.angle == RIGHT:
                bullet.x = pacman.x + 30
                bullet.y = pacman.y
            elif pacman.angle == DOWN:
                bullet.x = pacman.x
                bullet.y = pacman.y + 30
            elif pacman.angle == UP:
                bullet.x = pacman.x
                bullet.y = pacman.y - 30
    #механіка поїдання їжі1 та підняття 1од здоровя внаслідок поїдання
    if apple.colliderect(pacman):
        x = random.randint(10, 490)
        y = random.randint(10, 490)
        HP+=1
        apple.pos = x, y
        sounds.splat.play()
    #механіка поїдання їжі2 та підняття 10од здоровя внаслідок поїдання
    elif mouse.colliderect(pacman):
        x1 = random.randint(10, 490)
        y1 = random.randint(10, 490)
        HP+=10
        mouse.pos = x1, y1
        sounds.splat.play() #програвання звуку поїдання їжі

#механіка польоту кулі після пострілу
def shoot_bullet():
    global bullet_fired
    global pacman
    global bullet
    if bullet_fired:
        if pacman.angle == LEFT:
            bullet.x -= BULLET_SPEED
        elif pacman.angle == RIGHT:
            bullet.x += BULLET_SPEED
        elif pacman.angle == DOWN:
            bullet.y += BULLET_SPEED
        elif pacman.angle == UP:
            bullet.y -= BULLET_SPEED
        #якщо куля залетіла за екран то не відмальовуємо її
        if bullet.x >= WIDTH or bullet.x <= 0 or bullet.y >= HEIGHT or bullet.y <= 0:
            bullet_fired = False

#механіка створення зомбі
def create_zombies():
    if len(zombie_list) < 8: #кількість зомбі
        loc_rand = random.randint(0, 3) #випадкова локація для кожного наступного зомбі (верх,низ,ліво,право)
        if loc_rand == 0: 
            y = random.randint(40, HEIGHT - 40)
            z = Actor("borog.png")
            z.x = 1
            z.y = y
            zombie_list.append(z)
        elif loc_rand == 1:
            y = random.randint(40, HEIGHT - 40)
            z = Actor("borog.png")
            z.x = WIDTH - 1
            z.y = y
            zombie_list.append(z)
        elif loc_rand == 2:
            x = random.randint(40, WIDTH - 40)
            z = Actor("borog.png")
            z.y = 1
            z.x = x
            zombie_list.append(z)
        elif loc_rand == 3:
            x = random.randint(40, WIDTH - 40)
            z = Actor("borog.png")
            z.y = HEIGHT - 1
            z.x = x
            zombie_list.append(z)

#механіка руху зомбі в напрямку ГГ
def move_zombie():
    global score, game_over, HP
    for zomb in zombie_list:
        if zomb.x < pacman.x:
            zomb.x += ZOMBIE_SPEED
        elif zomb.x > pacman.x:
            zomb.x -= ZOMBIE_SPEED
        elif zomb.y < pacman.y:
            zomb.y += ZOMBIE_SPEED
        elif zomb.y > pacman.y:
            zomb.y -= ZOMBIE_SPEED
#відмальовка стеку зомбі
        for zomb in zombie_list:
            zomb.draw()
            if zomb.colliderect(bullet): #якщо куля зіштовхнеться з зомбі
                zombie_list.remove(zomb) #видаляємо його (координати) зі списку
                score += 1 #набір очків при пересіченні спрайтів кулі та зомбі (попаданні кулі в зомбі)
            if zomb.colliderect(pacman): #якщо ГГ зіштовхнеться з зомбі
                HP-=1 #кожен відмальований кадр з пересіченням ГГ і зомбі зменшуємо здоровя ГГ на 1од
            if zomb.colliderect(pacman) and HP == 0 : #коли пересічення з зомбі та здоровя ГГ 0од - гру завершено
                    game_over = True
