import pygame
import os
from random import randint

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')
running = True
BG = pygame.transform.scale(pygame.image.load(os.path.join("bg.jpg")), (400,600))

BLUE = (13,184,252)
COPPER = (184,115,51)
RED = (255,0,0)
BLACK = (0,0,0)

clock = pygame.time.Clock()

TUBE_WIDTH = 50
TUBE_VELOCITY = 3
TUBE_GAP = 150

tube1_x = 600
tube2_x = 800
tube3_x = 1000

tube1_height = randint(100,400)
tube2_height = randint(100,400)
tube3_height = randint(100,400)
 
BIRD_x = 50
bird_y = 400
BIRD_WIDTH = 35
BIRD_HEIGHT = 35

bird_drop_velocity = 0
GRAVITY = 0.5

score = 0

font = pygame.font.SysFont('sans', 20)

tube1_pass = False
tube2_pass = False
tube3_pass = False

pausing = False
score_x = 5
score_y = 5
score_mark = False

bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

sound = pygame.mixer.Sound("ms.mp3") #download from internet !!!!!!!!!!

while running:
	clock.tick(60)
	screen.blit(BG,(0,0))

	# Draw tube
	tube1_rect = pygame.draw.rect(screen, COPPER, (tube1_x, 0, TUBE_WIDTH, tube1_height))
	tube2_rect = pygame.draw.rect(screen, COPPER, (tube2_x, 0, TUBE_WIDTH, tube2_height))
	tube3_rect = pygame.draw.rect(screen, COPPER, (tube3_x, 0, TUBE_WIDTH, tube3_height))

	#Draw tube inverse
	tube1_rect_inv = pygame.draw.rect(screen, COPPER, (tube1_x, tube1_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube1_height + TUBE_GAP))
	tube2_rect_inv = pygame.draw.rect(screen, COPPER, (tube2_x, tube2_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube2_height + TUBE_GAP))
	tube3_rect_inv = pygame.draw.rect(screen, COPPER, (tube3_x, tube3_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube3_height + TUBE_GAP))

	tube1_x -= TUBE_VELOCITY
	tube2_x -= TUBE_VELOCITY
	tube3_x -= TUBE_VELOCITY

	# draw beach
	beach_rect = pygame.draw.rect(screen, BLUE, (0,570,400,30))

	# draw bird
	bird_rect = screen.blit(bird_image, (BIRD_x, bird_y))

	# bird falls
	bird_y += bird_drop_velocity
	bird_drop_velocity += GRAVITY

	# generate new tubes
	if tube1_x < -TUBE_WIDTH:
		tube1_x = 550
		tube1_height = randint(100,400)
		tube1_pass = False
	if tube2_x < -TUBE_WIDTH:
		tube2_x = 550
		tube2_height = randint(100,400)
		tube2_pass = False
	if tube3_x < -TUBE_WIDTH:
		tube3_x = 550
		tube3_height = randint(100,400) 
		tube3_pass = False

	score_txt = font.render("Score: " + str(score), True, BLACK)
	screen.blit(score_txt, (score_x,score_y))
 
	# update score
	if tube1_x + TUBE_WIDTH <= BIRD_x and tube1_pass == False:
		score +=1
		tube1_pass = True
	if tube2_x + TUBE_WIDTH <= BIRD_x and tube2_pass == False:
		score +=1
		tube2_pass = True
	if tube3_x + TUBE_WIDTH <= BIRD_x and tube3_pass == False:
		score +=1
		tube3_pass = True

	#check collision
	for tube in [tube1_rect, tube2_rect, tube3_rect, tube1_rect_inv, tube2_rect_inv, tube3_rect_inv, beach_rect]:
		if bird_rect.colliderect(tube):
			pausing = True
			score_mark = True
			TUBE_VELOCITY = 0
			bird_drop_velocity = 0
			game_over_txt = font.render("Game Over, score: " +str(score), True, BLACK)
			screen.blit(game_over_txt, (120,230))
			press_space_txt = font.render("Press SPACE to continue", True, BLACK)
			screen.blit(press_space_txt, (120,330))
			score_y = 650

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			# reset
			if event.key == pygame.K_SPACE:
				if pausing:
					bird_y = 400
					TUBE_VELOCITY = 3
					tube1_x = 600
					tube2_x = 800
					tube3_x = 1000
					score = 0
					pausing = False
				bird_drop_velocity = 0
				bird_drop_velocity -= 10

				if score_mark:
					score_y = 5
					score_mark = False

		if event.type == pygame.QUIT:
			running = False
				
	pygame.display.flip()

pygame.quit()