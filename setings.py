import pygame as pg
from copy import deepcopy
from random import choice, randrange

W, H = 10,20
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 950, 940
FPS = 60

pg.init()
sc = pg.display.set_mode(RES)
game_sc = pg.Surface(GAME_RES)
clock = pg.time.Clock()

Icon = pg.image.load('resources/icon.png')
pg.display.set_caption('TETRIS ~ Made By Saroshi_PL')
pg.display.set_icon(Icon)

grid = [pg.Rect(x*TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pg.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pg.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for j in range(H)]


font = pg.font.Font('resources/fonts/Franchises.ttf', 45)

title_record = font.render('Record', True, pg.Color('orange'))
title_score = font.render('Score', True, pg.Color('green'))

anim_count, anim_speed, anim_limit = 0,60,2000

bg = pg.image.load('resources/background.jpg').convert()

logo = pg.image.load('resources/logo.png')

bg = pg.transform.scale(bg, (950,940))
logo = pg.transform.scale(logo, (240,64))

score,lines = 0,0
scores = {0: 0, 1:100, 2:300, 3:700, 4:1500}

get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))
figure, next_figure = deepcopy(choice(figures)),deepcopy(choice(figures))
color, next_color = get_color(), get_color()


put_sounds = ['resources/put.wav','resources/put1.wav','resources/put2.wav']
put_sound = choice(put_sounds)
print(put_sound)
pg.mixer.init()
