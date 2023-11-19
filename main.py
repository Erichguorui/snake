import time
import pygame
import random

# initialize pygame
pygame.init()

# set screen and title
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("starving snake")

# define colour
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# define direction
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# define character
font = pygame.font.Font(None, 36)

# define snake
class Snake:
    def __init__(self):
        self.body = [(3, 10), (2, 10), (1, 10)]
        self.direction = RIGHT
        self.eat_flag = False
        self.score = 0
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if self.eat_flag:
            self.eat_flag = False
        else:
            self.body.pop()

    def grow(self):
        # tail = self.body[-1]
        # new_tail = (tail[0] - self.direction[0], tail[1] - self.direction[1])
        # self.body.append(new_tail)
        self.eat_flag = True
        self.score += 1
    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0]*20, segment[1]*20, 20, 20))

    def check_collision(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= 40 or head[1] < 0 or head[1] >= 30:
            return True
        return False

# define food
class Food:
    def __init__(self):
        self.position = (random.randint(1,38), random.randint(1,28))

    def spawn(self):
        self.position = (random.randint(1,38), random.randint(1,28))

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0]*20, self.position[1]*20, 20, 20))


snake = Snake()
food = Food()

clock = pygame.time.Clock()
game_over = False

pygame.key.stop_text_input()

while 1:
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type==pygame.KEYDOWN:
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and snake.direction != DOWN:
                    snake.direction = UP
                elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and snake.direction != UP:
                    snake.direction = DOWN
                elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and snake.direction != LEFT:
                    snake.direction = RIGHT

        snake.move()

        if snake.body[0] == food.position:
            snake.grow()
            food.spawn()
        # End if touch the wall
        if snake.check_collision():
            game_over=True

        screen.fill(WHITE)
        snake.draw()
        food.draw()

        score_text = font.render("Score: " + str(snake.score), True, GREEN)
        screen.blit(score_text, (10, 10))


        pygame.display.update()

        clock.tick(10+snake.score)

    font_game_over = pygame.font.Font(None, 72)
    game_over_text = font_game_over.render("GAME OVER", True, RED)

    font_restart = pygame.font.Font(None, 30)
    restart_text = font_restart.render("press <space> to restart", True, RED)

    score_text = font.render("Score: " + str(snake.score), True, GREEN)

    screen.fill(WHITE)
    screen.blit(game_over_text, (250, 200))
    screen.blit(score_text, (350, 300))
    screen.blit(restart_text, (280, 350))
    pygame.display.update()

    waiting_for_space = True
    while waiting_for_space:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting_for_space = False

    snake = Snake()
    food = Food()
    game_over = False
