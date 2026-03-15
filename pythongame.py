# Import necessary modules for the game
import pygame
import sys
import random

# Initialize Pygame to start the game engine
pygame.init()

# Define constants for the game window and colors
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GREEN = (0, 128, 0)  # Color for the pitch
WHITE = (255, 255, 255)  # Color for lines and ball
BLACK = (0, 0, 0)  # Color for players

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("1v1 Arcade Top-Down Football")

# Clock to control the game's frame rate
clock = pygame.time.Clock()

# Player class to represent each player in the game - players move only up and down like goalkeepers
class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 5  # How fast the player moves vertically
        self.direction = 0  # -1 for up, 1 for down, 0 for stop

    def move(self):
        self.y += self.direction * self.speed
        # Keep player within screen bounds - can't go off the top or bottom
        if self.y < 0:
            self.y = 0
        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Ball class to represent the football - starts with random direction and bounces off walls and players
class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = random.choice([-3, 3])  # Random initial left/right direction
        self.speed_y = random.choice([-3, 3])  # Random initial up/down direction

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off top and bottom walls - reverses vertical direction
        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
            self.speed_y = -self.speed_y

    def check_collision(self, player):
        # Simple collision detection with player - if ball hits player, it bounces back horizontally
        if (self.x - self.radius < player.x + player.width and
            self.x + self.radius > player.x and
            self.y - self.radius < player.y + player.height and
            self.y + self.radius > player.y):
            self.speed_x = -self.speed_x  # Bounce back

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Create player and ball objects - player1 on left (W/S keys), player2 on right (arrow keys), ball in center
player1 = Player(50, 150, 20, 100, BLACK)  # Left player
player2 = Player(730, 150, 20, 100, BLACK)  # Right player
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, WHITE)

# Score variables
score1 = 0
score2 = 0
font = pygame.font.Font(None, 36)

# Main game loop - the heartbeat of the game, running continuously
running = True
while running:
    # Phase 1: Event Handling - Listen for user inputs and system events (W/S for player1 up/down, arrows for player2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1.direction = -1  # Move up
            elif event.key == pygame.K_s:
                player1.direction = 1   # Move down
            elif event.key == pygame.K_UP:
                player2.direction = -1  # Move up
            elif event.key == pygame.K_DOWN:
                player2.direction = 1   # Move down
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                player1.direction = 0  # Stop moving
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                player2.direction = 0  # Stop moving

    # Phase 2: Game Logic/State Updates - Update positions, check collisions, handle scoring (ball resets to center on goal)
    player1.move()
    player2.move()
    ball.move()
    ball.check_collision(player1)
    ball.check_collision(player2)

    # Check for scoring - if ball goes past left edge, player2 scores; past right, player1 scores
    if ball.x < 0:
        score2 += 1
        ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, WHITE)  # Reset ball
    elif ball.x > SCREEN_WIDTH:
        score1 += 1
        ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, WHITE)  # Reset ball

    # Phase 3: Rendering - Draw everything to the screen (green pitch, white lines, players, ball, scores)
    screen.fill(GREEN)  # Draw the pitch

    # Draw pitch lines - center line, circle, and goal lines like a soccer field
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)  # Center line
    pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 50, 2)  # Center circle
    pygame.draw.line(screen, WHITE, (0, 0), (0, SCREEN_HEIGHT), 5)  # Left goal line
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), 5)  # Right goal line

    # Draw players and ball
    player1.draw(screen)
    player2.draw(screen)
    ball.draw(screen)

    # Draw scores
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 50, 10))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame when the loop ends
pygame.quit()
sys.exit()