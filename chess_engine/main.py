import pygame as p

# pygame setup
p.init()
screen = p.display.set_mode((1280,720))
clock = p.time.Clock()
running = True
dt = 0

rectX = 500
rectY = 50
rectW = 140
rectH = 140

player_pos = p.Vector2(screen.get_width() / 2,screen.get_height() / 2)

rows,cols = (8,8)
board = list()

def createBoardCoordinate():
    for i in range(rows):
        row = []
        for j in range(cols):   
            row.append(j)
        board.append(row)


while running:
    #poll for events
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
    
    #fill the screen with a color to wipe away anything from last frame
    screen.fill((148, 90, 13))
    createBoardCoordinate()
    print(board)
    #Render the game
    p.draw.rect(screen,"black",[rectX,rectY,rectW,rectH])
    keys = p.key.get_pressed()

    if keys[p.K_w]:
        player_pos.y -= 300 *dt
    if keys[p.K_s]:
        player_pos.y += 300 * dt
    if keys[p.K_a]:
        player_pos.x -= 300 *dt
    if keys[p.K_d]:
        player_pos.x += 300 * dt
    

    p.display.flip()
    dt = clock.tick(60) /1000
p.quit()