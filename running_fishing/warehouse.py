import pygame
import math
import random

SCREEN_HEIGHT = None
SCREEN_WIDTH = None
LAND_HEIGHT = None
SEA_HEIGHT = None
SCREEN = None


def init(screen_width, screen_height, rank, screen):
    global SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN
    SCREEN_HEIGHT = screen_height
    SCREEN_WIDTH = screen_width
    SCREEN = screen
# 背景类
class Background(object):
    def __init__(self):
        self.img = pygame.image.load('./image/bg.jpg')
        self.img1 = pygame.image.load('./image/bg2.png')
        self.img1 = pygame.transform.smoothscale(self.img1,(800,480))#改变图片大小
        self.x1 = 0
        self.x2 = SCREEN_WIDTH
    def update(self):
        self.x1 -= 4
        self.x2 -= 4
        if self.x1 <= -SCREEN_WIDTH:
            self.x1 = SCREEN_WIDTH
        if self.x2 <= -SCREEN_WIDTH:
            self.x2 = SCREEN_WIDTH

    def draw(self):
        SCREEN.blit(self.img, (self.x1, 0))
        SCREEN.blit(self.img1, (self.x2, 0))

 
class GameObject(object):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.is_alive = True

    def paly(self):
        pass

    def draw(self):
        SCREEN.blit(self.image,
                    (self.x - self.width / 2, self.y - self.height / 2))
    #判断碰撞，碰撞返回真，否则返回假
    def is_crash(self, other):
        if self.x - self.width / 2 < other.x + other.width / 2 \
                and self.x + self.width / 2 > other.x - other.width / 2 \
                and self.y - self.height / 2 < other.y + other.height / 2 \
                and self.y + self.height / 2 > other.y - other.height / 2:
            return True
        return False

#定义大炮类，继承GameObject
class Cannon(GameObject):
    def __init__(self, bullet_group):
        self.img = pygame.image.load('./image/cannon.png')
        super().__init__(self.img, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100)
        self.position = None
        self.rotate_playerpos = None
        self.rotate_img = None
        self.bullet_group = bullet_group
        self.count = 0

    def move(self, x, y):
        self.move_x = x
        self.move_y = y

    def fire(self):
        self.bullet_group.add(CannonBullet1(self.x, self.y - self.height / 2))
        self.bullet_group.add(CannonBullet2(self.x, self.y - self.height / 2))

    def update(self):
        self.rotate()
    # 大炮旋转
    def rotate(self):
        angle = math.atan2(self.move_y - (self.y + 36), self.move_x - (self.x + 50))
        self.rotate_img = pygame.transform.rotate(self.img, 265 - angle * 57.29)
        self.rotate_playerpos = \
            (self.x - self.rotate_img.get_rect().width / 2,
             self.y * 1.36 - self.rotate_img.get_rect().height / 2)

    def draw(self):
        SCREEN.blit(self.rotate_img, self.rotate_playerpos)

# 定义子弹类，继承精灵类，和GameObject
class Bullet(pygame.sprite.Sprite, GameObject):
    def __init__(self, image, x, y, damage):
        pygame.sprite.Sprite.__init__(self)
        GameObject.__init__(self, image, x, y)
        self.damage = damage
        self.flag = True
        self.count = 0
        self.net09_image = []
        self.net_images(self.net09_image)
        self.net_count = 0
        self.net_index = 0
        self.net_falg = True
        a, b = pygame.mouse.get_pos()
        self.angle = math.atan2(b - (430 + 32), a - (365 + 26))
        self.speed_y = (math.sin(self.angle)) * 25
        self.speed_x = (math.cos(self.angle)) * 25

    def net_images(self, net09_image):
        image = pygame.image.load('./image/net.png')
        # net_image1 = pygame.transform.smoothscale(image, (120, 120))
        # net_image2 = pygame.transform.smoothscale(image, (110, 110))
        # net_image3 = pygame.transform.smoothscale(image, (90, 90))
        # net_image4 = pygame.transform.smoothscale(image, (80, 80))
        net_image1 = pygame.transform.smoothscale(image, (80, 80))
        net09_image.append(net_image1)
        net09_image.append(net_image1)
        net09_image.append(net_image1)
        net09_image.append(net_image1)
        net09_image.append(net_image1)

    def update(self, *args):
        #没有碰撞到鱼，子弹移动，
        if self.flag:
            self.x += self.speed_x
            self.y += self.speed_y
        else:
            self.change_note()#遍历net09_image，遍历结束，子弹类的is_alive为False

        self.rect = (self.x - self.width / 2, self.y - self.height / 2)

        if self.x - self.width / 2 > SCREEN_WIDTH \
                or self.x + self.width / 2 < 0 \
                or self.y - self.height / 2 > SCREEN_HEIGHT \
                or self.y + self.height / 2 < 0:
            self.is_alive = False

    def is_crash(self, other):
        if self.x - self.width / 2 < other.x + other.width / 2 \
                and self.x + self.width / 2 > other.x - other.width / 2 \
                and self.y - self.height / 2 < other.y + other.height / 2 \
                and self.y + self.height / 2 > other.y - other.height / 2:
            if self.net_falg:
                # print('self.x,self.y', self.x, self.y)
                # print('other.x,other.y', other.x, other.y)
                self.x = self.x - self.speed_x
                self.y = self.y + self.speed_y * 2
                self.net_falg = False

            return True
        return False

    def change_note(self):
        self.net_count += 1
        if self.net_count % 5 == 0:
            self.net_index += 1
        if self.net_index >= len(self.net09_image):
            self.is_alive = False
        else:
            self.image = self.net09_image[self.net_index]

    def draw(self):
        arrow1 = pygame.transform.rotate(self.image, 270 - self.angle * 57.29)
        SCREEN.blit(arrow1, (self.x, self.y))

# 定义子弹1
class CannonBullet1(Bullet):
    bullet_damage = 1

    def __init__(self, x, y):
        image = pygame.image.load('./image/bullet01.png')
        super().__init__(image, 400, 430, CannonBullet1.bullet_damage)

# 定义子弹2
class CannonBullet2(Bullet):
    def __init__(self, x, y):
        image = pygame.image.load('./image/bullet01.png')
        super().__init__(image, 360, 430, CannonBullet1.bullet_damage)

# 定义鱼类，继承精灵类，和GameObject
class Fash(pygame.sprite.Sprite, GameObject):
    flag = True
    flag_count = 5000
    fash_x_speed = -1.9
    fash_flag = True
    temp_speed = 0
    temp_count = 0

    def __init__(self, image, run_images, dead_images, x, y, x_speed, y_speed, life):
        pygame.sprite.Sprite.__init__(self)
        GameObject.__init__(self, image, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
        Fash.temp_speed = self.x_speed
        self.life = life
        self.score = life

        self.run_images = run_images
        self.dead_images = dead_images

        self.index = 0
        self.count = 0
        self.move_x = -1
        self.move_y = -1
        self.need_move = True
        self.image_count = 0
        self.image_index = 0

        self.dead_count = 0
        self.dead_index = 0

    def update(self, *args):
        if self.life > 0:
            self.run_image_play()
        else:
            self.dead_image_paly()

        self.rect = (self.x - self.width / 2, self.y - self.height / 2)
        if not Fash.fash_flag:
            if Fash.temp_count == 0:
                Fash.temp_speed = self.x_speed
                Fash.temp_count += 1
            self.x_speed = -5
        else:
            self.x_speed = Fash.temp_speed

        if self.x - self.width / 2 > SCREEN_WIDTH \
                or self.x + self.width / 2 < 0:
            self.is_alive = False

    def run_image_play(self):
        if Fash.flag:
            self.x += self.x_speed
            self.y += self.y_speed
            self.image_count += 1
            if self.image_count % 8 == 0:
                self.image_index += 1
            if self.image_index >= len(self.run_images):
                self.image_index = 0
            self.image = self.run_images[self.image_index]
        if not Fash.flag:
            # print('111111111', Fash.falg_count,Fash.falg)
            Fash.flag_count -= 1
        if Fash.flag_count <= 0:
            print('2222222222')
            Fash.flag = True
            Fash.flag_count = 5000

    def dead_image_paly(self):
        self.dead_count += 1
        if self.dead_count % 5 == 0:
            self.dead_index += 1
        if self.dead_index >= len(self.dead_images):
            self.is_alive = False
        else:
            self.image = self.dead_images[self.dead_index]

    def injured(self, bullet):
        if random.randint(0, 1):
            sound = pygame.mixer.Sound('./sound/hit_target.wav')
            sound.set_volume(0.33)
            sound.play()
            self.life -= bullet.damage

# 定义Fash01
class Fash01(Fash):
    index = 0,
    count = 0
    rank_flag = True

    def __init__(self):
        y = random.randint(15, 430)
        x_speed = Fash.fash_x_speed - 1.8
        run_images = []
        dead_images = []
        self.load_images(run_images)
        self.dead_images(dead_images)
        image = run_images[0]
        if Fash01.rank_flag:

            super().__init__(image, run_images, dead_images, SCREEN_WIDTH, y, x_speed, 0, 1)
        else:
            pass

    def load_images(self, run_images):
        run_images.append(pygame.image.load('./image/fish01_00.png'))
        run_images.append(pygame.image.load('./image/fish01_01.png'))
        run_images.append(pygame.image.load('./image/fish01_02.png'))
        run_images.append(pygame.image.load('./image/fish01_03.png'))
        run_images.append(pygame.image.load('./image/fish01_04.png'))
        run_images.append(pygame.image.load('./image/fish01_05.png'))
        run_images.append(pygame.image.load('./image/fish01_06.png'))
        run_images.append(pygame.image.load('./image/fish01_07.png'))
        run_images.append(pygame.image.load('./image/fish01_08.png'))
        run_images.append(pygame.image.load('./image/fish01_09.png'))

    def dead_images(self, d_images):
        d_images.append(pygame.image.load('./image/fish01_catch_01.png'))
        d_images.append(pygame.image.load('./image/fish01_catch_02.png'))


class Fash02(Fash):
    index = 0,
    count = 0
    rank_flag = True

    def __init__(self):
        y = random.randint(30, 420)
        x_speed = Fash.fash_x_speed - 1
        run_images = []
        dead_images = []
        self.load_images(run_images)
        self.dead_images(dead_images)
        image = run_images[0]
        if Fash02.rank_flag:

            super().__init__(image, run_images, dead_images, SCREEN_WIDTH, y, x_speed, 0, 5)
        else:
            super().__init__(image, run_images, dead_images, SCREEN_WIDTH, 380, x_speed, 0, 5)

    def load_images(self, run_images):
        run_images.append(pygame.image.load('./image/fish02_00.png'))
        run_images.append(pygame.image.load('./image/fish02_01.png'))
        run_images.append(pygame.image.load('./image/fish02_02.png'))
        run_images.append(pygame.image.load('./image/fish02_03.png'))
        run_images.append(pygame.image.load('./image/fish02_04.png'))
        run_images.append(pygame.image.load('./image/fish02_05.png'))
        run_images.append(pygame.image.load('./image/fish02_06.png'))
        run_images.append(pygame.image.load('./image/fish02_07.png'))
        run_images.append(pygame.image.load('./image/fish02_08.png'))
        run_images.append(pygame.image.load('./image/fish02_09.png'))

    def dead_images(self, d_images):
        d_images.append(pygame.image.load('./image/fish02_catch_01.png'))
        d_images.append(pygame.image.load('./image/fish02_catch_02.png'))


class Fash03(Fash):
    index = 0,
    count = 0
    rank_flag = True

    def __init__(self):
        y = random.randint(30, 420)
        x_speed = Fash.fash_x_speed - 1
        run_images = []
        dead_images = []
        self.load_images(run_images)
        self.dead_images(dead_images)
        image = run_images[0]
        if Fash03.rank_flag:

            super().__init__(image, run_images, dead_images, SCREEN_WIDTH, y, x_speed, 0, 10)
        else:
            super().__init__(image, run_images, dead_images, SCREEN_WIDTH, 50, x_speed, 0, 10)

    def load_images(self, run_images):
        run_images.append(pygame.image.load('./image/fish03_00.png'))
        run_images.append(pygame.image.load('./image/fish03_01.png'))
        run_images.append(pygame.image.load('./image/fish03_02.png'))
        run_images.append(pygame.image.load('./image/fish03_03.png'))
        run_images.append(pygame.image.load('./image/fish03_04.png'))
        run_images.append(pygame.image.load('./image/fish03_05.png'))
        run_images.append(pygame.image.load('./image/fish03_06.png'))
        run_images.append(pygame.image.load('./image/fish03_07.png'))
        run_images.append(pygame.image.load('./image/fish03_08.png'))
        run_images.append(pygame.image.load('./image/fish03_09.png'))

    def dead_images(self, d_images):
        d_images.append(pygame.image.load('./image/fish03_catch_01.png'))
        d_images.append(pygame.image.load('./image/fish03_catch_02.png'))


class Fash04(Fash):
    index = 0
    count = 0
    rank_flag = True

    def __init__(self):
        y = random.randint(30, 420)
        x_speed = Fash.fash_x_speed - 1
        run_images = []
        dead_images = []
        self.load_images(run_images)
        self.dead_images(dead_images)
        image = run_images[0]
        if Fash04.rank_flag:
            super().__init__(image, run_images, dead_images, SCREEN_WIDTH, y, x_speed, 0, 30)
        else:
            pass

    def load_images(self, run_images):
        run_images.append(pygame.image.load('./image/fish04_00.png'))
        run_images.append(pygame.image.load('./image/fish04_01.png'))
        run_images.append(pygame.image.load('./image/fish04_02.png'))
        run_images.append(pygame.image.load('./image/fish04_03.png'))
        run_images.append(pygame.image.load('./image/fish04_04.png'))
        run_images.append(pygame.image.load('./image/fish04_05.png'))
        run_images.append(pygame.image.load('./image/fish04_06.png'))
        run_images.append(pygame.image.load('./image/fish04_07.png'))
        run_images.append(pygame.image.load('./image/fish04_08.png'))
        run_images.append(pygame.image.load('./image/fish04_09.png'))

    def dead_images(self, d_images):
        d_images.append(pygame.image.load('./image/fish04_catch_01.png'))
        d_images.append(pygame.image.load('./image/fish04_catch_02.png'))


class Fash05(Fash):
    index = 0
    count = 0
    rank_flag = True

    def __init__(self):
        y = random.randint(30, 420)
        x_speed = Fash.fash_x_speed - 0.5
        run_images = []
        dead_images = []
        self.load_images(run_images)
        self.dead_images(dead_images)
        image = run_images[0]
        if Fash05.rank_flag:

            super().__init__(image, run_images, dead_images, SCREEN_WIDTH, y, x_speed, 0, 50)
        else:
            super().__init__(image, run_images, dead_images, SCREEN_WIDTH, 130, x_speed, 0, 50)

    def load_images(self, run_images):
        run_images.append(pygame.image.load('./image/fish05_00.png'))
        run_images.append(pygame.image.load('./image/fish05_01.png'))
        run_images.append(pygame.image.load('./image/fish05_02.png'))
        run_images.append(pygame.image.load('./image/fish05_03.png'))
        run_images.append(pygame.image.load('./image/fish05_04.png'))
        run_images.append(pygame.image.load('./image/fish05_05.png'))
        run_images.append(pygame.image.load('./image/fish05_06.png'))
        run_images.append(pygame.image.load('./image/fish05_07.png'))
        run_images.append(pygame.image.load('./image/fish05_08.png'))
        run_images.append(pygame.image.load('./image/fish05_09.png'))

    def dead_images(self, d_images):
        d_images.append(pygame.image.load('./image/fish05_catch_01.png'))
        d_images.append(pygame.image.load('./image/fish05_catch_02.png'))


class Fash06(Fash):
    index = 0,
    count = 0
    rank_flag = True

    def __init__(self):
        y = random.randint(30, 420)
        x_speed = Fash.fash_x_speed - 0.5
        run_images = []
        dead_images = []
        self.load_images(run_images)
        self.dead_images(dead_images)
        image = run_images[0]
        if Fash06.rank_flag:

            super().__init__(image, run_images, dead_images, SCREEN_WIDTH, y, x_speed, 0, 100)
        else:
            super().__init__(image, run_images, dead_images, SCREEN_WIDTH, 300, x_speed, 0, 100)

    def load_images(self, run_images):
        run_images.append(pygame.image.load('./image/fish06_00.png'))
        run_images.append(pygame.image.load('./image/fish06_01.png'))
        run_images.append(pygame.image.load('./image/fish06_02.png'))
        run_images.append(pygame.image.load('./image/fish06_03.png'))
        run_images.append(pygame.image.load('./image/fish06_04.png'))
        run_images.append(pygame.image.load('./image/fish06_05.png'))
        run_images.append(pygame.image.load('./image/fish06_06.png'))
        run_images.append(pygame.image.load('./image/fish06_07.png'))
        run_images.append(pygame.image.load('./image/fish06_08.png'))
        run_images.append(pygame.image.load('./image/fish06_09.png'))

    def dead_images(self, d_images):
        d_images.append(pygame.image.load('./image/fish06_catch_01.png'))
        d_images.append(pygame.image.load('./image/fish06_catch_02.png'))


class Fash08(Fash):
    index = 0,
    count = 0
    rank_flag = True

    def __init__(self):
        y = random.randint(30, 420)
        x_speed = Fash.fash_x_speed + 0.4
        run_images = []
        dead_images = []
        self.load_images(run_images)
        self.dead_images(dead_images)
        image = run_images[0]
        if Fash08.rank_flag:

            super().__init__(image, run_images, dead_images, SCREEN_WIDTH, y, x_speed, 0, 200)
        else:
            pass

    def load_images(self, run_images):
        run_images.append(pygame.image.load('./image/fish08_00.png'))
        run_images.append(pygame.image.load('./image/fish08_01.png'))
        run_images.append(pygame.image.load('./image/fish08_02.png'))
        run_images.append(pygame.image.load('./image/fish08_03.png'))
        run_images.append(pygame.image.load('./image/fish08_04.png'))
        run_images.append(pygame.image.load('./image/fish08_05.png'))
        run_images.append(pygame.image.load('./image/fish08_06.png'))
        run_images.append(pygame.image.load('./image/fish08_07.png'))
        run_images.append(pygame.image.load('./image/fish08_08.png'))
        run_images.append(pygame.image.load('./image/fish08_09.png'))

    def dead_images(self, d_images):
        d_images.append(pygame.image.load('./image/fish08_catch_01.png'))
        d_images.append(pygame.image.load('./image/fish08_catch_02.png'))
        d_images.append(pygame.image.load('./image/fish08_catch_03.png'))
        d_images.append(pygame.image.load('./image/fish08_catch_04.png'))


class Fash09(Fash):
    index = 0,
    count = 0
    rank_flag = True

    def __init__(self):
        y = random.randint(30, 400)
        x_speed = Fash.fash_x_speed + 0.3
        run_images = []
        dead_images = []
        self.load_images(run_images)
        self.dead_images(dead_images)
        image = run_images[0]
        if Fash09.flag:

            super().__init__(image, run_images, dead_images, SCREEN_WIDTH, y, x_speed, 0, 300)
        else:
            pass

    def load_images(self, run_images):
        run_images.append(pygame.image.load('./image/fish09_00.png'))
        run_images.append(pygame.image.load('./image/fish09_01.png'))
        run_images.append(pygame.image.load('./image/fish09_02.png'))
        run_images.append(pygame.image.load('./image/fish09_03.png'))
        run_images.append(pygame.image.load('./image/fish09_04.png'))
        run_images.append(pygame.image.load('./image/fish09_05.png'))
        run_images.append(pygame.image.load('./image/fish09_06.png'))
        run_images.append(pygame.image.load('./image/fish09_07.png'))
        run_images.append(pygame.image.load('./image/fish09_08.png'))
        run_images.append(pygame.image.load('./image/fish09_09.png'))

    def dead_images(self, d_images):
        d_images.append(pygame.image.load('./image/fish09_catch_01.png'))
        d_images.append(pygame.image.load('./image/fish09_catch_02.png'))
        d_images.append(pygame.image.load('./image/fish09_catch_03.png'))
        d_images.append(pygame.image.load('./image/fish09_catch_04.png'))


class Fash13(Fash):
    index = 0,
    count = 0
    rank_flag = True

    def __init__(self):
        y = random.randint(100, 350)
        x_speed = Fash.fash_x_speed + 0.4
        run_images = []
        dead_images = []
        self.load_images(run_images)
        self.dead_images(dead_images)
        image = run_images[0]
        if Fash13.rank_flag:
            super().__init__(image, run_images, dead_images, SCREEN_WIDTH, y, x_speed, 0, 400)
        else:
            super().__init__(image, run_images, dead_images, SCREEN_WIDTH, 200, x_speed, 0, 400)

    def load_images(self, run_images):
        run_images.append(pygame.image.load('./image/fish13_00.png'))
        run_images.append(pygame.image.load('./image/fish13_01.png'))
        run_images.append(pygame.image.load('./image/fish13_02.png'))
        run_images.append(pygame.image.load('./image/fish13_03.png'))
        run_images.append(pygame.image.load('./image/fish13_04.png'))
        run_images.append(pygame.image.load('./image/fish13_05.png'))
        run_images.append(pygame.image.load('./image/fish13_06.png'))
        run_images.append(pygame.image.load('./image/fish13_07.png'))
        run_images.append(pygame.image.load('./image/fish13_08.png'))
        run_images.append(pygame.image.load('./image/fish13_09.png'))

    def dead_images(self, d_images):
        d_images.append(pygame.image.load('./image/fish13_catch_01.png'))
        d_images.append(pygame.image.load('./image/fish13_catch_02.png'))
        d_images.append(pygame.image.load('./image/fish13_catch_04.png'))
        d_images.append(pygame.image.load('./image/fish13_catch_04.png'))


class Fash14(Fash):
    index = 0
    count = 0
    rank_flag = True

    def __init__(self):
        y = random.randint(100, 400)
        x_speed = Fash.fash_x_speed + 0.4
        run_images = []
        dead_images = []
        self.load_images(run_images)
        self.dead_images(dead_images)
        image = run_images[0]
        if Fash14.rank_flag:

            super().__init__(image, run_images, dead_images, SCREEN_WIDTH, y, x_speed, 0, 500)
        else:
            pass

    def load_images(self, run_images):
        run_images.append(pygame.image.load('./image/fish14_00.png'))
        run_images.append(pygame.image.load('./image/fish14_01.png'))
        run_images.append(pygame.image.load('./image/fish14_02.png'))
        run_images.append(pygame.image.load('./image/fish14_03.png'))
        run_images.append(pygame.image.load('./image/fish14_04.png'))
        run_images.append(pygame.image.load('./image/fish14_05.png'))
        run_images.append(pygame.image.load('./image/fish14_06.png'))
        run_images.append(pygame.image.load('./image/fish14_07.png'))
        run_images.append(pygame.image.load('./image/fish14_08.png'))
        run_images.append(pygame.image.load('./image/fish14_09.png'))

    def dead_images(self, d_images):
        d_images.append(pygame.image.load('./image/fish14_catch_01.png'))
        d_images.append(pygame.image.load('./image/fish14_catch_02.png'))
        d_images.append(pygame.image.load('./image/fish14_catch_04.png'))
        d_images.append(pygame.image.load('./image/fish14_catch_04.png'))

# 展示文字信息
class DynamicGraph(object):
    def __init__(self, font_name, text, color, size, x, y):
        self.font_name = font_name
        self.text = text
        self.color = color
        self.size = size
        self.x = x
        self.y = y
        self.count = 40
        self.flag = False

    def update(self):
        if self.flag:
            self.count -= 1
        if self.count == 0:
            self.flag = False
            self.count = 40

    def draw(self):
        font = pygame.font.Font(self.font_name, self.size)
        text_surface = font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.x, self.y)
        if self.flag:
            SCREEN.blit(text_surface, text_rect)

#展示技能图标
class DynamicLogo(pygame.sprite.Sprite, object):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./image/ice_logo.png')
        self.x = x
        self.y = y
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.count = 40
        self.flag = False
        self.angle = math.atan2(70 - (self.y + 32), 40 - (self.x + 26))
        self.speed_y = (math.sin(self.angle)) * 25
        self.speed_x = (math.cos(self.angle)) * 25

    def update(self, *args):
        if self.flag:
            self.x += self.speed_x
            self.y += self.speed_y
            self.image_width -= 1
            self.image_height -= 1
            self.image = pygame.transform.smoothscale(self.image, (self.image_width, self.image_height))

        if self.x < 40 and self.y < 70:
            self.flag = False

        self.rect = (self.x - self.image_width / 2, self.y - self.image_height / 2)

    def draw(self):
        if self.flag:
            arrow1 = pygame.transform.rotate(self.image, 270 - self.angle * 57.29)
            SCREEN.blit(arrow1, (self.x, self.y))


# class Mermaid(pygame.sprite.Sprite, object):
#     def __init__(self, x, y):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.image.load('./image/ice_logo.png')
#         self.x = x
#         self.y = y
#         self.image_width = self.image.get_width()
#         self.image_height = self.image.get_height()
#         self.count = 40
#         self.flag = False
#         self.angle = math.atan2(70 - (self.y + 32), 40 - (self.x + 26))
#         self.speed_y = (math.sin(self.angle)) * 25
#         self.speed_x = (math.cos(self.angle)) * 25
#
#     def update(self, *args):
#         if self.flag:
#             self.x += self.speed_x
#             self.y += self.speed_y
#             self.image_width -= 1
#             self.image_height -= 1
#             self.image = pygame.transform.smoothscale(self.image, (self.image_width, self.image_height))
#
#         if self.x < 40 and self.y < 70:
#             self.flag = False
#
#         self.rect = (self.x - self.image_width / 2, self.y - self.image_height / 2)
#
#     def draw(self):
#         if self.flag:
#             arrow1 = pygame.transform.rotate(self.image, 270 - self.angle * 57.29)
#             SCREEN.blit(arrow1, (self.x, self.y))
# 全屏冰冻
class IceScreen(object):
    def __init__(self):
        self.image = pygame.image.load('./image/ice_screen.png')
        self.count = 60
        self.flag = True

    def update(self):
        if not self.flag:
            self.count -= 1
        if self.count == 0:
            self.flag = True
            Fash.flag = True
            self.count = 80

    def draw(self):
        if not self.flag:
            SCREEN.blit(self.image, (0, 0))

#美人鱼，大boss
class Mermaid(GameObject):
    def __init__(self):
        self.role_rect = (59, 0, 170, 188)
        self.count = 0
        self.image = pygame.image.load('./image/mermaid3.png')
        self.x = 305
        self.y = -300
        self.life = 1000
        self.is_alive = True
        self.death_image = []
        self.death_image.append(pygame.image.load('./image/mermaid3.png'))
        self.death_image.append(pygame.image.load('./image/mermaid3.png'))
        self.death_image.append(pygame.image.load('./image/mermaid3.png'))
        self.death_image.append(pygame.image.load('./image/mermaid3.png'))
        # self.death_image.append(pygame.image.load('./image/mermaid3.png').subsurface((0, 369, 190, 200)))
        # self.death_image.append(pygame.image.load('./image/mermaid3.png').subsurface((86, 369, 190, 200)))
        # self.death_image.append(pygame.image.load('./image/mermaid3.png').subsurface((172, 369, 190, 200)))
        # self.death_image.append(pygame.image.load('./image/mermaid3.png').subsurface((258, 369,190, 200)))
        self.death_count = 0
        self.flag = False
        self.direction = 1
        GameObject.__init__(self, self.image, self.x, self.y)

    def update(self):
        if self.flag:
            if self.life > 0:
                self.y=130
                print('life', self.life)
                if self.direction == 1 and self.x > 200:
                    print('1111111')
                    self.x -= 5
                elif self.x <= 200:
                    self.direction = -1
                if self.direction == -1 and self.x < 400:
                    self.x += 5
                elif self.x >= 400:
                    self.direction = 1

            else:
                self.is_alive = False
                self.y=-300
                print('222222')
        else:
            self.y = -200
            self.life=1000

    def injured(self, bullet):
        if self.flag:
            if random.randint(0, 1):
                sound = pygame.mixer.Sound('./sound/hit_target.wav')
                sound.set_volume(0.33)
                sound.play()
                self.life -= bullet.damage

    def draw(self):
        if self.flag:
            SCREEN.blit(self.image, (self.x, self.y))
