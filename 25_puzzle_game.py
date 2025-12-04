import pygame
import sys
import random
import time

def initialize_pygame():
    """Initialize PyGame with error handling"""
    try:
        pygame.init()
        print("PyGame initialized successfully!")
        return True
    except Exception as e:
        print(f"Failed to initialize PyGame: {e}")
        return False

# Constants
WIDTH, HEIGHT = 600, 700
GRID_SIZE = 5
TILE_SIZE = 100
MARGIN = 5
BOARD_PADDING = 50
FPS = 60

# Colors
BACKGROUND = (40, 44, 52)
GRID_BACKGROUND = (30, 34, 42)
TILE_COLORS = [
    (241, 196, 15),   # Yellow
    (230, 126, 34),   # Orange
    (231, 76, 60),    # Red
    (155, 89, 182),   # Purple
    (52, 152, 219),   # Blue
    (46, 204, 113),   # Green
    (26, 188, 156),   # Teal
    (52, 73, 94),     # Dark Blue
]
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (52, 152, 219)
BUTTON_HOVER_COLOR = (41, 128, 185)
BUTTON_TEXT_COLOR = (255, 255, 255)

class PuzzleGame:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        # Initialize game state first
        self.moves = 0
        self.start_time = time.time()
        self.game_over = False
        
        # Create a solved board
        self.board = [[i + j * GRID_SIZE + 1 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        self.board[GRID_SIZE-1][GRID_SIZE-1] = 0  # Empty space
        self.empty_pos = (GRID_SIZE-1, GRID_SIZE-1)
        
        # Shuffle the board
        self.shuffle_board(1000)
        
    def shuffle_board(self, moves):
        # Make random moves to shuffle the board
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        
        for _ in range(moves):
            valid_moves = []
            for dx, dy in directions:
                new_x, new_y = self.empty_pos[0] + dx, self.empty_pos[1] + dy
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    valid_moves.append((dx, dy))
            
            if valid_moves:
                dx, dy = random.choice(valid_moves)
                # Use a temporary method to move without counting moves
                self._swap_tiles(self.empty_pos[0] + dx, self.empty_pos[1] + dy)
    
    def _swap_tiles(self, x, y):
        """Swap tiles without counting moves (for shuffling)"""
        # Swap the tile with the empty space
        self.board[self.empty_pos[0]][self.empty_pos[1]] = self.board[x][y]
        self.board[x][y] = 0
        self.empty_pos = (x, y)
    
    def move_tile(self, x, y):
        if self.game_over:
            return False
            
        # Check if the tile is adjacent to the empty space
        if (abs(x - self.empty_pos[0]) + abs(y - self.empty_pos[1])) == 1:
            # Swap the tile with the empty space
            self.board[self.empty_pos[0]][self.empty_pos[1]] = self.board[x][y]
            self.board[x][y] = 0
            self.empty_pos = (x, y)
            self.moves += 1
            
            # Check if the puzzle is solved
            if self.is_solved():
                self.game_over = True
                
            return True
        return False
    
    def is_solved(self):
        # Check if the board is in the solved state
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if i == GRID_SIZE-1 and j == GRID_SIZE-1:
                    if self.board[i][j] != 0:
                        return False
                else:
                    if self.board[i][j] != i * GRID_SIZE + j + 1:
                        return False
        return True
    
    def draw(self, screen):
        # Draw background
        screen.fill(BACKGROUND)
        
        # Draw title
        title_text = font.render("25 Puzzle Game", True, TEXT_COLOR)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
        
        # Draw moves and time
        moves_text = small_font.render(f"Moves: {self.moves}", True, TEXT_COLOR)
        screen.blit(moves_text, (20, 80))
        
        elapsed_time = int(time.time() - self.start_time)
        time_text = small_font.render(f"Time: {elapsed_time}s", True, TEXT_COLOR)
        screen.blit(time_text, (WIDTH - time_text.get_width() - 20, 80))
        
        # Draw board background
        board_rect = pygame.Rect(
            BOARD_PADDING, 
            120, 
            GRID_SIZE * (TILE_SIZE + MARGIN) - MARGIN, 
            GRID_SIZE * (TILE_SIZE + MARGIN) - MARGIN
        )
        pygame.draw.rect(screen, GRID_BACKGROUND, board_rect, border_radius=10)
        
        # Draw tiles
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.board[i][j]
                if value == 0:  # Skip empty tile
                    continue
                    
                # Calculate position
                x = BOARD_PADDING + j * (TILE_SIZE + MARGIN)
                y = 120 + i * (TILE_SIZE + MARGIN)
                
                # Draw tile with color based on value
                color_idx = (value - 1) % len(TILE_COLORS)
                tile_color = TILE_COLORS[color_idx]
                
                tile_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, tile_color, tile_rect, border_radius=8)
                pygame.draw.rect(screen, (255, 255, 255), tile_rect, 2, border_radius=8)
                
                # Draw number
                number_text = font.render(str(value), True, TEXT_COLOR)
                text_rect = number_text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(number_text, text_rect)
        
        # Draw game over message
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            # Congratulations message
            congrats_text = font.render("Congratulations!", True, (46, 204, 113))
            screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, HEIGHT // 2 - 50))
            
            # Moves and time
            stats_text = small_font.render(
                f"You solved the puzzle in {self.moves} moves and {elapsed_time} seconds!", 
                True, TEXT_COLOR
            )
            screen.blit(stats_text, (WIDTH // 2 - stats_text.get_width() // 2, HEIGHT // 2))
        
        # Draw reset button
        button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 80, 150, 50)
        mouse_pos = pygame.mouse.get_pos()
        button_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        
        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
        reset_text = small_font.render("New Game", True, BUTTON_TEXT_COLOR)
        screen.blit(reset_text, (button_rect.centerx - reset_text.get_width() // 2, 
                                button_rect.centery - reset_text.get_height() // 2))
        
        return button_rect

def main():
    # Initialize PyGame
    if not initialize_pygame():
        sys.exit()
    
    # Create the window
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("25 Puzzle Game")
        print("Window created successfully!")
    except Exception as e:
        print(f"Failed to create window: {e}")
        sys.exit()
    
    # Initialize fonts
    global font, small_font
    try:
        font = pygame.font.SysFont('Arial', 36)
        small_font = pygame.font.SysFont('Arial', 24)
        print("Fonts loaded successfully!")
    except Exception as e:
        print(f"Failed to load fonts: {e}")
        # Use default fonts
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
    
    clock = pygame.time.Clock()
    game = PuzzleGame()
    running = True
    
    print("Game starting...")
    
    while running:
        button_rect = game.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if reset button was clicked
                    if button_rect.collidepoint(event.pos):
                        game.reset_game()
                    
                    # Check if a tile was clicked
                    elif not game.game_over:
                        x, y = event.pos
                        # Convert screen coordinates to board coordinates
                        board_x = (y - 120) // (TILE_SIZE + MARGIN)
                        board_y = (x - BOARD_PADDING) // (TILE_SIZE + MARGIN)
                        
                        if 0 <= board_x < GRID_SIZE and 0 <= board_y < GRID_SIZE:
                            game.move_tile(board_x, board_y)
            
            elif event.type == pygame.KEYDOWN and not game.game_over:
                # Handle arrow key controls
                x, y = game.empty_pos
                if event.key == pygame.K_UP and x < GRID_SIZE - 1:
                    game.move_tile(x + 1, y)
                elif event.key == pygame.K_DOWN and x > 0:
                    game.move_tile(x - 1, y)
                elif event.key == pygame.K_LEFT and y < GRID_SIZE - 1:
                    game.move_tile(x, y + 1)
                elif event.key == pygame.K_RIGHT and y > 0:
                    game.move_tile(x, y - 1)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()