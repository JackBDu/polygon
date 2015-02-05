########################################################
###                    Polygon                       ###
########################################################

__author__ = "Jack B. Du (Jiadong Du)"
__copyright__ = "Copyright 2014, DS @NYUSH"
__email__ = "JackBDu@nyu.edu"

import pygame
from pygame.locals import *
from positional_list import PositionalList
import math

# absolute varibles
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (0, 0, 255)

# manual initialization
pygame.init()
INIT_SCREEN_W = 1024
INIT_SCREEN_H = 768
FPS = 50
REDIUS = 10
bg_color = WHITE_COLOR
fullscreen = False
caption = "Jack's Polygon"
add = False
closed = False
move = False
deltaX = 0
deltaY = 0
mousePos = (0, 0)
pMousePos = mousePos
letsMove = False
inserted = False

# get device info
infoObject = pygame.display.Info()
FULLSCREEN_W = infoObject.current_w
FULLSCREEN_H = infoObject.current_h

# automatic initialization
if fullscreen:
    current_screen_w = FULLSCREEN_W
    current_screen_h = FULLSCREEN_H
else:
    current_screen_w = INIT_SCREEN_W
    current_screen_h = INIT_SCREEN_H

screen = pygame.display.set_mode((current_screen_w, current_screen_h), 0, 32)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(bg_color)

pygame.display.set_caption(caption)

def main():
    global screen, polygonList, mainloop

    polygonList = PositionalList()
    
    mainloop = True
    
    while mainloop:

        pygame.time.Clock().tick(FPS)
        screen.blit(background,(0,0))

        update()
        draw()    

        pygame.display.update()

    pygame.quit()

def update():
    global screen, add, mainloop, closed, move, deltaX, deltaY, mousePos, pMousePos, letsMove, currentCursor, inserted, fullscreen, current_screen_w, current_screen_h, background

    for event in pygame.event.get():
        
        if event.type == QUIT:
            mainloop = False
            
        if event.type == KEYDOWN:

            # handling fullscreen
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    current_screen_w = FULLSCREEN_W
                    current_screen_h = FULLSCREEN_H
                    screen = pygame.display.set_mode((current_screen_w, current_screen_h), FULLSCREEN, 32)
                else:
                    current_screen_w = INIT_SCREEN_W
                    current_screen_h = INIT_SCREEN_H
                    screen = pygame.display.set_mode((current_screen_w, current_screen_h), 0, 32)
                background = pygame.Surface(screen.get_size())
                background = background.convert()
                background.fill(bg_color)
            if event.key == K_m:
                letsMove = not letsMove
        if event.type == MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            if not closed:
                add = True
            elif letsMove:
                for pos in polygonList:
                    dist = math.sqrt((mousePos[0]-pos[0]-deltaX)**2 + (mousePos[1]-pos[1]-deltaY)**2)
                    if dist <= REDIUS:
                        move = True
            elif not inserted:
                cursor = polygonList.first()
                pos = cursor.element()
                dist = math.sqrt((mousePos[0]-pos[0]-deltaX)**2 + (mousePos[1]-pos[1]-deltaY)**2)
                i = 1
                length = len(polygonList)
                while length > i and dist > REDIUS:
                    i += 1
                    cursor = polygonList.after(cursor)
                    pos = cursor.element()
                    dist = math.sqrt((mousePos[0]-pos[0]-deltaX)**2 + (mousePos[1]-pos[1]-deltaY)**2)
                if dist <= REDIUS:
                    polygonList.add_after(cursor, (mousePos[0]-deltaX, mousePos[1]-deltaY))
                    currentCursor = polygonList.after(cursor)
                    inserted = True


        elif event.type == MOUSEBUTTONUP:
            if closed:
                move = False
                inserted = False

        if event.type == MOUSEMOTION:
            mousePos = pygame.mouse.get_pos()
            if move:
                deltaX += mousePos[0] - pMousePos[0]
                deltaY += mousePos[1] - pMousePos[1]
            if inserted:
                polygonList.replace(currentCursor, (mousePos[0]-deltaX, mousePos[1]-deltaY))
            pMousePos = mousePos

    if add:
        for pos in polygonList:
            dist = math.sqrt((mousePos[0]-pos[0])**2 + (mousePos[1]-pos[1])**2)
            if dist <= REDIUS:
                mousePos = pos
        polygonList.add_last(mousePos)
        add = False
        if len(polygonList) > 3:
            firstPos = polygonList.first().element()
            if mousePos == firstPos:
                closed = True

def draw():
    pPos = None
    ## circles and lines are separate so that lines are all underneath circles
    for pos in polygonList:
        pos = (pos[0] + deltaX, pos[1] + deltaY)
        if pPos != None:
            pygame.draw.line(screen, GREEN_COLOR, pPos, pos, 3)
        pPos = pos
    for pos in polygonList:
        pos = (pos[0] + deltaX, pos[1] + deltaY)
        pygame.draw.circle(screen, BLACK_COLOR, pos, REDIUS, 0)



main()
