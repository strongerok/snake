from random import randint

import pygame

# Define the background colour
# using RGB color coding.
WHITE = (255, 255, 255)

BACKGROUND = (0, 0, 0)
DISPLAY = (600, 600)
DELAY = 100
SNAKE = (0, 255, 0)
FOOD = (255, 255, 255)

screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
screen.fill(BACKGROUND)
pygame.display.update()
running = True

tick_event = pygame.USEREVENT + 1
pygame.time.set_timer(tick_event, DELAY)


def center(arr):
    return [arr[0] + 15, arr[1] + 15]


def gameOverScreen(Score):
    ending = 1
    global running, gameover

    screen.fill(BACKGROUND)
    font = pygame.font.SysFont('Comic Sans MS', 30)
    endtext = font.render("You lost!", True, WHITE)
    screen.blit(endtext, [220, 230])
    kill = font.render("Score: " + str(Score), True, WHITE)
    screen.blit(kill, (220, 280))

    pygame.display.flip()
    clock.tick(100)


if __name__ == '__main__':
    snake_body = {
        "0": [60, 0],
        "1": [30, 0],
        "2": [0, 0],
    }
    size = 3
    food_coords = [15 + 30*randint(1, 20), 15 + 30*randint(1, 20)]
    score = 0
    steps_in_dir = {
        "RIGHT": [30, 0],
        "DOWN": [0, 30],
        "LEFT": [-30, 0],
        "UP": [0, -30],
    }
    move_dir = "RIGHT"

    pygame.font.init()

    # game loop
    while running:
        clock.tick(100)
        # for loop through the event queue
        for event in pygame.event.get():
            pygame.display.update()
            # Check for QUIT event
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if move_dir == "UP" or move_dir == "DOWN":
                        move_dir = "LEFT"
                if event.key == pygame.K_RIGHT:
                    if move_dir == "UP" or move_dir == "DOWN":
                        move_dir = "RIGHT"
                if event.key == pygame.K_UP:
                    if move_dir == "LEFT" or move_dir == "RIGHT":
                        move_dir = "UP"
                if event.key == pygame.K_DOWN:
                    if move_dir == "LEFT" or move_dir == "RIGHT":
                        move_dir = "DOWN"
            elif event.type == tick_event:
                screen.fill(BACKGROUND)
                pygame.draw.circle(screen, FOOD, food_coords, 5)

                font = pygame.font.SysFont('Comic Sans MS', 30)
                score_text = font.render("Score: " + str(score), True, WHITE)
                screen.blit(score_text, [0, 0])

                if len(list(snake_body.values())) != len(set([tuple(i) for i in snake_body.values()])):
                    gameOverScreen(score)
                    continue

                collide = pygame.Rect(*snake_body["0"], 30, 30).collidepoint(food_coords)
                if collide:
                    snake_body[str(size)] = [sum(i) for i in zip(snake_body[str(size-1)][:], [i*(-1) for i in steps_in_dir[move_dir]])]
                    size += 1
                    score += 1
                    while food_coords in [center(i) for i in snake_body.values()]:
                        food_coords = [15 + 30 * randint(1, 19), 15 + 30 * randint(1, 19)]
                        pygame.draw.circle(screen, FOOD, food_coords, 5)
                for i in range(size):
                    pygame.draw.rect(screen, SNAKE, (*snake_body[str(i)], 30, 30))
                for j in range(size - 1, 0, -1):
                    snake_body[str(j)] = snake_body[str(j - 1)][:]
                snake_body["0"] = [sum(i) for i in zip(snake_body["0"], steps_in_dir[move_dir])]
                if snake_body["0"][0] > 599:
                    snake_body["0"][0] -= 600
                elif snake_body["0"][1] > 599:
                    snake_body["0"][1] -= 600
                elif snake_body["0"][0] < 0:
                    snake_body["0"][0] += 600
                elif snake_body["0"][1] < 0:
                    snake_body["0"][1] += 600