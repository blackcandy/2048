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
def init():
	global screen
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
	pool = []
	k = 2 if random.randrange(0, 10) > 1 else 4
	for i in range(4):
		for j in range(4):
			if board[i][j] == 0:
				pool.append([i, j])
	s = random.choice(pool)
	board[s[0]][s[1]] = k
	s = divmod(random.randrange(0, 16), 4)

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
	v = deepcopy(board)
	for i in range(4):
		for j in [0, 1, 2, 3]:
			for k in [0, 1, 2]:
				if v[j][k] == 0:
					v[j][k] = v[j][k+1]
					v[j][k+1] = 0
				if v[j][k] == v[j][k+1]:
					v[j][k] *= 2
					score += v[j][k]
					v[j][k+1] = 0
	return v

def move_right(board):
	global score
	v = deepcopy(board)
	for i in range(4):
		for j in [0, 1, 2, 3]:
			for k in [3, 2, 1]:
				if v[j][k] == 0:
					v[j][k] = v[j][k-1]
					v[j][k-1] = 0
				if v[j][k] == v[j][k-1]:
					v[j][k] *= 2
					score += v[j][k]
					v[j][k-1] = 0
	return v

def move_up(board):
	global score
	v = deepcopy(board)
	for i in range(4):
		for j in [0, 1, 2, 3]:
			for k in [0, 1, 2]:
				if v[k][j] == 0:
					v[k][j] = v[k+1][j]
					v[k+1][j] = 0
				if v[k][j] == v[k+1][j]:
					v[k][j] *= 2
					score += v[k][j]
					v[k+1][j] = 0
	return v

def move_down(board):
	global score
	v = deepcopy(board)
	for i in range(4):
		for j in [0, 1, 2, 3]:
			for k in [3, 2, 1]:
				if v[k][j] == 0:
					v[k][j] = v[k-1][j]
					v[k-1][j] = 0
				if v[k][j] == v[k-1][j]:
					v[k][j] *= 2
					score += v[k][j]
					v[k-1][j] = 0
	return v

def main(board):
	global score
	init()
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
					board = move_up(board)
				elif event.type == KEYUP and event.key == K_DOWN:
					board = move_down(board)
				elif event.type == KEYUP and event.key == K_LEFT:
					board = move_left(board)
				elif event.type == KEYUP and event.key == K_RIGHT:
					board = move_right(board)
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


# AI for game 2048
def display(board):
	print('{0:4} {1:4} {2:4} {3:4}'.format(board[0][0], board[0][1], board[0][2], board[0][3]))
	print('{0:4} {1:4} {2:4} {3:4}'.format(board[1][0], board[1][1], board[1][2], board[1][3]))
	print('{0:4} {1:4} {2:4} {3:4}'.format(board[2][0], board[2][1], board[2][2], board[2][3]))
	print('{0:4} {1:4} {2:4} {3:4}'.format(board[3][0], board[3][1], board[3][2], board[3][3]))

def ai(board):
	global score
	init_board(board)
	newboard = deepcopy(board)
	gameover = check(board)
	number = 0
	while not gameover:
		board = get_min_smooth(board)
		if newboard == board:
			board = random.choice([move_left(board), move_right(board), move_up(board), move_down(board)])

		if newboard != board:
			add_num(board)
			newboard = deepcopy(board)
		elif newboard == board:
			break
		gameover = check(board)
		print number
		number += 1
		
		

		display(board)
		print smooth_price(board)
	pool = []
	for i in range(4):
		for j in range(4):
			pool.append(board[i][j])
	max_cell = max(pool)
	print max_cell
	

def smooth_price(board):
	smooth = 0
	for i in range(4):
		smooth += abs(board[i][0] - board[i][1]) + abs(board[i][1] - board[i][2]) + abs(board[i][2] - board[i][3])
	for j in range(4):
		smooth += abs(board[0][j] - board[1][j]) + abs(board[1][j] - board[2][j]) + abs(board[2][j] - board[3][j])
	return smooth

def get_min_smooth(board):
	next_step = [move_left(board), move_right(board), move_up(board), move_down(board)]
	my_list = map(smooth_price, next_step)
	min_smooth = my_list[0]
	for i in my_list:
		if i < min_smooth:
			min_smooth = i
	x = my_list.index(min_smooth)
	return next_step[x]


if __name__ == "__main__":
    main(board)
    # ai(board)