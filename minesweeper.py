import pygame, random
import numpy as np
pygame.init()

WIDTH = 1100
HEIGHT = 650

SIZE = 20

SQRSIZE = HEIGHT / SIZE

font = pygame.font.SysFont('arial',int(SQRSIZE)//2 -int(SQRSIZE//30),True)

#colors
WHITE = (255,255,255)
BLACK = (10,10,10)
GREY = (120,120,120)
LIGHT_GREY = (200,200,200)

BOMBS = SIZE * 2



def create_board(size):
    return np.zeros((size,size))

def place_mines(board,size):
    mines = set()
    mine_count = 0
    while mine_count < BOMBS:
        i = random.randint(0,size - 1)
        j = random.randint(0,size - 1)
        if board[i][j] == 0:
            board[i][j] = -1
            mines.add((i,j))
            mine_count += 1
    return mines

def safes(board):
    safes = set()
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0:
                safes.add((i,j))
    return safes

def draw_board(screen,size,board):
    for i in range(size):
        for j in range(size):
            rect = pygame.Rect(j * SQRSIZE + 4 , i * SQRSIZE + 4, SQRSIZE - 5, SQRSIZE - 5)
            pygame.draw.rect(screen,GREY, rect)
    draw_title(screen)
    draw_no_of_bombs(screen)
    draw_restart(screen)
    pygame.display.update()

def draw_title(screen):
    font = pygame.font.SysFont('arial',60,True)
    text = font.render("MINESWEEPER",True,WHITE)
    text_rect = pygame.Rect(HEIGHT + 40 , 40 ,text.get_width() , text.get_height())
    screen.blit(text,text_rect)

def draw_restart(screen):
    font = pygame.font.SysFont('arial',40,True)
    text = font.render("Restart",True,BLACK)
    text_rect = pygame.Rect(HEIGHT + (WIDTH - HEIGHT) / 3, HEIGHT - 120 ,text.get_width() , text.get_height())
    blank_rect = pygame.Rect(HEIGHT + (WIDTH - HEIGHT) / 3 - 20, HEIGHT - 140 , text.get_width() + 40 , text.get_height() + 40)
    pygame.draw.rect(screen,WHITE,blank_rect)
    screen.blit(text,text_rect)
    return blank_rect



def draw_win_lose(screen,Win):
    Word = "Won" if Win else "Lost"  
    font = pygame.font.SysFont('arial',40,True)
    text = font.render(f'You {Word} !',True,WHITE)
    text_rect = pygame.Rect(HEIGHT + 120 , 400 ,text.get_width() , text.get_height())
    screen.blit(text,text_rect)
    pygame.display.update()

def draw_no_of_bombs(screen,Flagged=set()):
    num = BOMBS - len(Flagged)
    font = pygame.font.SysFont('arial',40,True)
    text = font.render(f"Bombs : {num}",True,WHITE)
    text_rect = pygame.Rect(HEIGHT + 120 , 200 ,text.get_width() , text.get_height())
    blank_rect = pygame.Rect(HEIGHT, 160 , WIDTH - HEIGHT , text.get_height() + 50)
    pygame.draw.rect(screen,'#000000',blank_rect)
    screen.blit(text,text_rect)

def get_neighbors(row,col):
    """
        top row, row , bottom row
    """
    neighbors = []
    if row - 1 >= 0 :
        neighbors.append((row-1,col))
        if col - 1 >= 0:
            neighbors.append((row-1,col-1))
        if col + 1 <= SIZE - 1:
            neighbors.append((row-1,col+1))
    if col - 1 >= 0:
        neighbors.append((row,col-1))
    if col + 1 <= SIZE - 1:
        neighbors.append((row,col+1))
    if row + 1 <= SIZE - 1:
        neighbors.append((row+1,col))
        if col - 1 >= 0: 
            neighbors.append((row+1,col-1))
        if col + 1 <= SIZE - 1:
            neighbors.append((row+1,col+1))
    return neighbors


def get_num(board,i,j):
    neighbors = get_neighbors(i,j)
    count = 0
    for neighbor in neighbors:
        if board[neighbor[0]][neighbor[1]] == -1:
            count += 1
    return count

def draw_num(board,i,j,screen,Flagged,clicked,safes):
    over = False
    num = get_num(board,i,j)
    text = font.render(str(num),True,BLACK)
    text_rect = pygame.Rect(j*SQRSIZE + SQRSIZE /2 - text.get_width()/2 + 2 ,i*SQRSIZE + SQRSIZE / 2 - text.get_height()/2 + 2,text.get_width(),text.get_height())
    rect = pygame.Rect(j * SQRSIZE + 4 , i * SQRSIZE + 4, SQRSIZE - 5, SQRSIZE - 5)

    if board[i][j] != -1 and not (i,j) in Flagged:
        clicked.add((i,j))
        pygame.draw.rect(screen,LIGHT_GREY,rect)
        screen.blit(text,text_rect)
        if clicked == safes:
            draw_win_lose(screen,True)
            over = True

    elif board[i][j] == -1:
        mine = pygame.image.load("assets/images/mine.png")
        mine = pygame.transform.scale(mine, (SQRSIZE, SQRSIZE))
        mine_Rect = pygame.Rect(j * SQRSIZE + 2 , i * SQRSIZE + 2 , SQRSIZE - 5, SQRSIZE - 5)
        pygame.draw.rect(screen,LIGHT_GREY, rect)
        screen.blit(mine,mine_Rect)
        draw_win_lose(screen,False)
        over = True

    pygame.display.update()
    return over

def draw_flag(screen,i,j,Flagged,mines,clicked):
    flag = pygame.image.load("assets/images/flag.png")
    flag = pygame.transform.scale(flag, (SQRSIZE, SQRSIZE))
    rect = pygame.Rect(j * SQRSIZE + 4 , i * SQRSIZE + 4, SQRSIZE - 5, SQRSIZE - 5)
    if (i,j) in Flagged:
        Flagged.remove((i,j))
        pygame.draw.rect(screen,GREY, rect)
    elif not ((i,j) in clicked):
        pygame.draw.rect(screen,LIGHT_GREY, rect)
        Flagged.add((i,j))
        screen.blit(flag,rect)
        if Flagged == mines:
            draw_win_lose(screen,True)

    draw_no_of_bombs(screen,Flagged)
    pygame.display.update()



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Minesweeper")
    pygame.display.update()
    board = create_board(SIZE)
    mines = place_mines(board,SIZE)
    safe = safes(board)
    draw_board(screen,SIZE,board)
    restart = draw_restart(screen)
    Flagged = set()
    clicked = set()
    game = True
    over = False
    while game == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                clickedX, clickedY = int(my // SQRSIZE) , int(mx//SQRSIZE )
                left, _, right = pygame.mouse.get_pressed()
                if clickedX < SIZE and clickedY < SIZE and not over:
                    if left:
                        get_num(board,clickedX,clickedY)
                        over = draw_num(board,clickedX,clickedY,screen,Flagged,clicked,safe)

                    if right:
                        draw_flag(screen,clickedX,clickedY,Flagged,mines,clicked)

                if restart.collidepoint(pygame.mouse.get_pos()):
                    pygame.time.wait(500)
                    main()
    pygame.quit()
                



if __name__ == "__main__":
    main()