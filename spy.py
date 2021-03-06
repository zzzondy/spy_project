"""
###############################################################################
	Space Shooter (Redux, plus fonts and sounds) by Kenney Vleugels (www.kenney.nl)
			------------------------------
			        License (CC0)
	       http://creativecommons.org/publicdomain/zero/1.0/
	You may use these graphics in personal and commercial projects.
	Credit (Kenney or www.kenney.nl) would be nice but is not manda tory.
###############################################################################
"""
import pygame
import random
from os import path
import time

# Ссылки на папки со звуком и спрайтами
img_dir = path.join(path.dirname(__file__), 'img')
sound_dir = path.join(path.dirname(__file__), 'sounds')
COUNT = 0

WIDTH = 480  # Ширина окна
HEIGHT = 600  # Высота окна
FPS = 60  # Плавность и скорость игры

# Все цвета радуги
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 186)
CYAN = (59, 190, 186)
CVET_ANDREW_NIKOLAEVICHA = (171, 112, 79)
BIG_YELLOW = (255, 247, 38)
MODNIY_ROZOVIY = (254, 167, 255)
MODNIY_SINIJ = (134, 193, 249)

# Инициализация окна с игрой
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spy by Vanyok and Artyom")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    """Класс игрока"""

    def __init__(self):
        """Инициализация игрока"""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        """Движение игрока"""
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        """Выстрел"""
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    """Класс метеоритов и Андрея Николаевича"""

    def __init__(self):
        """Случайная инициализаия моба"""
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice([meteor1_img, meteor2_img, bigBoss, medBoss, miniBoss1, miniBoss2])
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        """Моб летает по полю"""
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    """Класс выстрела"""

    def __init__(self, x, y):
        """Случайная инициализация пули"""
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice([laserRed1_img, laserRed2_img, laserRed3_img, laserRed4_img])
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        """Полет пули"""
        self.rect.y += self.speedy
        # Если пуля вылетает за верхнюю границу - она пропадает
        if self.rect.bottom < 0:
            self.kill()


def game_over_first():
    """Основаная функция конца игры. Вызывается когда в персонажа попали."""
    pygame.mixer.music.stop()
    sound_lose.play()
    screen.fill(BLACK)
    screen.blit(over_background, over_background_rect)
    font = pygame.font.Font(None, 50)
    text = font.render(f'Итого: {str(COUNT)}', True, random_color)
    text_x = 170
    text_y = 270
    screen.blit(text, (text_x, text_y))
    all_sprites.add(cursor)
    pygame.display.flip()


def game_over_second(mouse_in_refresh_pole):
    """Функция конца игры, служащая для нужд разработчика (костыль)."""
    global all_sprites
    screen.fill(BLACK)
    screen.blit(over_background, over_background_rect)
    if not mouse_in_refresh_pole:
        screen.blit(nonactive_refresh.image, (170, 340))
    else:
        screen.blit(active_refresh.image, (170, 340))
    font = pygame.font.Font(None, 50)
    text = font.render(f'Итого: {str(COUNT)}', True, random_color)
    text_x = 170
    text_y = 270
    screen.blit(text, (text_x, text_y))
    all_sprites = pygame.sprite.Group()
    all_sprites.add(cursor)
    if pygame.mouse.get_focused():
        all_sprites.draw(screen)
    pygame.display.flip()


def new_game():
    """Функция новой игры. Когда нажата кнопка "перезагрузить", она вызывается."""
    global all_sprites, cursor, mobs, bullets, player, i, m, random_color, flag_game_over, running, COUNT
    pygame.display.set_caption("Spy by Vanyok and Artyom")
    COUNT = 0
    all_sprites = pygame.sprite.Group()
    cursor = pygame.sprite.Sprite()
    cursor.image = pygame.image.load(path.join(img_dir, 'cursor.png'))
    cursor.rect = cursor.image.get_rect()
    pygame.mouse.set_visible(False)
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    random_color = random.choice(
        [WHITE, BLUE, YELLOW, GREEN, RED, MAGENTA, CYAN, CVET_ANDREW_NIKOLAEVICHA, MODNIY_ROZOVIY, MODNIY_SINIJ,
         BIG_YELLOW])
    flag_game_over = False
    pygame.mixer.music.load(path.join(sound_dir, random.choice(['ougigi.ogg', 'white_elephants.mp3', 'fonk.ogg'])))
    pygame.mixer.music.play()


def correct_click_motion(mouse_pos):
    """Определяет правильность положения мышки. Венет True если мышка находится в кнопке 'перезагрузить'."""
    if 170 <= mouse_pos[0] <= 305 and 340 <= mouse_pos[1] <= 370:
        return True
    return False


def print_score_on_the_screen():
    """Постоянная отприсовка счета прямо на экране во время игры."""
    font = pygame.font.Font(None, 50)
    text = font.render(f'Score: {str(COUNT)}', True, random_color)
    text_x = 10
    text_y = 10
    screen.blit(text, (text_x, text_y))


# Загрузка спрайтов
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip3_red.png")).convert()
meteor1_img = pygame.image.load(path.join(img_dir, "meteorGrey_big1.png")).convert()
meteor2_img = pygame.image.load(path.join(img_dir, 'meteorGrey_med2.png')).convert()
bigBoss = pygame.image.load(path.join(img_dir, 'andrew.png'))
medBoss = pygame.image.load(path.join(img_dir, 'kerril.png'))
miniBoss1 = pygame.image.load(path.join(img_dir, 'nikita.png'))
miniBoss2 = pygame.image.load(path.join(img_dir, 'dima.png'))
laserRed1_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
laserRed2_img = pygame.image.load(path.join(img_dir, 'laserRed15.png')).convert()
laserRed3_img = pygame.image.load(path.join(img_dir, 'laserRed06.png')).convert()
laserRed4_img = pygame.image.load(path.join(img_dir, 'laserRed01.png')).convert()
over_background = pygame.image.load(path.join(img_dir, 'over_background.jpg'))
over_background_rect = over_background.get_rect()
nonactive_refresh = pygame.sprite.Sprite()
nonactive_refresh.image = pygame.image.load(path.join(img_dir, 'nonactive_refresh.png'))
nonactive_refresh.rect = nonactive_refresh.image.get_rect()
active_refresh = pygame.sprite.Sprite()
active_refresh.image = pygame.image.load(path.join(img_dir, 'active_refresh.png'))
active_refresh.rect = active_refresh.image.get_rect()

# Загрузка звуков
sound_laser = pygame.mixer.Sound(path.join(sound_dir, 'sfx_laser1.ogg'))
sound_lose = pygame.mixer.Sound(path.join(sound_dir, 'sfx_lose.ogg'))
pygame.mixer.music.load(path.join(sound_dir, random.choice(['ougigi.ogg', 'white_elephants.mp3', 'fonk.ogg'])))
sound_lose_length = sound_lose.get_length()

all_sprites = pygame.sprite.Group()
cursor = pygame.sprite.Sprite()
cursor.image = pygame.image.load(path.join(img_dir, 'cursor.png'))
cursor.rect = cursor.image.get_rect()
pygame.mouse.set_visible(False)
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    # генерация мобов.
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

random_color = random.choice(
    [WHITE, BLUE, YELLOW, GREEN, RED, MAGENTA, CYAN, CVET_ANDREW_NIKOLAEVICHA, MODNIY_ROZOVIY, MODNIY_SINIJ,
     BIG_YELLOW]) # Случайный цвет.
flag_game_over = False
flag_motion = False
running = True
pygame.mixer.music.play()
while running:
    # Игровой цикл.
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Выстрел.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
                sound_laser.play()
        # Работа с мышкой
        if event.type == pygame.MOUSEMOTION:
            cursor.rect.topleft = event.pos
            if correct_click_motion(event.pos):
                flag_motion = True
            else:
                flag_motion = False
        if event.type == pygame.MOUSEBUTTONUP:
            if correct_click_motion(event.pos):
                new_game()

    if flag_game_over:
        # когда игра кончилась.
        if flag_motion:
            game_over_second(True)
        else:
            game_over_second(False)
        continue

    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        # обработка попаданий.
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        COUNT += 10

    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        # когда персонаж столкнулся.
        flag_game_over = True
        game_over_first()
        continue

    if pygame.mouse.get_focused():
        # отрисовка нового курсора.
        all_sprites.draw(screen)

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    print_score_on_the_screen()
    pygame.display.flip()

# Конец. Авторы наелись и спят.
pygame.quit()
