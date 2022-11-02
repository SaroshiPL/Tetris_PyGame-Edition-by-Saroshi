import pygame as pg
from copy import deepcopy
from random import choice, randrange
from setings import *
import sys



def check_border():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


def draw_rect_alpha(surface, color, rect):
    shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
    pg.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


BG_sound = pg.mixer.Sound('resources/theme.mp3')
BG_sound.play(loops=100000)


while True:
    record = get_record()
    dx, rotate = 0, False
    sc.blit(bg,(0,0))
    
    sc.blit(game_sc,(40,25))
    sc.blit(logo,(610,30))
    game_sc.fill(pg.Color('black'))

    draw_rect_alpha(sc, (0, 0, 0, 230), (630, 120, 200, 800))

    # Delay for full lines

    for i in range(lines):
        pg.time.wait(200)
        clear_line_sound = pg.mixer.Sound('resources/clear_line.wav')
        clear_line_sound.play()

    keys = pg.key.get_pressed()
            
    if keys[pg.K_f] == True :
        anim_speed = 0
    elif keys[pg.K_f] == False :
        anim_speed= 60

    #Control
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                dx = -1
            elif event.key == pg.K_d:
                dx = 1
            elif event.key == pg.K_SPACE:
                anim_limit = -1
            elif event.key == pg.K_w:
                rotate = True
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.key == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.key == pg.K_f:
                dx = dx
                
                
                
                
    #Move X
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_border():
            figure = deepcopy(figure_old)
            break
    
    #Move Y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_border():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                putsound = pg.mixer.Sound(put_sound)
                putsound.play()
                put_sound = choice(put_sounds)
                break

    #Rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_border():
                figure = deepcopy(figure_old)
                break
    
    #Check Line
    line, lines = H - 1, 0
    line = H -1
    for row in range(H -1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    #Compute Score
    score += scores[lines]
    #Draw grid
    [pg.draw.rect(game_sc,(40,40,40), i_rect,1) for i_rect in grid]

    #Draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pg.draw.rect(game_sc, color, figure_rect)

    #Draw Next Figure
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 505
        figure_rect.y = next_figure[i].y * TILE + 185
        pg.draw.rect(sc, next_color, figure_rect)

    #Draw Field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pg.draw.rect(game_sc, col, figure_rect)
    
    #draw titles
    sc.blit(title_score, (685,780))
    sc.blit(font.render(str(score), True, pg.Color('white')),(700,840))
    sc.blit(title_record, (675,380))
    sc.blit(font.render(record, True, pg.Color('violet')),(700,440))

    #Game Over
    for i in range(W):
        if field[0][i]:
            BG_sound.stop()
            gameover_sound = pg.mixer.Sound('resources/gameover.wav')
            gameover_sound.play()
            pg.time.wait(1600)
            set_record(record, score)
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pg.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (40, 25))
                pg.display.flip()
                clock.tick(200)
            pg.time.wait(1000)
            BG_sound.play(loops=100000)
    pg.display.flip()
    clock.tick(FPS)