import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
FPS = 10

# Colors
LIGHT_BROWN = (205, 133, 63)
DARK_BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game States
RUNNING = 0
GAME_OVER = 1

# Snake class
class Snake:
    def __init__(self, food):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.head_images = {
            UP: pygame.transform.scale(pygame.image.load("head_up.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)),
            DOWN: pygame.transform.scale(pygame.image.load("head_down.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)),
            LEFT: pygame.transform.scale(pygame.image.load("head_left.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)),
            RIGHT: pygame.transform.scale(pygame.image.load("head_right.png").convert_alpha(), (GRID_SIZE, GRID_SIZE))
        }
        self.tail_images = {
            DOWN: pygame.transform.scale(pygame.image.load("tail_up.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)),
            UP: pygame.transform.scale(pygame.image.load("tail_down.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)),
            RIGHT: pygame.transform.scale(pygame.image.load("tail_left.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)),
            LEFT: pygame.transform.scale(pygame.image.load("tail_right.png").convert_alpha(), (GRID_SIZE, GRID_SIZE))
        }
        self.body_images = {
            (UP, DOWN): pygame.transform.scale(pygame.image.load("body_vertical.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)),
            (LEFT, RIGHT): pygame.transform.scale(pygame.image.load("body_horizontal.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)),
            (UP, RIGHT): pygame.transform.scale(pygame.image.load("body_topright.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)),
            (UP, LEFT): pygame.transform.scale(pygame.image.load("body_topleft.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)),
            (DOWN, RIGHT): pygame.transform.scale(pygame.image.load("body_bottomright.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)),
            (DOWN, LEFT): pygame.transform.scale(pygame.image.load("body_bottomleft.png").convert_alpha(), (GRID_SIZE, GRID_SIZE))
        }
        self.body_image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.body_image.fill(WHITE)
        self.tail_position = self.positions[-1]
        self.food = food
        self.score = 0
        self.state = RUNNING

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        if self.state == RUNNING:
            cur = self.get_head_position()
            x, y = self.direction
            new = (((cur[0] + (x*GRID_SIZE)) % WIDTH), (cur[1] + (y*GRID_SIZE)) % HEIGHT)

            if new == self.food.position:
                if self.score % 5 == 0 and self.score != 0:
                    self.food.randomize_position()
                    self.score += 2
                else:
                    self.length += 1
                    self.score += 1
                    self.food.randomize_position()
            
            # Check for Bapple collision
            elif new == self.bapple.position:
                self.score -= 5  # Deduct 5 points
                self.bapple.randomize_position(self)
                
            else:
                if len(self.positions) > 2 and new in self.positions[2:]:
                    self.state = GAME_OVER
                else:
                    self.positions.insert(0, new)
                    if len(self.positions) > self.length:
                        self.tail_position = self.positions.pop()

            if new[0] < GRID_SIZE or new[0] >= WIDTH - GRID_SIZE or new[1] < GRID_SIZE or new[1] >= HEIGHT - GRID_SIZE:
                self.state = GAME_OVER

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.tail_position = self.positions[-1]
        self.score = 0
        self.state = RUNNING

    def render(self, surface):
        pygame.draw.rect(surface, DARK_BROWN, [0, 0, WIDTH, GRID_SIZE])
        pygame.draw.rect(surface, DARK_BROWN, [0, 0, GRID_SIZE, HEIGHT])
        pygame.draw.rect(surface, DARK_BROWN, [0, HEIGHT - GRID_SIZE, WIDTH, GRID_SIZE])
        pygame.draw.rect(surface, DARK_BROWN, [WIDTH - GRID_SIZE, 0, GRID_SIZE, HEIGHT])
        
        head_image = self.head_images[self.direction]
        surface.blit(head_image, self.positions[0])
        for i, p in enumerate(self.positions[1:]):
            prev = self.positions[i]
            next = self.positions[i + 2] if i < len(self.positions) - 2 else self.positions[-1]
            if prev[1] == next[1]:
                body_image = self.body_images[(LEFT, RIGHT)]
            elif prev[0] == next[0]:
                body_image = self.body_images[(UP, DOWN)]
            elif (prev[0] - p[0] == -GRID_SIZE and next[1] - p[1] == -GRID_SIZE) or (next[0] - p[0] == -GRID_SIZE and prev[1] - p[1] == -GRID_SIZE):
                body_image = self.body_images[(UP, LEFT)]
            elif (prev[0] - p[0] == GRID_SIZE and next[1] - p[1] == -GRID_SIZE) or (next[0] - p[0] == GRID_SIZE and prev[1] - p[1] == -GRID_SIZE):
                body_image = self.body_images[(UP, RIGHT)]
            elif (prev[0] - p[0] == -GRID_SIZE and next[1] - p[1] == GRID_SIZE) or (next[0] - p[0] == -GRID_SIZE and prev[1] - p[1] == GRID_SIZE):
                body_image = self.body_images[(DOWN, LEFT)]
            elif (prev[0] - p[0] == GRID_SIZE and next[1] - p[1] == GRID_SIZE) or (next[0] - p[0] == GRID_SIZE and prev[1] - p[1] == GRID_SIZE):
                body_image = self.body_images[(DOWN, RIGHT)]
            surface.blit(body_image, p)
        tail_image = self.tail_images[self.get_tail_direction()]
        surface.blit(tail_image, self.tail_position)

    def get_tail_direction(self):
        tail_x, tail_y = self.tail_position
        prev_tail_x, prev_tail_y = self.positions[-2] if len(self.positions) > 1 else self.positions[-1]
        if tail_x < prev_tail_x:
            return RIGHT
        elif tail_x > prev_tail_x:
            return LEFT
        elif tail_y < prev_tail_y:
            return DOWN
        elif tail_y > prev_tail_y:
            return UP
        else:
            return self.direction

# Food class
class Food:
    def __init__(self, snake):
        self.position = (0, 0)
        self.image = pygame.image.load("apple.png").convert_alpha()
        self.super_image = pygame.image.load("Sapple.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.super_image = pygame.transform.scale(self.super_image, (GRID_SIZE, GRID_SIZE))
        self.snake = snake  # Store the snake instance
        self.randomize_position()

    def randomize_position(self):
        valid_positions = [(x, y) for x in range(GRID_SIZE, WIDTH - GRID_SIZE, GRID_SIZE)
                           for y in range(GRID_SIZE, HEIGHT - GRID_SIZE, GRID_SIZE)
                           if (x, y) not in self.snake.positions]
        self.position = random.choice(valid_positions)

    def render(self, surface, snake):
        if snake.score % 10 == 0 and snake.score > 0:
            surface.blit(self.super_image, self.position)
        else:
            surface.blit(self.image, self.position)

# Bapple class
class Bapple:
    def __init__(self, snake):
        self.position = (0, 0)
        self.image = pygame.image.load("Bapple.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.spawn_time = time.time()
        self.randomize_position(snake)

    def randomize_position(self, snake):
        valid_positions = [(x, y) for x in range(GRID_SIZE, WIDTH - GRID_SIZE, GRID_SIZE)
                           for y in range(GRID_SIZE, HEIGHT - GRID_SIZE, GRID_SIZE)
                           if (x, y) not in snake.positions]
        self.position = random.choice(valid_positions)
        self.spawn_time = time.time()

    def render(self, surface, snake):
        surface.blit(self.image, self.position)
        
        if time.time() - self.spawn_time > 3:
            self.randomize_position(snake)

# Button class
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = RED
        self.text = text

    def draw(self, surface, outline=None):
        if outline:
            pygame.draw.rect(surface, outline, self.rect, 0)
        
        pygame.draw.rect(surface, self.color, self.rect, 0)

        if self.text != "":
            font = pygame.font.SysFont("Arial", 20)
            text = font.render(self.text, True, BLACK)
            surface.blit(text, (self.rect.x + (self.rect.width // 2 - text.get_width() // 2),
                                self.rect.y + (self.rect.height // 2 - text.get_height() // 2)))

    def is_over(self, pos):
        return self.rect.collidepoint(pos)

# Main function
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake(None)
    food = Food(snake)  # Pass snake instance to Food
    bapple = Bapple(snake)  # Initialize Bapple
    snake.food = food  # Assign food instance to snake
    snake.bapple = bapple  # Assign bapple instance to snake

    play_again_button = Button(150, 350, 100, 50, "Play Again")  # Define play_again_button

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and snake.state == RUNNING:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT

        snake.update()

        surface.fill(LIGHT_BROWN)
        snake.render(surface)
        food.render(surface, snake)
        bapple.render(surface, snake)  # Render Bapple
        
        font = pygame.font.SysFont("Arial", 20)
        score_text = font.render(f"Score: {snake.score}", True, BLACK)
        surface.blit(score_text, (10, 10))

        if snake.state == GAME_OVER:
            font = pygame.font.SysFont("Arial", 30)
            game_over_text = font.render("Game Over", True, BLACK)
            surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
            play_again_button.draw(surface, BLACK)

            mouse_pos = pygame.mouse.get_pos()
            if play_again_button.is_over(mouse_pos):
                play_again_button.color = (255, 69, 0)
                if pygame.mouse.get_pressed()[0]:
                    snake.reset()

        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
