import pygame
import time
import random
import os

pygame.init()
pygame.mixer.init()
MENU_MUSIC = 'sounds/menu.mp3'
GAME_MUSIC = 'sounds/cancion_fondo.mp3'

display_width = 870
display_height = 800
button_width = 240
button_height = 55
button_start_x = (display_width - button_width) // 2
new_game_y = 400
quit_y = 470

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
BLUE = (0, 110, 164)
RED = (153, 0, 9)
YELLOW = (240, 200, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('FFR')
clock = pygame.time.Clock()

def safe_load_img(path, size=None):
    if not os.path.exists(path):
        surf = pygame.Surface((size if size else (50,50)))
        surf.fill((200,0,0))
        return surf.convert_alpha()
    im = pygame.image.load(path).convert_alpha()
    if size:
        im = pygame.transform.scale(im, size)
    return im


size_car = (120, 220)

orig_center = safe_load_img('imagenes/f1.png', (90,90))
orig_left = pygame.transform.rotate(orig_center, 20)
orig_right = pygame.transform.rotate(orig_center, -20)

car3_center = safe_load_img('imagenes/car3.png', (90,90))
car1_center = safe_load_img('imagenes/car1.png', (90,90))
car2_center = safe_load_img('imagenes/car2.png', (90,90))
car4_center = safe_load_img('imagenes/car4.png', (90,90))

car_options = [
    {'center': orig_center, 'left': orig_left, 'right': orig_right, 'name': 'ELECTRIC'},
    {'center': car3_center, 'left': pygame.transform.rotate(car3_center, 20), 'right': pygame.transform.rotate(car3_center, -20), 'name': 'BLAZE'},
    {'center': car1_center, 'left': pygame.transform.rotate(car1_center, 20), 'right': pygame.transform.rotate(car1_center, -20), 'name': 'RAZOR'},
    {'center': car2_center, 'left': pygame.transform.rotate(car2_center, 20), 'right': pygame.transform.rotate(car2_center, -20), 'name': 'NOVA'},
    {'center': car4_center, 'left': pygame.transform.rotate(car4_center, 20), 'right': pygame.transform.rotate(car4_center, -20), 'name': 'SUTRA'}
]

selected_car = 0
background = safe_load_img('imagenes/fondo.png', (display_width, display_height))
poster_img = safe_load_img('imagenes/poster.png', (display_width, display_height))


ob1 = safe_load_img("imagenes/obstacle1.png", (90,90))
ob2 = safe_load_img("imagenes/obstacle2.png", (90,90))
ob3 = safe_load_img("imagenes/obstacle3.png", (90,90))

obstacles_catalog = [
    {'img': ob1, 'type': 'cone', 'speed_mod': 0},
    {'img': ob2, 'type': 'barrier', 'speed_mod': 2},
    {'img': ob3, 'type': 'tire', 'speed_mod': 1},
    
]

def safe_load_sound(path):
    try:
        if os.path.exists(path):
            return pygame.mixer.Sound(path)
    except:
        pass
    return None

crash_sound = safe_load_sound('sounds/car_crash.wav')
MENU_MUSIC = 'sounds/menu.mp3'
GAME_MUSIC = 'sounds/cancion_fondo.mp3'



cora_img = safe_load_img('imagenes/cora.png', (50,50))
perdio1 = safe_load_img('imagenes/perdio1.png', (86,175))
perdio2 = safe_load_img('imagenes/perdio2.png', (86,175))

def draw_button(msg, x, y, w, h, color_inactive, color_active):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    hovered = x < mouse[0] < x + w and y < mouse[1] < y + h

    scale = 1.12 if hovered else 1.0
    new_w = int(w * scale)
    new_h = int(h * scale)
    new_x = x - (new_w - w) // 2
    new_y = y - (new_h - h) // 2

    if hovered:
        glow = pygame.Surface((new_w + 10, new_h + 10), pygame.SRCALPHA)
        pygame.draw.rect(
            glow,
            (*color_active, 90),
            glow.get_rect(),
            border_radius=18
        )
        gameDisplay.blit(glow, (new_x - 5, new_y - 5))

    pygame.draw.rect(
        gameDisplay,
        color_active if hovered else color_inactive,
        (new_x, new_y, new_w, new_h),
        border_radius=16
    )

    font = pygame.font.Font('freesansbold.ttf', 26)
    text = font.render(msg, True, WHITE)
    rect = text.get_rect(center=(new_x + new_w // 2, new_y + new_h // 2))
    gameDisplay.blit(text, rect)

    if hovered and click[0]:
        return True
    return False


def title_animation():
   h = display_height
   while h > -300:
        gameDisplay.blit(background, (0,0))
        gameDisplay.blit(car_options[0]['center'], (display_width//2 - 40, h))
        h -= 8
        pygame.display.update()
        clock.tick(60)

def draw_title():
    f = pygame.font.Font('freesansbold.ttf', 60)
    t = f.render("FFR", True, BLUE)
    r = t.get_rect(center=(display_width//2, 180))
    gameDisplay.blit(t, r)

def credits_screen():
    running = True
    while running:
        gameDisplay.blit(background, (0,0))
        f = pygame.font.Font('freesansbold.ttf', 32)
        t = f.render("Créditos", True, YELLOW)
        gameDisplay.blit(t, (display_width//2 - 70, 80))
        f2 = pygame.font.Font('freesansbold.ttf', 22)
        lines = ["Juego creado por:",
                 "JOANNA DURAN • CITLALLY CEDILLO • IRIS AVENDAÑO • VALERIA JACOBO",
                 "",
                 "07LI11",
                 "LICENCIATURA EN INFORMATICA"]
        y = 180
        for line in lines:
            txt = f2.render(line, True, WHITE)
            gameDisplay.blit(txt, (display_width//2 - txt.get_width()//2, y))
            y += 40
        back = draw_button("Volver", button_start_x, 600, button_width, button_height, BLACK, BLUE)
        if back:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
        pygame.display.update()
        clock.tick(60)

def select_car_screen():
    global selected_car
    running = True
    card_w = 160; card_h = 260; gap = 20
    n = len(car_options)
    total_w = n * card_w + (n - 1) * gap
    start_x = (display_width - total_w) // 2
    while running:
        gameDisplay.blit(background, (0,0))
        title = pygame.font.Font('freesansbold.ttf', 40).render("Selecciona tu auto", True, WHITE)
        gameDisplay.blit(title, (display_width//2 - title.get_width()//2, 40))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for i in range(n):
            x = start_x + i * (card_w + gap); y = 140
            card_color = BLUE if i == selected_car else GRAY
            pygame.draw.rect(gameDisplay, card_color, (x, y, card_w, card_h), border_radius=12)
            img = pygame.transform.scale(car_options[i]['center'], (110,200))
            gameDisplay.blit(img, (x + (card_w - 110)//2, y + 10))
            name = car_options[i]['name']
            txt = pygame.font.Font('freesansbold.ttf', 22).render(name, True, WHITE)
            gameDisplay.blit(txt, (x + card_w//2 - txt.get_width()//2, y + 215))
            if x + card_w > mouse[0] > x and y + card_h > mouse[1] > y:
                if click[0]:
                    selected_car = i
        play = draw_button("Aceptar", button_start_x, 600, button_width, button_height, BLACK, BLUE)
        if play:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
        pygame.display.update()
        clock.tick(60)

def play_hit_animation(x, y):
    try:
        gameDisplay.blit(perdio1, (x - 10, y - 10))
        pygame.display.update(); pygame.time.delay(120)
        gameDisplay.blit(perdio2, (x - 10, y - 10))
        pygame.display.update(); pygame.time.delay(120)
    except:
        pass

def show_hearts(lives):
    start_x = display_width - 40
    for i in range(lives):
        gameDisplay.blit(cora_img, (start_x - i*38, 10))

def game_over_screen(final_score):
    run = True
    while run:
        gameDisplay.fill((0, 0, 0))  

        f = pygame.font.Font('freesansbold.ttf', 72)
        t = f.render("GAME OVER", True, RED)
        gameDisplay.blit(t, (display_width//2 - t.get_width()//2, 220))

        f2 = pygame.font.Font('freesansbold.ttf', 36)
        score_txt = f2.render(f"Puntaje final: {final_score}", True, WHITE)
        gameDisplay.blit(
            score_txt,
            (display_width//2 - score_txt.get_width()//2, 330)
        )

        f3 = pygame.font.Font('freesansbold.ttf', 24)
        s = f3.render("Presiona ESPACIO para volver al menú", True, GRAY)
        gameDisplay.blit(
            s,
            (display_width//2 - s.get_width()//2, 400)
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mixer.music.stop()
                return

        pygame.display.update()
        clock.tick(60)

def poster_fade_in():
    overlay = pygame.Surface((display_width, display_height))
    overlay.fill((0, 0, 0))
    for alpha in range(255, -1, -10):
        gameDisplay.blit(poster_img, (0, 0))
        overlay.set_alpha(alpha)
        gameDisplay.blit(overlay, (0, 0))
        pygame.display.update()
        clock.tick(60)

def splash_screen():
    pygame.mixer.music.load(MENU_MUSIC)
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)

    poster_fade_in()  
    running = True
    while running:
        gameDisplay.blit(poster_img, (0, 0))

        start = draw_button(
            "INICIAR",
            80,
            520,
            180,
            45,
            BLACK,
            GRAY
        )

        quit_game = draw_button(
            "SALIR",
            80,
            580,
            180,
            45,
            BLACK,
            GRAY
        )

        if start:
            fade_out()   
            return

        if quit_game:
            pygame.quit()
            quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(60) 

def fade_out():
    fade = pygame.Surface((display_width, display_height))
    fade.fill((0, 0, 0))
    for alpha in range(0, 180, 8):
        fade.set_alpha(alpha)
        gameDisplay.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(20)

def game_intro():
    title_animation()
    intro = True
    while intro:
        gameDisplay.blit(background, (0,0))
        draw_title()
        play = draw_button("Jugar", button_start_x, 350, button_width, button_height, BLACK, BLUE)
        car_sel = draw_button("Seleccionar auto", button_start_x, 420, button_width, button_height, BLACK, BLUE)
        credits = draw_button("Créditos", button_start_x, 490, button_width, button_height, BLACK, BLUE)
        quit_game = draw_button("Salir", button_start_x, 560, button_width, button_height, RED, BLUE)
        if play:
            pygame.mixer.music.fadeout(800)
            pygame.time.delay(800)
            countdown()
            return
        if car_sel:
            select_car_screen()
        if credits:
            credits_screen()
        if quit_game:
            pygame.quit(); quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
        pygame.display.update()
        clock.tick(60)

def spawn_obstacle(level):
    choice = random.choice(obstacles_catalog)
    base_speed = {1:5, 2:8, 3:11, 4:14}[level]
    speed = base_speed + choice['speed_mod'] + random.randint(0,2)
    ROAD_LEFT = 250
    ROAD_RIGHT = 620
    x = random.randint(ROAD_LEFT, ROAD_RIGHT - choice['img'].get_width())
    y = -50

    return {'img': choice['img'], 'type': choice['type'], 'x': x, 'y': y, 'speed': speed}

def countdown():
    font = pygame.font.Font('freesansbold.ttf', 120)
    for n in ["3", "2", "1"]:
        gameDisplay.blit(background, (0, 0))
        txt = font.render(n, True, WHITE)
        gameDisplay.blit(
            txt,
            (display_width//2 - txt.get_width()//2,
             display_height//2 - txt.get_height()//2)
        )
        pygame.display.update()
        pygame.time.delay(700)

def draw_level_bar(score, level, x=20, y=150, w=200, h=18):
    progress = (score % 7) / 7  # 0 a 1
    pygame.draw.rect(gameDisplay, GRAY, (x, y, w, h), border_radius=8)
    pygame.draw.rect(gameDisplay, BLUE, (x, y, int(w * progress), h), border_radius=8)

def game_loop():
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(GAME_MUSIC)
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1, fade_ms=800)
    except:
        pass
    ROAD_LEFT = 250
    ROAD_RIGHT = 620

    x = (ROAD_LEFT + ROAD_RIGHT) // 2
    y = display_height * 0.6

    
    x_change = 0

    current = spawn_obstacle(1)
    dodged_cones = 0
    level = 1

    carImg = car_options[selected_car]['center']
    carLeft = car_options[selected_car]['left']
    carRight = car_options[selected_car]['right']

    
    car_width, car_height = carImg.get_rect().size

    hs_path = 'resources/high_score.txt'
    try:
        with open(hs_path, 'r') as hs:
            high_score = int(hs.read())
    except:
        high_score = 0

    bg_y1 = 0
    bg_y2 = -display_height

    running = True
    lives = 3
    invuln = 0

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    x_change = -10
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    x_change = 10
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d]:
                    x_change = 0

        x += x_change
        x = max(ROAD_LEFT, min(x, ROAD_RIGHT - car_width))


        bg_y1 += 3
        bg_y2 += 3
        if bg_y1 >= display_height: bg_y1 = -display_height
        if bg_y2 >= display_height: bg_y2 = -display_height

        gameDisplay.blit(background, (0, bg_y1))
        gameDisplay.blit(background, (0, bg_y2))

        if draw_button("MENÚ", 10, 10, 120, 40, BLUE, GRAY):
            return

        gameDisplay.blit(current['img'], (current['x'], current['y']))
        current['y'] += current['speed']

        if x_change == 0:
            gameDisplay.blit(carImg, (x, y))
        elif x_change < 0:
            gameDisplay.blit(carLeft, (x, y))
        else:
            gameDisplay.blit(carRight, (x, y))

        f = pygame.font.SysFont(None, 28)
        gameDisplay.blit(f.render(f"Puntaje (obstaculos): {dodged_cones}", True, WHITE), (20, 60))
        gameDisplay.blit(f.render(f"Nivel: {level}", True, WHITE), (20, 90))
        draw_level_bar(dodged_cones, level)
        gameDisplay.blit(f.render(f"Récord: {high_score}", True, WHITE), (20, 120))

        show_hearts(lives)

        car_rect = pygame.Rect(x, y, car_width, car_height)
        if current['type'] == 'cone':
            obs_rect = pygame.Rect(
                current['x'],
                current['y'],
                current['img'].get_width(),
                current['img'].get_height()
    )
        else:
            obs_rect = pygame.Rect(
                current['x'] + 10,
                current['y'] + 10,
                
                current['img'].get_width() - 20,
                current['img'].get_height() - 20
    )

        pygame.draw.rect(gameDisplay, (255, 0, 0), obs_rect, 2)

        if invuln > 0:
            invuln -= 1  

        if car_rect.colliderect(obs_rect) and invuln == 0:
            if current['type'] != 'cone':
                if crash_sound: 
                    crash_sound.play()

            play_hit_animation(int(x), int(y))
            lives -= 1
            invuln = 40
            current = spawn_obstacle(level)

            if lives <= 0:
                game_over_screen(dodged_cones)
                return

        if current['y'] > display_height:
                dodged_cones += 1

                if dodged_cones % 7 == 0 and level < 4:
                    level += 1

                current = spawn_obstacle(level)

        if dodged_cones > high_score:
            try:
                with open(hs_path, 'w') as hs:
                    hs.write(str(dodged_cones))
                high_score = dodged_cones
            except:
                pass

        pygame.display.update()
        clock.tick(60)

while True:
    splash_screen()
    game_intro()

    game_loop()
