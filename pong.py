import sys
import numpy
import pygame

#----------------------------------------------------------------------------
#CONSTANTS AND VARIABLES

# frame rate
FPS = 60

# window size
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# paddle size
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60

# distance from paddle to buffer
PADDLE_BUFFER = 10

# boundaries
TOP_BOUNDARY = 0
BOTTOM_BOUNDARY = WINDOW_HEIGHT - PADDLE_HEIGHT
LEFT_BOUNDARY = PADDLE_BUFFER + PADDLE_WIDTH
RIGHT_BOUNDARY = WINDOW_WIDTH - PADDLE_BUFFER - PADDLE_WIDTH

# ball size
BALL_SIZE = 10

# speeds
PADDLE_SPEED = 2
BALL_X_SPEED = 3
BALL_Y_SPEED = 2

# RGB colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# screen for game
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#----------------------------------------------------------------------------
#METHODS

# draws ball
def drawBall(ball_x, ball_y):
	ball = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)
	pygame.draw.rect(screen, WHITE, ball)


# draws paddles
# set 'left' flag to 1 for left paddle
def drawPaddle(paddle_y, left):
	paddle = None
	if left:
		paddle = pygame.Rect(PADDLE_BUFFER, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
	else:
		paddle = pygame.Rect(RIGHT_BOUNDARY, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
	pygame.draw.rect(screen, WHITE, paddle)


def drawScore(score):
	font = pygame.font.Font(None, 36)
	text = font.render("%d : %d" % (score[0], score[1]), 1, WHITE)
	textPos = text.get_rect(centerx = WINDOW_WIDTH/2, centery = 20)
	screen.blit(text, textPos)


# update ball image
def updateBall(ball_x, ball_y, ball_x_dir, ball_y_dir, l_paddle_y, r_paddle_y):
	score = numpy.array([0, 0])
	ball_x += ball_x_dir * BALL_X_SPEED
	ball_y += ball_y_dir * BALL_Y_SPEED

	#collisions on left and right sides
	if (ball_x <= LEFT_BOUNDARY) and (ball_y + BALL_SIZE >= l_paddle_y) and (ball_y <= l_paddle_y + PADDLE_HEIGHT):
		ball_x_dir = 1
	elif (ball_x >= RIGHT_BOUNDARY) and (ball_y + BALL_SIZE >= r_paddle_y) and (ball_y <= r_paddle_y + PADDLE_HEIGHT):
		ball_x_dir = -1
	elif ball_x <= 0:
		score[1] += 1
		ball_x_dir = 1
	elif ball_x >= WINDOW_WIDTH - BALL_SIZE:
		score[0] += 1
		ball_x_dir = -1

	#collisions on top and bottom
	if ball_y <= 0:
		ball_y = 0
		ball_y_dir = 1
	elif ball_y + BALL_SIZE >= WINDOW_HEIGHT:
		ball_y = WINDOW_HEIGHT - BALL_SIZE
		ball_y_dir = -1

	return [score, ball_x, ball_y, ball_x_dir, ball_y_dir]


# update paddle images
# left is user, right is computer
def updatePaddle(paddle_y, ball_y, action, left):
	if left:
		# move up
		if action[0] == 1:
			paddle_y -= PADDLE_SPEED
		# move down
		elif action[1] == 1:
			paddle_y += PADDLE_SPEED
	else:
		if (paddle_y + PADDLE_HEIGHT/2) > (ball_y + BALL_SIZE/2):
			paddle_y -= PADDLE_SPEED
		else:
			paddle_y += PADDLE_SPEED

	#prevent from going out of bounds
	if paddle_y <= TOP_BOUNDARY:
		paddle_y = TOP_BOUNDARY
	elif paddle_y >= BOTTOM_BOUNDARY:
		paddle_y = BOTTOM_BOUNDARY

	return paddle_y

#----------------------------------------------------------------------------
#CLASS

# class for pong game
class PongGame:

	# intitalize game
	def __init__(self):
		self.score = numpy.array([0,0])
		self.l_paddle_y = WINDOW_HEIGHT/2 - PADDLE_HEIGHT/2
		self.r_paddle_y = WINDOW_HEIGHT/2 - PADDLE_HEIGHT/2
		self.ball_x = WINDOW_WIDTH/2 - BALL_SIZE/2
		self.ball_y = WINDOW_HEIGHT/2 - BALL_SIZE/2
		self.ball_x_dir = numpy.random.choice([1, -1], 1)
		self.ball_y_dir = numpy.random.choice([1, -1], 1)


	def getFirstFrame(self):
		pygame.event.pump()
		screen.fill(BLACK)
		drawPaddle(self.l_paddle_y, True)
		drawPaddle(self.r_paddle_y, False)
		drawBall(self.ball_x, self.ball_y)
		drawScore(self.score)
		pygame.display.flip()


	def getNextFrame(self, action):
		pygame.event.pump()
		addedScore = None
		screen.fill(BLACK)
		self.l_paddle_y = updatePaddle(self.l_paddle_y, self.ball_y, action, True)
		drawPaddle(self.l_paddle_y, True)
		self.r_paddle_y = updatePaddle(self.r_paddle_y, self.ball_y, action, False)
		drawPaddle(self.r_paddle_y, False)
		[addedScore, self.ball_x, self.ball_y, self.ball_x_dir, self.ball_y_dir] = \
			updateBall(self.ball_x, self.ball_y, self.ball_x_dir, self.ball_y_dir, self.l_paddle_y, self.r_paddle_y)
		drawBall(self.ball_x, self.ball_y)
		self.score += addedScore
		drawScore(self.score)
		pygame.display.flip()

#----------------------------------------------------------------------------
#MAIN

def main():
	pygame.init()
	game = PongGame()
	game.getFirstFrame()
	while True:
		action = [0,0]
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			action[0] = 1
		if keys[pygame.K_DOWN]:
			action[1] = 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		game.getNextFrame(action)	


if __name__ == "__main__": main()
