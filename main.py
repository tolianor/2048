import random
import logics
import pygame
import sys
import db
import json
import os


GAMERS_DB = db.the_best()


def init_const():
    global mas, score
    mas = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    score = 0
    empty = logics.empty_list(mas)
    random.shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1, y1 = logics.get_index_from_number(random_num1)
    mas = logics.insert_2_or_4(mas, x1, y1)
    x2, y2 = logics.get_index_from_number(random_num2)
    mas = logics.insert_2_or_4(mas, x2, y2)


COLOR_TEXT_SCORE = (255, 140, 0)

COLORS = {
    0: (130, 130, 130),
    2: (255, 255, 255),
    4: (255, 128, 255),
    8: (255, 0, 255),
    16: (235, 255, 205),
    32: (235, 128, 205),
    64: (235, 0, 205),
    128: (215, 255, 155),
    256: (215, 128, 155),
    512: (215, 0, 155),
    1024: (195, 255, 105),
    2048: (195, 128, 105),
    4096: (195, 0, 105),
    8192: (175, 255, 55),
    16384: (175, 128, 55),
    32768: (175, 0, 55),
    65536: (175, 255, 5),
    131072: (175, 128, 5),
    262144: (175, 0, 5),
}

WHITE = (255, 255, 255)
GRAY = (130, 130, 130)
BLACK = (0, 0, 0)

BLOCKS = 4
SIZE_BLOCK = 110
MARGIN = 10
WIGHT = BLOCKS * SIZE_BLOCK + (BLOCKS + 1) * MARGIN
HEIGHT = WIGHT + 110
TITLE_REQ = pygame.Rect(0, 0, WIGHT, 110)

USERNAME = None
mas = None
score = None
save_mas = None
save_score = None
path = os.getcwd()
if "data.txt" in os.listdir():
    with open("data.txt") as file:
        data = json.load(file)
        USERNAME = data['user']
        mas = data['mas']
        score = data['score']
    full_path = os.path.join(path, "data.txt")
    os.remove(full_path)
else:
    init_const()
logics.pretty_print(mas)

pygame.init()
screen = pygame.display.set_mode((WIGHT, HEIGHT))
pygame.display.set_caption("2048")


def draw_intro():
    image = pygame.image.load("intro.jpg")
    font = pygame.font.SysFont("comicsansms", 50)
    text_welcome = font.render("Welcome", True, WHITE)
    name = "Enter your name"
    is_find_name = False

    while not is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == "Enter your name":
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name) > 3:
                        global USERNAME
                        USERNAME = name
                        is_find_name = True

        screen.fill(GRAY)
        text_name = font.render(name, True, WHITE)
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center
        screen.blit(image, (10, 10))
        screen.blit(text_welcome, (250, 75))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(BLACK)


def draw_game_over():
    global USERNAME, mas, GAMERS_DB
    image = pygame.image.load("intro.jpg")
    font = pygame.font.SysFont("comicsansms", 45)
    text_game_over = font.render("Game Over", True, WHITE)
    text_score = font.render(f"You have {score} points", True, WHITE)
    best_score = GAMERS_DB[0][1]

    db.insert_result(USERNAME, score)

    if score > best_score:
        text = "New record"
    else:
        text = f"Record  is {best_score}"
    text_record = font.render(text, True, WHITE)
    GAMERS_DB = db.the_best()
    make_decision = False
    while not make_decision:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    init_const()
                    make_decision = True
                elif event.key == pygame.K_SPACE:
                    USERNAME = None
                    init_const()
                    make_decision = True
            screen.fill(GRAY)
            screen.blit(image, (10, 10))
            screen.blit(text_game_over, (230, 75))
            rect_score = text_score.get_rect()
            rect_score.center = screen.get_rect().center
            screen.blit(text_score, rect_score)
            screen.blit(text_record, (rect_score[0], rect_score[1] + 70))
            pygame.display.update()

        screen.fill(BLACK)


def draw_top_gamers():
    font_top = pygame.font.SysFont("comicsansms", 15)
    font_gamer = pygame.font.SysFont("comicsansms", 18)
    text_head = font_top.render(f"Best gamers:", True, COLOR_TEXT_SCORE)
    screen.blit(text_head, (320, 15))
    for index, gamer in enumerate(GAMERS_DB):
        name, scores = gamer
        s = f"{index + 1}. {name} - {scores}"
        text_top_gamers = font_gamer.render(s, True, COLOR_TEXT_SCORE)
        screen.blit(text_top_gamers, (320, 40 + 20 * index))


def draw_interface(scores, deltas=0):
    pygame.draw.rect(screen, WHITE, TITLE_REQ)
    font = pygame.font.SysFont("comicsansms", 60)
    font_score = pygame.font.SysFont("comicsansms", 38)
    font_delta = pygame.font.SysFont("comicsansms", 36)
    text_score = font_score.render(f"Total score: {scores}", True, COLOR_TEXT_SCORE)
    screen.blit(text_score, (20, 35))
    if deltas > 0:
        text_delta = font_delta.render(f"+ {deltas}", True, COLOR_TEXT_SCORE)
        screen.blit(text_delta, (205, 70))
    logics.pretty_print(mas)
    draw_top_gamers()
    for row in range(BLOCKS):
        for column in range(BLOCKS):
            value = mas[row][column]
            text = font.render(str(value), True, BLACK)
            w = column * SIZE_BLOCK + (column + 1) * MARGIN
            h = row * SIZE_BLOCK + (row + 1) * MARGIN + SIZE_BLOCK
            pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCK, SIZE_BLOCK))
            if value != 0:
                font_w, font_h = text.get_size()
                text_x = w + (SIZE_BLOCK - font_w) / 2
                text_y = h + (SIZE_BLOCK - font_h) / 2
                screen.blit(text, (text_x, text_y))


def save_game():
    datas = {
        'user': USERNAME,
        'score': score,
        'mas': mas,
    }
    with open('data.txt', 'w') as outfile:
        json.dump(datas, outfile)


def game_loop():
    global score, mas, save_mas, save_score
    draw_interface(score)
    pygame.display.update()
    is_mas_move = False
    while logics.is_zero_in_mas(mas) or logics.can_move(mas):
        for event in pygame.event.get():
            save_mas_r = None
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                delta = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    mas, delta, is_mas_move, save_mas_r = logics.move_left(mas)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    mas, delta, is_mas_move, save_mas_r = logics.move_right(mas)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    mas, delta, is_mas_move, save_mas_r = logics.move_up(mas)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    mas, delta, is_mas_move, save_mas_r = logics.move_down(mas)
                elif event.key == pygame.K_BACKSPACE:
                    mas = save_mas
                    score = save_score
                elif event.key == pygame.K_ESCAPE:
                    save_game()
                    pygame.quit()
                    sys.exit()
                save_score = score
                score += delta
                if logics.is_zero_in_mas(mas) and is_mas_move:
                    save_mas = save_mas_r
                    empty = logics.empty_list(mas)
                    random.shuffle(empty)
                    random_num = empty.pop()
                    x, y = logics.get_index_from_number(random_num)
                    mas = logics.insert_2_or_4(mas, x, y)
                    is_mas_move = False

                draw_interface(score, delta)
                pygame.display.update()


while True:
    if USERNAME is None:
        draw_intro()
    game_loop()
    draw_game_over()
