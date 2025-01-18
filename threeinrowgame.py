import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Three in a Row with Score and Mechanics")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Grid settings
GRID_SIZE = 5  # 8x8 grid
TILE_SIZE = SCREEN_WIDTH // GRID_SIZE

# Define colors for the tiles
COLOR_MAP = {
    0: (255, 255, 255),  # White for empty
    1: (255, 0, 0),      # Red
    2: (0, 255, 0),      # Green
    3: (0, 0, 255),      # Blue
    4: (255, 255, 0),    # Yellow
}

# Initialize grid with random colors
def create_grid():
    return [[random.randint(1, len(COLOR_MAP) - 1) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Draw the grid
def draw_grid(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = COLOR_MAP.get(grid[row][col], BLACK)  # Default to black if color is missing
            pygame.draw.rect(
                screen,
                color,
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
            )
            pygame.draw.rect(
                screen,
                BLACK,
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                2,  # Border thickness
            )

# Draw HUD
def draw_hud(score, moves_left, target_score, game_over):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    moves_text = font.render(f"Moves Left: {moves_left}", True, BLACK)
    target_text = font.render(f"Target: {target_score}", True, BLACK)

    # Display game status
    screen.blit(score_text, (10, 10))
    screen.blit(moves_text, (10, 50))
    screen.blit(target_text, (10, 90))

    if game_over:
        game_over_text = "You Win!" if score >= target_score else "Game Over!"
        game_over_display = font.render(game_over_text, True, BLACK)
        screen.blit(game_over_display, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20))

# Check for matches
def check_matches(grid):
    matched_positions = set()

    # Horizontal matches
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2] != 0:
                matched_positions.update([(row, col), (row, col + 1), (row, col + 2)])

    # Vertical matches
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col] != 0:
                matched_positions.update([(row, col), (row + 1, col), (row + 2, col)])

    return matched_positions

# Remove matches and drop new tiles
def resolve_matches(grid, matched_positions):
    for row, col in matched_positions:
        grid[row][col] = 0  # Set matched tiles to empty

    # Drop new tiles into empty spaces
    for col in range(GRID_SIZE):
        column_tiles = [grid[row][col] for row in range(GRID_SIZE) if grid[row][col] != 0]
        empty_count = GRID_SIZE - len(column_tiles)
        new_column = [0] * empty_count + column_tiles
        for row in range(GRID_SIZE):
            grid[row][col] = new_column[row]

    # Fill empty spaces at the top with new random tiles
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                grid[row][col] = random.randint(1, len(COLOR_MAP) - 1)

# Swap two tiles
def swap_tiles(grid, pos1, pos2):
    grid[pos1[0]][pos1[1]], grid[pos2[0]][pos2[1]] = grid[pos2[0]][pos2[1]], grid[pos1[0]][pos1[1]]

# Check if two tiles are adjacent
def are_adjacent(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1

# Main game loop
def main():
    grid = create_grid()
    clock = pygame.time.Clock()
    running = True

    # Game variables
    score = 0
    target_score = 1000
    moves_left = 20
    game_over = False

    selected_tile = None  # Store the first selected tile

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = event.pos
                col = mouse_x // TILE_SIZE
                row = mouse_y // TILE_SIZE

                if selected_tile is None:
                    selected_tile = (row, col)  # Select the first tile
                else:
                    if are_adjacent(selected_tile, (row, col)):
                        # Swap tiles
                        swap_tiles(grid, selected_tile, (row, col))
                        matched_positions = check_matches(grid)
                        if matched_positions:
                            resolve_matches(grid, matched_positions)
                            score += len(matched_positions) * 10  # Add points for matches
                            moves_left -= 1 
                        else:
                            # If no match, swap back
                            swap_tiles(grid, selected_tile, (row, col))
                            moves_left -= 1  # Deduct a move
                    selected_tile = None  # Reset selection

        # Check win/lose conditions
        if moves_left <= 0 or score >= target_score:
            game_over = True

        # Draw everything
        screen.fill(WHITE)
        draw_grid(grid)
        draw_hud(score, moves_left, target_score, game_over)

        # Highlight the selected tile
        if selected_tile is not None:
            pygame.draw.rect(
                screen,
                (0, 255, 255),  # Cyan highlight
                (selected_tile[1] * TILE_SIZE, selected_tile[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                5,  # Border thickness
            )

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()