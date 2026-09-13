import pygame
import random
import sys

WIDTH, HEIGHT = 600,600
fps = 60
BACKGROUND_COLOR = (192, 192, 192)
cell_size = 40
Difficulties = {
    "Beginner":{"cols":9,"rows":9,"mines":10},
    "Intermediate": {"cols": 16, "rows": 16, "mines": 40},
    "Advanced": {"cols": 30, "rows": 16, "mines": 99}   
}
BG_GRAY = (192, 192, 192)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER = (150, 150, 150)
TEXT_COLOR = (255, 255, 255)
TITLE_COLOR = (0, 0, 0)

NUMBER_COLORS = {
    1: (0, 0, 255),      # Blue
    2: (0, 128, 0),      # Green
    3: (255, 0, 0),      # Red
    4: (0, 0, 128),      # Dark Blue
    5: (128, 0, 0),      # Maroon
    6: (0, 128, 128),    # Teal
    7: (0, 0, 0),        # Black
    8: (128, 128, 128)   # Gray
}

class Cell:
    def __init__(self):
        self.is_mine = False
        self.adjacent_mines = 0
        self.is_revealed = False
        self.is_flagged = False

def generate_board(row,cols,num_mines):
    grid = [[Cell() for _ in range(cols)] for _ in range(row)]
    all_coordinates = [(r,c) for r in range(row) for c in range(cols)]
    mine_positions = random.sample(all_coordinates,num_mines)
    for r,c in mine_positions:
        grid[r][c].is_mine = True
    #calculating adjacent mines
    for r in range(row):
        for c in range(cols):
            if grid[r][c].is_mine:
                continue
            mines_count = 0
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr,nc = r+dr,c+dc
                    if 0 <= nr < row and 0 <= nc < cols:
                        if grid[nr][nc].is_mine:
                            mines_count += 1
            grid[r][c].adjacent_mines = mines_count
    return grid

def reveal_cell(grid,r,c):
    rows = len(grid)
    cols = len(grid[0])

    # base case: out of bounds
    if not (0 <= r < rows and 0 <= c < cols):
        return
    cell = grid[r][c]

    # base case: already revealed or protected by a flag
    if cell.is_revealed or cell.is_flagged:
        return

    # reveal the cell
    cell.is_revealed = True

    # stop cascading if it's a number or a mine
    if cell.adjacent_mines > 0 or cell.is_mine:
        return

    # if it's a zero, cascade to all 8 neighbors
    for dr in [-1,0,1]:
        for dc in [-1,0,1]:
            if dr == 0 and dc == 0:
                continue
            reveal_cell(grid,r + dr,c + dc)

# Making the menu
def draw_menu(screen,font,title_font,buttons,mouse_pos):
    screen.fill(BG_GRAY)
    title = title_font.render("Minesweeper",True,TITLE_COLOR)
    title_rect = title.get_rect(center=(WIDTH // 2,150))
    screen.blit(title,title_rect)

    # Drawing buttons
    for text, rect in buttons.items():
        color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen,color=color,rect=rect,border_radius=5)
        text = font.render(text,True,TEXT_COLOR)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text,text_rect)

def draw(screen,grid,font):
    #All the drawing goes here
    screen.fill(BG_GRAY)
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            cell = grid[r][c]
            x = c * cell_size
            y = r * cell_size
            rect = pygame.Rect(x,y,cell_size,cell_size)

            if not cell.is_revealed:
                #unrevealed state
                pygame.draw.rect(screen,BG_GRAY,rect)
                #top and left highlights
                pygame.draw.line(screen,(255,255,255),(x,y),(x+cell_size -1,y),2)
                pygame.draw.line(screen,(255,255,255),(x,y),(x,y + cell_size -1),2)
                # Bottom and right shadows
                pygame.draw.line(screen, (128, 128, 128), (x, y + cell_size - 1), (x + cell_size - 1, y + cell_size - 1), 2)
                pygame.draw.line(screen, (128, 128, 128), (x + cell_size - 1, y), (x + cell_size - 1, y + cell_size - 1), 2)

                if cell.is_flagged:
                    flag = font.render("F",True,(255,0,0))
                    screen.blit(flag,flag.get_rect(center=rect.center))
            else:
                #revealed state
                pygame.draw.rect(screen,(180,180,180),rect)
                pygame.draw.rect(screen,(128,128,128),rect,1)

                if cell.is_mine:
                    pygame.draw.circle(screen,(0,0,0),rect.center,cell_size // 4)
                elif cell.adjacent_mines > 0:
                    color = NUMBER_COLORS.get(cell.adjacent_mines,(0,0,0))
                    num = font.render(str(cell.adjacent_mines),True,color)
                    screen.blit(num,num.get_rect(center=rect.center))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial",24,bold=True)
    title_font = pygame.font.SysFont("Arial",48,bold=True)

    btn_width, btn_height = 200, 50
    center_x = (WIDTH - btn_width) // 2
    buttons = {
        "Beginner": pygame.Rect(center_x, 250, btn_width, btn_height),
        "Intermediate": pygame.Rect(center_x, 320, btn_width, btn_height),
        "Advanced": pygame.Rect(center_x, 390, btn_width, btn_height)
    }
    state = "MENU"
    game_status = "ACTIVE"
    current_config = None
    grid = []
    total_safe_cells = 0

    #main loop
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        #event handling
        for event in pygame.event.get():
            # quit the game
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "MENU":
                    if event.button == 1:
                        for diff_name,rect in buttons.items():
                            if rect.collidepoint(mouse_pos):
                                current_config = Difficulties[diff_name]
                                new_width = current_config["cols"]*cell_size
                                new_height = current_config["rows"] * cell_size

                                game_status = "ACTIVE"
                                total_safe_cells = (current_config["rows"] * current_config["cols"]) - current_config["mines"]

                                grid = generate_board(current_config["rows"],current_config["cols"],current_config["mines"])
                  
                                screen = pygame.display.set_mode((new_width,new_height))
                                state = "PLAYING"
                                break
                elif state == "PLAYING":
                    if game_status != "ACTIVE":
                        state = "MENU"
                        screen = pygame.display.set_mode((WIDTH,HEIGHT))
                        continue

                    c = mouse_pos[0] // cell_size
                    r = mouse_pos[1] // cell_size

                    if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                        cell = grid[r][c]

                        if event.button == 1:
                            if not cell.is_flagged and not cell.is_revealed:
                                reveal_cell(grid,r,c)

                                if cell.is_mine:
                                    game_status = "LOST"

                                    for row in grid:
                                        for sq in row:
                                            if sq.is_mine:
                                                sq.is_revealed = True
                                else:
                                    revealed_count = sum(1 for row in grid for sq in row if sq.is_revealed and not sq.is_mine)
                                    if revealed_count == total_safe_cells:
                                        game_status = "WON"

                            elif event.button == 3:
                                if not cell.is_revealed:
                                    cell.is_flagged = not cell.is_flagged

        if state == "MENU":
            draw_menu(screen,font,title_font,buttons,mouse_pos)
        elif state == "PLAYING":
            draw(screen,grid,font)

            if game_status != "ACTIVE":
                overlay = pygame.Surface(screen.get_size())
                overlay.set_alpha(180)
                overlay.fill((0,0,0))
                screen.blit(overlay,(0,0))


                msg = "YOU WIN!" if game_status == "WON" else "Game Over"
                color = (0,255,0) if game_status == "WON" else (255,0,0)

                msg_surf = title_font.render(msg,True,color)
                msg_rect = msg_surf.get_rect(center=(screen.get_width() //2,screen.get_height()//2-30))
                screen.blit(msg_surf,msg_rect)

                sub_surf = font.render("Click anywhere to return to Menu", True, (255, 255, 255))
                sub_rect = sub_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30))
                screen.blit(sub_surf, sub_rect)

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()