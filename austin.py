import pygame
import random
import os

# Game constants
TILE_SIZE = 64
GRID_SIZE = 8
WINDOW_WIDTH = GRID_SIZE * TILE_SIZE
WINDOW_HEIGHT = GRID_SIZE * TILE_SIZE + 50  # Extra space for score
FPS = 60
COLORS = ['red', 'green', 'blue', 'yellow']

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Match Three")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def load_images():
    images = {}
    for color in COLORS:
        try:
            img = pygame.image.load(f"images/{color}.png").convert_alpha()
            images[color] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        except Exception as e:
            print(f"Error loading {color} image: {e}")
            pygame.quit()
            exit()
    return images

class Game:
    def __init__(self):
        self.images = self.load_images()
        self.grid = self.create_grid()
        self.score = 0
        self.selected = None
        self.moves_left = 20
        self.hearts_collected = 0
        self.target_hearts = 15  # Set winning condition
        self.game_over = False

    def load_images(self):
        images = {}
        for color in COLORS:
            try:
                img = pygame.image.load(f"images/{color}.png").convert_alpha()
                images[color] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            except Exception as e:
                print(f"Error loading {color} image: {e}")
                pygame.quit()
                exit()
        return images

    def create_grid(self):
        """Create grid with no initial matches"""
        while True:
            grid = [[random.choice(COLORS) for _ in range(GRID_SIZE)] 
                   for _ in range(GRID_SIZE)]
            if not self.find_matches(grid):
                return grid

    def draw(self):
        screen.fill((255, 255, 255))
        
        # Draw grid
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                screen.blit(self.images[color], (x*TILE_SIZE, y*TILE_SIZE))
                
                if self.selected == (y, x):
                    pygame.draw.rect(screen, (255, 0, 0), 
                                   (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)
        
        # Draw game info
        info_y = GRID_SIZE * TILE_SIZE + 10
        font = pygame.font.Font(None, 44)
        
        moves_text = font.render(f"Moves: {self.moves_left}", True, (0, 0, 0))
        screen.blit(moves_text, (10, info_y))
        
        hearts_text = font.render(f"Hearts: {self.hearts_collected}/{self.target_hearts}", 
                                True, (255, 0, 0))
        screen.blit(hearts_text, (200, info_y))

        # Game over messages
        if self.game_over:
            text = "You Win!" if self.hearts_collected >= self.target_hearts else "Game Over!"
            color = (100, 100, 200) if self.hearts_collected >= self.target_hearts else (200, 0, 0)
            text_surf = font.render(text, True, color)
            text_rect = text_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            screen.blit(text_surf, text_rect)

    def find_matches(self, grid):
        matches = set()
        # Horizontal check
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE - 2):
                if grid[y][x] == grid[y][x+1] == grid[y][x+2]:
                    matches.update((y, x+i) for i in range(3))
        # Vertical check
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE - 2):
                if grid[y][x] == grid[y+1][x] == grid[y+2][x]:
                    matches.update((y+i, x) for i in range(3))
        return matches

    def swap_tiles(self, pos1, pos2):
        y1, x1 = pos1
        y2, x2 = pos2
        self.grid[y1][x1], self.grid[y2][x2] = self.grid[y2][x2], self.grid[y1][x1]
        
        if not self.find_matches(self.grid):
            self.grid[y1][x1], self.grid[y2][x2] = self.grid[y2][x2], self.grid[y1][x1]
            return False
        return True

    def process_matches(self):
        while True:
            matches = self.find_matches(self.grid)
            if not matches:
                break
            
            # Count red hearts in matches
            red_matches = sum(1 for (y, x) in matches if self.grid[y][x] == 'red')
            self.hearts_collected += red_matches
            
            # Remove matches and refill
            for y, x in matches:
                self.grid[y][x] = None
            
            for x in range(GRID_SIZE):
                column = [self.grid[y][x] for y in range(GRID_SIZE) if self.grid[y][x] is not None]
                column = [None]*(GRID_SIZE - len(column)) + column
                for y in range(GRID_SIZE):
                    self.grid[y][x] = column[y] or random.choice(COLORS)
            
            pygame.time.wait(300)
            self.draw()
            pygame.display.update()

    def handle_click(self, pos):
        if self.game_over:
            return
            
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return
        
        if self.selected is None:
            self.selected = (y, x)
        else:
            dy, dx = abs(y - self.selected[0]), abs(x - self.selected[1])
            if (dy == 1 and dx == 0) or (dx == 1 and dy == 0):
                if self.swap_tiles(self.selected, (y, x)):
                    self.moves_left -= 1
                    self.process_matches()
                    
                    # Check game conditions
                    if self.hearts_collected >= self.target_hearts:
                        self.game_over = True
                    elif self.moves_left <= 0:
                        self.game_over = True
                        
            self.selected = None

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        clock = pygame.time.Clock()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.draw()
            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    Game().run()