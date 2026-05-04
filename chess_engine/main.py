import pygame as p

p.init()
WIDTH, HEIGHT = 800,800
screen = p.display.set_mode((WIDTH,HEIGHT))
p.display.set_caption("Chess")

move_rules = {
    'r': { # Rook: Straight lines, unlimited range
        'directions': [(0, 1), (0, -1), (1, 0), (-1, 0)],
        'max_steps': 7
    },
    'b': { # Bishop: Diagonals, unlimited range
        'directions': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
        'max_steps': 7
    },
    'q': { # Queen: All 8 directions, unlimited range
        'directions': [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)],
        'max_steps': 7
    },
    'k': { # King: All 8 directions, but only 1 step
        'directions': [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)],
        'max_steps': 1
    },
    'n': { # Knight: These aren't unit vectors, they are the full jumps
        'directions': [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)],
        'max_steps': 1
    },
    'p': { # Pawn: Special case - we might need to handle white vs black separately
        'white_move': [(-1, 0)], # Up the board
        'black_move': [(1, 0)],  # Down the board
        'max_steps': 1 
    }
}


#Helper functions
def is_empty(board_list,row,col):
    check = board_list[row][col]
    if 0 <= row < 8 and 0 <= col < 8:
        return check == '--'
    else:
        return False
    
def is_path_clear(board_list,start_row,start_col,end_row,end_col, direction):
    row_step,col_step = direction
    current_row, current_col = start_row + row_step , start_col + col_step
    while current_row != end_row or current_col != end_col:
        if not is_empty(board_list, current_row,current_col):
            return False
        else:
            current_row +=row_step
            current_col += col_step
    return True

def get_move_info(start_r,start_c,end_r,end_c):
    delta_r = end_r - start_r
    delta_c = end_c - start_c

    row_step = 0 if delta_r == 0 else (1 if delta_r > 0 else -1)
    col_step = 0 if delta_c == 0 else (1 if delta_c > 0 else -1)

    distance = max(abs(delta_r),abs(delta_c))
    return (row_step,col_step),distance 

# Main functions
# draw a rect
def draw_rect(color,x,y,width,height):
    p.draw.rect(screen,color,(x,y,width,height))

def draw_board():
    color_wood = (191, 68, 34)
    color_white = (247, 243, 242)
    for i in range(0,8):
        for j in range(0,8):
            x = i * 100
            y = j * 100
            sum = i+j
            if sum % 2 == 0:
                draw_rect(color_wood,x,y,100,100)
            else:
                draw_rect(color_white,x,y,100,100)
board = [
    ['br','bn','bb','bq','bk','bb','bn','br'],
    ['bp','bp','bp','bp','bp','bp','bp','bp'],
    ['--','--','--','--','--','--','--','--'],
    ['--','--','--','--','--','--','--','--'],
    ['--','--','--','--','--','--','--','--'],
    ['--','--','--','--','--','--','--','--'],
    ['wp','wp','wp','wp','wp','wp','wp','wp'],
    ['wr','wn','wb','wq','wk','wb','wn','wr']
]
IMAGES = {}
def load_images():
    pieces = ['bb','bn','bk','bp','bq','br','wb','wk','wn','wp','wq','wr']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"img/{piece}.png"),(100,100))

def draw_pieces():
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece],(c*100,r * 100))
def sketch_book():
    draw_board()
    draw_pieces()

def is_move_legal(select_row,select_col,change_row,change_col):
    direction, distance = get_move_info(select_row,select_col,change_row,change_col)
    piece = board[select_row][select_col]
    if piece == '--': return False
    color = piece[0]
    piece_type = piece[1]
    rules = move_rules[piece_type]
    if piece_type == 'p':
        allowed_dirs = move_rules['p']['white_move'] if color == 'w' else move_rules['p']['black_move']
        if direction not in allowed_dirs or distance > move_rules['p']['max_steps']:
            return False
    else:
        if direction not in rules['directions'] or distance > rules['max_steps']:
            return False
    if piece_type != 'n':
        if not is_path_clear(board,select_row,select_col,change_row,change_col,direction):
            return False
    return True


def move(select_row,select_col,change_row,change_col):
    if is_move_legal(select_row,select_col,change_row,change_col):
        temp = board[select_row][select_col]
        board[select_row][select_col] = board[change_row][change_col]
        board[change_row][change_col] = temp
    else:
        print("Can't move")

#game loop
running = True
clicks = []
load_images()
while running:
    mouse_x ,mouse_y = p.mouse.get_pos()
    hover_col = mouse_x // 100
    hover_row = mouse_y // 100
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.MOUSEBUTTONDOWN:
            # location = p.mouse.get_pos()
            clicks.append((hover_row,hover_col))
            print(f"coordinate: {hover_row}, {hover_col}")
            if len(clicks) == 2:
                start_row, start_col = clicks[0]
                end_row,end_col = clicks[1]
                move(start_row,start_col,end_row,end_col)
                clicks = []
                print("Moved")
    
    screen.fill((40,44,52))
    sketch_book()
    p.display.flip()

p.quit()