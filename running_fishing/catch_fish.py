import pygame
import random
import math
import pygame.locals as locals
import warehouse
from warehouse import *

pygame.init()


def final_time_update():
    global final_time
    final_time = game_time // 1000

#事件控制
def eventControl():
    global MONEY, pause, FLAG, ICE_COUNT, rank, dynamic_graph_falg, start_flag
    for event in pygame.event.get():
        if not pause:
            if event.type == pygame.locals.QUIT:
                exit()
            if event.type == locals.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                cannon.move(x, y)
            if start_flag:
                if event.type == pygame.locals.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0] == 1:
                        sound1 = pygame.mixer.Sound('./sound/Gunfire.wav')
                        sound1.set_volume(0.1)
                        sound1.play()
                        cannon.fire()
                        MONEY -= 2
        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_ESCAPE:
                exit()
            if event.key == pygame.locals.K_RETURN:
                if not start_flag:
                    start_flag = True

            if event.key == pygame.locals.K_SPACE:
                if MONEY > (rank + 1) ** 2 * 200:
                    print('K_SPACE', CannonBullet1.bullet_damage)
                    rank += 1
                    CannonBullet1.bullet_damage += rank
                    MONEY -= 200 * (rank * rank)
                    sound2 = pygame.mixer.Sound('./sound/change_cannon.wav')
                    sound2.set_volume(0.8)
                    sound2.play()
                    cannon_level_right.flag = True
                else:
                    cannon_level_error.flag = True

            if event.key == pygame.locals.K_p:
                if pause:
                    pause = False
                else:
                    pause = True

            if event.key == pygame.locals.K_f:
                if ICE_COUNT > 0:
                    # print(Fash.falg)
                    Fash.flag = False
                    FLAG = False
                    ICE_COUNT -= 1
                    ice_screen.flag = False
                else:
                    short_ice.flag = True
                # print(Fash.falg)
        if event.type == pygame.locals.MOUSEBUTTONUP:
            if pygame.mouse.get_pressed()[0] == 0:
                pass

# 更新美人鱼
def mermaid_update():
    global mermaid
    if mermaid.flag:
        # mermaid_group.add(Mermaid())
        # for mermaid in mermaid_group:
        mermaid.update()
        if mermaid.life <= 0 and mermaid.flag:
            # SOUND=====================================================================
            mermaid.flag = False
        elif mermaid.life > 0 and not mermaid.flag:
            mermaid.y = -200
            pass

#调用创造鱼群的方法
def fash_update():
    global MONEY, ICE_COUNT, fash_score01_flag, fash_score02_flag, fash_score03_flag, fash_score04_flag, fash_score05_flag, \
        fash_score06_flag, fash_score08_flag, fash_score09_flag, fash_score13_flag, fash_score14_flag, fash_score01, \
        fash_score02, fash_score03, fash_score04, fash_score05, fash_score06, fash_score08, fash_score09, \
        fash_score13, fash_score14, add_ice
    if Fash.flag:
        create_fash01()
        create_fash02()
        create_fash03()
        create_fash04()
        create_fash05()
        create_fash06()
        create_fash08()
        create_fash09()
        create_fash13()
        create_fash14()
    for fash in fash_group:
        if not fash.is_alive:

            fash_group.remove(fash)
            sound1 = pygame.mixer.Sound('./sound/coin.wav')
            sound1.set_volume(0.6)
            sound2 = pygame.mixer.Sound('./sound/coins.wav')
            sound2.set_volume(3.0)

            if 'Fash01' in str(fash) and fash.life <= 0:
                MONEY += fash.score * 3
                fash_score01 = DynamicGraph(font_name, '+ 3 ', GOLD, 40, fash.x, fash.y)
                # print(fash.x, fash.y)
                fash_score01_flag = True
                fash_score01.flag = True
                # print('fash1')
                # print(fash.score)
            if 'Fash02' in str(fash) and fash.life <= 0:
                MONEY += fash.score * 6
                fash_score02 = DynamicGraph(font_name, '+ 30', GOLD, 40, fash.x, fash.y)
                fash_score02_flag = True
                fash_score02.flag = True
                # print('fash2')
                # print(fash.score)
            if 'Fash03' in str(fash) and fash.life <= 0:
                MONEY += fash.score * 6
                fash_score03 = DynamicGraph(font_name, '+ 60', GOLD, 45, fash.x, fash.y)
                fash_score03_flag = True
                fash_score03.flag = True
                sound1.play()
                # print('fash3')
                # print(fash.score)
            if 'Fash04' in str(fash) and fash.life <= 0:
                MONEY += fash.score * 8
                fash_score04 = DynamicGraph(font_name, '+ 240', GOLD, 45, fash.x, fash.y)
                fash_score04_flag = True
                fash_score04.flag = True
                sound1.play()
                # print('fash4')
                # print(fash.score)
            if 'Fash05' in str(fash) and fash.life <= 0:
                MONEY += fash.score * 8
                fash_score05 = DynamicGraph(font_name, '+ 400', GOLD, 45, fash.x, fash.y)
                fash_score05_flag = True
                fash_score05.flag = True
                sound1.play()
                # print('fash5')
                # print(fash.score)
            if 'Fash06' in str(fash) and fash.life <= 0:
                MONEY += fash.score * 8
                fash_score06 = DynamicGraph(font_name, '+ 800', GOLD, 50, fash.x, fash.y)
                fash_score06_flag = True
                fash_score06.flag = True
                sound2.play()
                # print('fash6')
                # print(fash.score)
            if 'Fash08' in str(fash) and fash.life <= 0:
                MONEY += fash.score * 9
                fash_score08 = DynamicGraph(font_name, '+ 1800', GOLD, 50, fash.x, fash.y)
                fash_score08_flag = True
                fash_score08.flag = True
                sound2.play()
                # print('fash8')
                # print(fash.score)
            if 'Fash09' in str(fash) and fash.life <= 0:
                MONEY += fash.score * 10
                fash_score09 = DynamicGraph(font_name, '+ 3000', GOLD, 50, fash.x, fash.y)
                fash_score09_flag = True
                fash_score09.flag = True
                sound2.play()
                # print('fash9')
                # print(fash.score)
            if 'Fash13' in str(fash) and fash.life <= 0:
                MONEY += fash.score * 15
                ICE_COUNT += 1
                fash_score13 = DynamicGraph(font_name, '+ 4000', GOLD, 60, fash.x, fash.y)
                add_ice = DynamicLogo(fash.x, fash.y)
                add_ice.flag = True
                fash_score13_flag = True
                fash_score13.flag = True
                sound2.play()

                # print('fash13')
                # print(fash.score)
            if 'Fash14' in str(fash) and fash.life <= 0:
                MONEY += fash.score * 20
                ICE_COUNT += 1

                fash_score14 = DynamicGraph(font_name, '+ 5000', GOLD, 60, fash.x, fash.y)
                add_ice = DynamicLogo(fash.x, fash.y)
                add_ice.flag = True
                fash_score14_flag = True
                fash_score14.flag = True
                sound2.play()
                # print('fash14')
                # print(fash.score)
        else:
            fash.update()

# 子弹更新
def bullet_update():
    # print('can', cannon_bullet_group)
    for bullet in cannon_bullet_group1:

        if not bullet.is_alive:
            cannon_bullet_group1.remove(bullet)
        else:
            bullet.update()
    for bullet in cannon_bullet_group2:

        if not bullet.is_alive:
            cannon_bullet_group2.remove(bullet)
        else:
            bullet.update()

# 子弹碰撞到鱼
def crash_update():
    global mermaid
    for bullet in cannon_bullet_group1:
        for fash in fash_group:
            if bullet.is_crash(fash) and fash.life > 0:
                if bullet.flag:
                    fash.injured(bullet)
                bullet.flag = False
        if bullet.is_crash(mermaid) and mermaid.life > 0:
            if bullet.flag:
                mermaid.injured(bullet)
            bullet.flag = False

    for bullet in cannon_bullet_group2:
        for fash in fash_group:
            if bullet.is_crash(fash) and fash.life > 0:
                if bullet.flag:
                    fash.injured(bullet)
                bullet.flag = False
        if bullet.is_crash(mermaid) and mermaid.life > 0:
            if bullet.flag:
                mermaid.injured(bullet)
            bullet.flag = False

            # bullet.change_note()
            # bullet.is_alive = False
            # bullet.image=pygame.image.load()

#有规律动态创造鱼群
def create_fash01():
    global create_fash_time01
    if scene_num == 1:
        if count % create_fash_time01 == 0:
            create_fash_time01 = random.randint(30, 50)
            fash_group.add(Fash01())


def create_fash02():
    global create_fash_time02
    if scene_num == 1:
        if count % create_fash_time02 == 0:
            create_fash_time02 = random.randint(100, 140)
            fash_group.add(Fash02())
    elif scene_num == 2:
        pass
    else:
        create_fash_time02 = 45
        if count % create_fash_time02 == 0:
            create_fash_time02 = 45
            fash_group.add(Fash02())


def create_fash03():
    global create_fash_time03
    if scene_num == 1:
        if count % create_fash_time03 == 0:
            create_fash_time03 = random.randint(100, 200)
            fash_group.add(Fash03())
    elif scene_num == 2:
        pass
    else:
        create_fash_time03 = 55
        if count % create_fash_time03 == 0:
            create_fash_time03 = 55
            fash_group.add(Fash03())


def create_fash04():
    global create_fash_time04
    if scene_num == 1:
        if count % create_fash_time04 == 0:
            create_fash_time04 = random.randint(1000, 1250)
            fash_group.add(Fash04())


def create_fash05():
    global create_fash_time05
    if scene_num == 1:
        if count % create_fash_time05 == 0:
            create_fash_time05 = random.randint(1250, 1500)
            fash_group.add(Fash05())
    elif scene_num == 2:
        pass
    else:
        create_fash_time05 = 55
        if count % create_fash_time05 == 0:
            create_fash_time05 = 55
            fash_group.add(Fash05())


def create_fash06():
    global create_fash_time06
    if scene_num == 1:
        if count % create_fash_time06 == 0:
            create_fash_time06 = random.randint(1500, 1750)
            fash_group.add(Fash06())
    elif scene_num == 2:
        pass
    else:
        create_fash_time06 = 80
        if count % create_fash_time06 == 0:
            create_fash_time06 = 80
            fash_group.add(Fash06())


def create_fash08():
    global create_fash_time08
    if scene_num == 1:
        if count % create_fash_time08 == 0:
            create_fash_time08 = random.randint(1750, 2000)
            fash_group.add(Fash08())


def create_fash09():
    global create_fash_time09
    if scene_num == 1:
        if count % create_fash_time09 == 0:
            create_fash_time09 = random.randint(2000, 2500)
            fash_group.add(Fash09())


def create_fash13():
    global create_fash_time13
    if scene_num == 1:
        if count % create_fash_time13 == 0:
            create_fash_time13 = random.randint(2500, 3000)
            fash_group.add(Fash13())
    elif scene_num == 2:
        pass
    else:
        create_fash_time13 = 250
        if count % create_fash_time13 == 0:
            create_fash_time13 = 250
            fash_group.add(Fash13())


def create_fash14():
    global create_fash_time14
    if scene_num == 1:
        if count % create_fash_time14 == 0:
            create_fash_time14 = random.randint(3000, 4000)
            fash_group.add(Fash14())

# 动态更新
def update():
    global count, fash_score01, fash_score02, fash_score03, fash_score04, fash_score05, fash_score06, \
        fash_score08, fash_score09, fash_score13, fash_score14, final_time
    if start_flag:
        count += 1
        if count == 1000000000000000000000000:
            count = 0
        crash_update()
        # background1.update()
        # background2.update()
        if final_time % 70 <= 40:
            pass
        elif final_time % 70 <= 44:
            background.update()
        elif final_time % 70 < 70:
            pass

        cannon.update()

        bullet_update()

        fash_update()
        mermaid_update()
        final_time_update()
        cannon_level_right.update()
        cannon_level_error.update()
        short_ice.update()
        more_fash.update()
        ice_screen.update()

        if fash_score01_flag:
            fash_score01.update()
        if fash_score02_flag:
            fash_score02.update()
        if fash_score03_flag:
            fash_score03.update()
        if fash_score04_flag:
            fash_score04.update()
        if fash_score05_flag:
            fash_score05.update()
        if fash_score06_flag:
            fash_score06.update()
        if fash_score08_flag:
            fash_score08.update()
        if fash_score09_flag:
            fash_score09.update()
        if fash_score13_flag:
            add_ice.update()
            fash_score13.update()
        if fash_score14_flag:
            add_ice.update()
            fash_score14.update()

#显示文本
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_picture_money(img_path, size_x, size_y, x, y):
    img = pygame.image.load(img_path)
    image = pygame.transform.smoothscale(img, (size_x, size_y))
    screen.blit(image, (x, y))

# 显示图片信息
def draw_picture_canon(img_path, x, y):
    image = pygame.image.load(img_path)
    screen.blit(image, (x, y))

#调用绘画方法，动态展示各种效果
def draw():
    global fash_score01, fash_score02, fash_score3, fash_score04, fash_score05, fash_score06, fash_score08, \
        fash_score09, fash_score13, fash_score14, final_time, start_flag, scene_num, add_ice, mermaid
    if not start_flag:
        start_img = pygame.image.load("./image/main3.jpg")
        start_img = pygame.transform.smoothscale(start_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(start_img, (0, 0))
        sound1 = pygame.mixer.Sound('./sound/begin.wav')
        # sound1.play(1)
    if start_flag:
        if final_time % 70 <= 20:
            Fash01.rank_flag = True
            Fash02.rank_flag = True
            Fash03.rank_flag = True
            Fash04.rank_flag = True
            Fash05.rank_flag = True
            Fash06.rank_flag = True
            Fash08.rank_flag = True
            Fash09.rank_flag = True
            Fash13.rank_flag = True
            Fash14.rank_flag = True
            Fash.fash_x_speed = -1
            Fash.fash_flag = True
            scene_num = 1
            background.draw()
        elif final_time % 70 <= 30:
            Fash01.rank_flag = True
            Fash02.rank_flag = True
            Fash03.rank_flag = True
            Fash04.rank_flag = True
            Fash05.rank_flag = True
            Fash06.rank_flag = True
            Fash08.rank_flag = True
            Fash09.rank_flag = True
            Fash13.rank_flag = True
            Fash14.rank_flag = True
            Fash.fash_x_speed = -1
            Fash.fash_flag = True
            scene_num = 1
            background.draw()
            mermaid.flag = True  # 美人鱼出现（20-30）
        elif final_time % 70 <= 40:
            Fash01.rank_flag = True
            Fash02.rank_flag = True
            Fash03.rank_flag = True
            Fash04.rank_flag = True
            Fash05.rank_flag = True
            Fash06.rank_flag = True
            Fash08.rank_flag = True
            Fash09.rank_flag = True
            Fash13.rank_flag = True
            Fash14.rank_flag = True
            Fash.fash_x_speed = -1
            Fash.fash_flag = True
            scene_num = 1
            background.draw()
            mermaid.flag = False  # 美人鱼消失（>30)
        elif final_time % 70 <= 44:  # 大于40 不出现雨，提示鱼潮将要来临，超过43，鱼潮到来
            more_fash.flag = True
            Fash.fash_flag = False
            scene_num = 2
            # Fash.temp_count=0
            background.draw()
        elif final_time % 70 < 64:  # 超过63 鱼潮退去，
            Fash01.rank_flag = False
            Fash02.rank_flag = False
            Fash03.rank_flag = False
            Fash04.rank_flag = False
            Fash05.rank_flag = False
            Fash06.rank_flag = False
            Fash08.rank_flag = False
            Fash09.rank_flag = False
            Fash13.rank_flag = False
            Fash14.rank_flag = False
            Fash.fash_x_speed = -1
            Fash.fash_flag = True
            # Fash.temp_count==0
            scene_num = 0
            background.draw()
            sound3 = pygame.mixer.Sound('./sound/music1.wav')
            # sound3.play(-1)
        elif final_time % 70 < 70:
            scene_num = 2
            background.draw()

        cannon.draw()

        # cannon_bullet_group.draw(screen)
        for bullet in cannon_bullet_group1:
            bullet.draw()
        for bullet in cannon_bullet_group2:
            bullet.draw()
        fash_group.draw(screen)

        draw_text(screen, 'Time:' + str(final_time), 40, SCREEN_WIDTH - 400, 30)

        cannon_level_right.draw()
        cannon_level_error.draw()
        short_ice.draw()

        more_fash.draw()
        ice_screen.draw()
        if mermaid.flag:
            mermaid.draw()

        if fash_score01_flag:
            fash_score01.draw()

        if fash_score02_flag:
            fash_score02.draw()

        if fash_score03_flag:
            fash_score03.draw()
        if fash_score04_flag:
            fash_score04.draw()

        if fash_score05_flag:
            fash_score05.draw()

        if fash_score06_flag:
            fash_score06.draw()

        if fash_score08_flag:
            fash_score08.draw()

        if fash_score09_flag:
            fash_score09.draw()

        if fash_score13_flag:
            fash_score13.draw()
            add_ice.draw()
        if fash_score14_flag:
            fash_score14.draw()
            add_ice.draw()

        draw_picture_money('./image/money.png', 25, 25, SCREEN_WIDTH - 780, 30)
        draw_text(screen, str(MONEY), 40, SCREEN_WIDTH - 690, 30)
        draw_picture_money('./image/ice_logo.png', 25, 25, SCREEN_WIDTH - 780, 70)
        draw_text(screen, str(ICE_COUNT), 40, SCREEN_WIDTH - 690, 70)
        draw_picture_canon('./image/cannon3.png', SCREEN_WIDTH - 790, 100)
        draw_text(screen, str(rank), 40, SCREEN_WIDTH - 700, 110)


def init():
    # 定义全局变量
    global game_time, clock, pause, count, FLAG, ICE_COUNT, final_time, screen, background, \
        cannon, mermaid, rank, MONEY, fash_group, mermaid_group, cannon_bullet_group1, cannon_bullet_group2, \
        create_fash_time01, create_fash_time02, create_fash_time03, create_fash_time04, \
        create_fash_time05, create_fash_time06, create_fash_time08, create_fash_time09, \
        create_fash_time13, create_fash_time14, cannon_level_right, cannon_level_error, \
        short_ice, add_ice, scene_num, fash_score13, fash_score14, start_flag, ice_screen, more_fash
    # 设置窗口大小
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    warehouse.init(SCREEN_WIDTH, SCREEN_HEIGHT, rank, screen)
    game_time = 0

    clock = pygame.time.Clock() # 创建计时器
    background = Background()#创建背景
    # background1 = Background('./image/bg.jpg')
    # background2 = Background('./image/bg2.png')
    pygame.mixer.music.load('./sound/music1.wav')#背景音效
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.20)
    mermaid = Mermaid()#创建美人鱼
    # 子弹精灵
    cannon_bullet_group1 = pygame.sprite.Group()
    cannon = Cannon(cannon_bullet_group1)
    cannon_bullet_group2 = pygame.sprite.Group()
    cannon = Cannon(cannon_bullet_group2)
    # 设置文本
    cannon_level_right = DynamicGraph(font_name, 'Level +1', YELOOW, 45, 410, 400)
    cannon_level_error = DynamicGraph(font_name, 'Lack of Gold Coin', RED, 50, 400, 200)
    short_ice = DynamicGraph(font_name, 'Freezing Value Is Null ', RED, 50, 400, 70)
    # add_ice = DynamicGraph(font_name, 'Freezing Value +1 ', ORANGE, 45, 400, 70)
    more_fash = DynamicGraph(font_name, 'A FISH TIDE COMING ', YELOOW, 70, 400, 200)
    ice_screen = IceScreen()#全屏冰冻

    fash_group = pygame.sprite.Group()
    mermaid_group = pygame.sprite.Group()


def main():
    global game_time, pause
    init()
    while True:
        eventControl()
        if not pause:
            update()
            draw()
            pygame.display.update()
            print(clock.tick(FPS))
            if start_flag:
                game_time += clock.tick(FPS)


# ================全局变量，对外开放================
FPS = 50
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
LAND_HEIGHT = 400
SEA_HEIGHT = 200
FLAG = True
keys = [False, False, False, False]
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELOOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (218, 112, 214)
# ORANGE = (255, 165, 0)
# ORANGE2 = (238, 154, 0)
# ORANGE3 = (205, 133, 0)
ORANGE = (255, 52, 179)
ORANGE2 = (238, 48, 167)
ORANGE3 = (205, 41, 144)
GOLD = (255, 215, 0)
font_name = pygame.font.match_font('simsun.ttf')

# ================全局变量，对外开放================
game_time = 0
final_time = 0
count = 0
screen = None
clock = None
background = None
cannon = None
add_ice = None
short_ice = None
fash_score01 = None
fash_score13 = None
fash_score14 = None
cannon_bullet_group1 = None
cannon_bullet_group2 = None
fash_group = None
mermaid_group = None
rank = 1#炮弹等级
dynamic_graph_falg = False
fash_score01_flag = False
fash_score02_flag = False
fash_score03_flag = False
fash_score04_flag = False
fash_score05_flag = False
fash_score06_flag = False
fash_score08_flag = False
fash_score09_flag = False
fash_score13_flag = False
fash_score14_flag = False
pause = False
start_flag = False
MONEY = 10000#初始化分数
ICE_COUNT = 5#初始化冰冻技能个数
scene_num = 3
# 不同种类鱼的刷新时间
create_fash_time01 = int(random.randint(10, 70) / scene_num)
create_fash_time02 = int(random.randint(200, 400) / scene_num)
create_fash_time03 = int(random.randint(400, 1000) / scene_num)
create_fash_time04 = int(random.randint(1000, 1250) / scene_num)
create_fash_time05 = int(random.randint(1250, 1500) / scene_num)
create_fash_time06 = int(random.randint(1500, 1750) / scene_num)
create_fash_time08 = int(random.randint(1750, 2000) / scene_num)
create_fash_time09 = int(random.randint(2000, 2500) / scene_num)
create_fash_time13 = int(random.randint(2500, 3000) / scene_num)
create_fash_time14 = int(random.randint(3000, 4000) / scene_num)

if __name__ == '__main__':
    main()
