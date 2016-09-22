# -*- coding:UTF-8 -*-  
import pygame
from pygame.locals import *
import random  
from sys import exit
from copy import deepcopy
  
board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

pygame.init()

score = 0

BOX_SIZE = 50
BOX_GAP = 5
TOP_GAP = 100
BOTTOM_GAP = 30
EDGE_GAP = 20
SCREEN_WIDTH = BOX_SIZE *4 + BOX_GAP * 5 + EDGE_GAP *2
SCREEN_HEIGHT = BOX_SIZE * 4 + BOX_GAP * 5 + TOP_GAP + BOTTOM_GAP
TEXT_HEIGHT  = int(BOX_SIZE * 0.35)
BLACK   = pygame.color.THECOLORS["black"]
GOLD    =  pygame.color.THECOLORS["gold"]
GRAY    = pygame.color.THECOLORS["gray41"]
FORESTGREEN = pygame.color.THECOLORS['forestgreen']

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("2048")

def draw_box(board):
	colors = {
		0 : (192, 192, 192), 
		2 : (176, 224, 230), 
		4 : (127, 255, 212), 
		8 : (135, 206, 235), 
		16 : (64, 224, 208),
		32 : (0, 255, 255), 
		64 : (0, 201, 87), 
		128 : (50, 205, 50), 
		256 : (34, 139, 34),
		512 : (0, 255, 127), 
		1024 : (61, 145, 64), 
		2048 : (48, 128, 20), 
		4096 : (65, 105, 255),
		8192 : (8, 46, 84), 
		16384 : (11, 23, 70), 
		32768 : (25, 25, 112), 
		65536 : (0, 0, 255)}
	x, y = EDGE_GAP, TOP_GAP
	size = BOX_SIZE * 4 + BOX_GAP * 5
	pygame.draw.rect(screen, BLACK, (x, y, size, size))
	x, y = x + BOX_GAP, y + BOX_GAP
	for i in range(4):
		for j in range(4):
			idx = board[i][j]
			if idx == 0:
				text = ""
			else:
				text = str(idx)
			if idx > 65536: 
				idx = 65536
			color = colors[idx] 
			pygame.draw.rect(screen, color, (x, y, BOX_SIZE, BOX_SIZE))
			my_font = pygame.font.SysFont("arial", 32)
			text_surface = my_font.render(text, True, (255, 255, 255))
			text_rect = text_surface.get_rect()
			text_rect.center = (x + BOX_SIZE / 2, y + BOX_SIZE /2)
			screen.blit(text_surface, text_rect)
			x += BOX_SIZE + BOX_GAP
		x = EDGE_GAP + BOX_GAP
		y += BOX_SIZE + BOX_GAP

def write(msg="pygame is cool", color= BLACK, height = 14):    
	myfont = pygame.font.SysFont("None", 32)
	mytext = myfont.render(msg, True, color)
	mytext = mytext.convert_alpha()
	return mytext
  
def add_num(board):  
	k = 2 if random.randrange(0, 10) > 1 else 4
	s = divmod(random.randrange(0, 16), 4)
        if board[s[0]][s[1]] == 0:
            board[s[0]][s[1]] = k

def init_board(board):
	for i in range(2):
		add_num(board)

def check(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
    for i in range(4):
    	for j in range(3):
    		if board[i][j] == board[i][j+1]:
    			return False
    		if board[j][i] == board[j+1][i]:
    			return False
    return True
  
def move_left(board):
	global score
	for i in range(4):
		for j in [0, 1, 2, 3]:
			for k in [0, 1, 2]:
				if board[j][k] == 0:
					board[j][k] = board[j][k+1]
					board[j][k+1] = 0
				if board[j][k] == board[j][k+1]:
					board[j][k] *= 2
					score += board[j][k]
					board[j][k+1] = 0

def move_right(board):
	global score
	for row in board:
		for i in range(4):
			for j in [0, 1, 2, 3]:
				for k in [1, 2, 3]:
					if board[j][k] == 0:
						board[j][k] = board[j][k-1]
						board[j][k-1] = 0
					if board[j][k] == board[j][k-1]:
						board[j][k] *= 2
						score += board[j][k]
						board[j][k-1] = 0

def move_up(board):
	global score
	for i in range(4):
		for j in [0, 1, 2, 3]:
			for k in [0, 1, 2]:
				if board[k][j] == 0:
					board[k][j] = board[k+1][j]
					board[k+1][j] = 0
				if board[k][j] == board[k+1][j]:
					board[k][j] *= 2
					score += board[k][j]
					board[k+1][j] = 0

def move_down(board):
	global score
	for i in range(4):
		for j in [0, 1, 2, 3]:
			for k in [1, 2, 3]:
				if board[k][j] == 0:
					board[k][j] = board[k-1][j]
					board[k-1][j] = 0
				if board[k][j] == board[k-1][j]:
					board[k][j] *= 2
					score += board[k][j]
					board[k-1][j] = 0

def main(board):
	global score
	init_board(board)
	newboard = deepcopy(board)
	gameover = check(board)

	draw_box(board)
	screen.blit(write("2048", height = 40, color = GOLD), (EDGE_GAP, EDGE_GAP // 2))

	screen.blit(write("SCORE", height=14, color=FORESTGREEN), (EDGE_GAP+120, EDGE_GAP//2 + 5))
	rect1 = pygame.draw.rect(screen, FORESTGREEN, (EDGE_GAP+125, EDGE_GAP//2 + 30, 60, 20))
	text1 = write(str(score), height=14, color=GOLD)
	text1_rect = text1.get_rect()
	text1_rect.center = (EDGE_GAP+100+30, EDGE_GAP//2 + 40)
	screen.blit(text1, text1_rect)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.display.quit()
			elif not gameover:
				if event.type == KEYUP and event.key == K_UP:
					move_up(board)
				elif event.type == KEYUP and event.key == K_DOWN:
					move_down(board)
				elif event.type == KEYUP and event.key == K_LEFT:
					move_left(board)
				elif event.type == KEYUP and event.key == K_RIGHT:
					move_right(board)
				if newboard != board:
					add_num(board)
					newboard = deepcopy(board)
					draw_box(board)
				gameover = check(board)

				rect1 = pygame.draw.rect(screen, FORESTGREEN, (EDGE_GAP+125, EDGE_GAP//2 + 30, 60, 20))
				text1 = write(str(score), height=14, color=GOLD)
				text_rect = text1.get_rect()
				text_rect.center = (EDGE_GAP+125+30, EDGE_GAP//2 + 40)
				screen.blit(text1, text_rect)

			else:
				screen.blit(write("Game Over!", height = 40, color = FORESTGREEN), (EDGE_GAP, SCREEN_HEIGHT // 2))

		pygame.display.update()

if __name__ == "__main__":
    main(board)