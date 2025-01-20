import pygame
import random
import os

# Constants
TILE_SIZE = 64
GRID_SIZE = 8
WINDOW_WIDTH = GRID_SIZE * TILE_SIZE
WINDOW_HEIGHT = GRID_SIZE * TILE_SIZE
FPS = 60

# Colors for debugging (optional)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Three-in-a-Row Game with Icons")
clock = pygame.time.Clock()

# Load images
def load_images():
    image_folder = "images"  # Folder where images are stored
    images = {
        "red": pygame.image.load(os.path.join(image_folder, "red.png")),
        "green": pygame.image.load(os.path.join(image_folder, "green.png")),
        "blue": pygame.image.load(os.path.join(image_folder, "blue.png")),
        "yellow": pygame.image.load(os.path.join(image_folder, "yellow.png")),
    }
    # Scale images to TILE_SIZE
    for key in images:
        images[key] = pygame.transform.scale(images[key], (TILE_SIZE, TILE_SIZE))
    return images

images = load_images()

# Generate the initial grid
def generate_grid():
    return [[random.choice(list(images.keys())) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Draw the grid
def draw_grid(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile = grid[row][col]
            screen.blit(images[tile], (col * TILE_SIZE, row * TILE_SIZE))

# Check for matches
def find_matches(grid):
    matches = []
    # Check rows
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                matches.append((row, col))
                matches.append((row, col + 1))
                matches.append((row, col + 2))
    # Check columns
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                matches.append((row, col))
                matches.append((row + 1, col))
                matches.append((row + 2, col))
    return list(set(matches))

# Remove matches and fill empty spaces
def remove_and_refill(grid, matches):
    for (row, col) in matches:
        grid[row][col] = None  # Mark the tile as empty
    # Let tiles fall down
    for col in range(GRID_SIZE):
        empty_slots = [row for row in range(GRID_SIZE) if grid[row][col] is None]
        if empty_slots:
            for row in reversed(range(GRID_SIZE)):
                if row < empty_slots[0]:
                    grid[row + len(empty_slots)][col] = grid[row][col]
                    grid[row][col] = None
            for i, row in enumerate(empty_slots):
                grid[row][col] = random.choice(list(images.keys()))  # Fill empty spaces

# Main game loop
def main():
    grid = generate_grid()
    score = 0

    running = True
    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Check for matches
        matches = find_matches(grid)
        if matches:
            score += len(matches) * 10  # Increase score
            remove_and_refill(grid, matches)

        draw_grid(grid)
        
        # Display score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()