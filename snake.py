import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.image = pygame.image.load("apple.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH//GRID_SIZE)-1) * GRID_SIZE,
                         random.randint(0, (HEIGHT//GRID_SIZE)-1) * GRID_SIZE)

    def render(self, surface):
        surface.blit(self.image, self.position)

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
        self.tail_position = self.positions[-1]  # Initialize tail position at the end of the snake
        self.score = 0  # Initialize score
        self.food = food  # Reference to the food object

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*GRID_SIZE)) % WIDTH), (cur[1] + (y*GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.tail_position = self.positions.pop()
        
        # Update score when snake eats food
        if self.get_head_position() == self.food.position:
            self.score += 1
            self.length += 1
            self.food.randomize_position()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.tail_position = self.positions[-1]  # Reset tail position

    def render(self, surface):
        head_image = self.head_images[self.direction]
        surface.blit(head_image, self.positions[0])
        for i, p in enumerate(self.positions[1:]):
            prev = self.positions[i]
            next = self.positions[i + 2] if i < len(self.positions) - 2 else self.positions[-1]
            if prev[1] == next[1]:  # Horizontal body segment
                body_image = self.body_images[(LEFT, RIGHT)]
            elif prev[0] == next[0]:  # Vertical body segment
                body_image = self.body_images[(UP, DOWN)]
            elif (prev[0] - p[0] == -GRID_SIZE and next[1] - p[1] == -GRID_SIZE) or (next[0] - p[0] == -GRID_SIZE and prev[1] - p[1] == -GRID_SIZE):  # Top-left corner
                body_image = self.body_images[(UP, LEFT)]
            elif (prev[0] - p[0] == GRID_SIZE and next[1] - p[1] == -GRID_SIZE) or (next[0] - p[0] == GRID_SIZE and prev[1] - p[1] == -GRID_SIZE):  # Top-right corner
                body_image = self.body_images[(UP, RIGHT)]
            elif (prev[0] - p[0] == -GRID_SIZE and next[1] - p[1] == GRID_SIZE) or (next[0] - p[0] == -GRID_SIZE and prev[1] - p[1] == GRID_SIZE):  # Bottom-left corner
                body_image = self.body_images[(DOWN, LEFT)]
            elif (prev[0] - p[0] == GRID_SIZE and next[1] - p[1] == GRID_SIZE) or (next[0] - p[0] == GRID_SIZE and prev[1] - p[1] == GRID_SIZE):  # Bottom-right corner
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

# Main function
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    food = Food()  # Instantiate food object
    snake = Snake(food)  # Pass food object to Snake class

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    snake.direction = RIGHT

        snake.update()

        surface.fill(BLACK)
        snake.render(surface)
        food.render(surface)
        
        # Display score on the screen
        font = pygame.font.SysFont("arial", 24)
        score_text = font.render(f"Score: {snake.score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        
        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
