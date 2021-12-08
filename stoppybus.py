# Welcome to StoppyBus


from typing import Counter
import pygame ,sys
import numpy as np
import os
import math


pygame.init()


#___________CONSTANTS____________________________________________________________CONSTANTS Stored here...
#screen size...
WIDTH=900
HEIGHT=600

#Object sizes...
BUS_WIDTH=150
BUS_HEIGHT=150
MENU_WIDTH=280
MENU_HEIGHT=580
MENU_BTN_WIDTH=260
MENU_BTN_HEIGHT=180
ROAD_WIDTH=470
ROAD_HEIGHT=200
SCOREBOARD_WIDTH=150
SCOREBOARD_HEIGHT=400
TIMER_WIDTH=100
TIMER_HEIGHT=70
EXIT_WIDTH=50
EXIT_HEIGHT=50
LINE_THICKNESS=10
LINE_LENGTH=360

TIME_ATTACK_DURATION = 30  #seconds
# __________Sound Effects__________________________________________

whoosh  = pygame.mixer.Sound(os.path.join("Sound","whoosh.wav"))
exit   = pygame.mixer.Sound(os.path.join("Sound","crash.wav"))
pebble  = pygame.mixer.Sound(os.path.join("Sound","pebble.wav"))
yay     = pygame.mixer.Sound(os.path.join("Sound","yay.wav"))
boo     = pygame.mixer.Sound(os.path.join("Sound","boo.wav"))
crash    = pygame.mixer.Sound(os.path.join("Sound","exit.wav"))
#______Background music...
pygame.mixer.music.load(os.path.join("Sound","happy.mp3"))


# ___________Stuff for tic tack toe_______________________________________________Ticky Tacks and the Toes...
#create the game board
BOARD_ROWS=3
BOARD_COLUMNS=3
board = np.zeros((BOARD_ROWS,BOARD_COLUMNS))

#game variables
victory=0 #0= no victory. 1=a player has won the game
player=1  # player 1 = busses / player 2 = Stopsigns 

#framerate...
FPS=59

#colors...
GREY = (50,50,50)
LIGHT_GREY=(200,200,200)
LIGHT_SKY_BLUE=(150,230,255)
SKY_BLUE=(120,200,220)
DARK_BLUE=(90,170,190)
MENU_BLUE=(70,150,170)
WHITE=(255,255,255)

MENU_BG=(120,200,220)
MENU_BTN=(110,180,200)

ROAD_TAR=(20,20,20)
ROAD_LINE=(200,200,200)



#____________Images_______________________________________________________________Image Files...
#Resized images (the ones actually used in the game) are found below under the Game Assets tab
BUS_IMG        = pygame.image.load(os.path.join('Images','bus.png'))
ROAD_IMG       = pygame.image.load(os.path.join('Images','road.png'))
SCOREBOARD_IMG = pygame.image.load(os.path.join('Images','billboard.png'))
EXIT_IMG       = pygame.image.load(os.path.join('Images','exit.png'))
STOP_IMG       = pygame.image.load(os.path.join('Images','stop.png'))
VICTORY_IMG    = pygame.image.load(os.path.join('Images','victory.png'))


#Dimensions...

#___________Game initialisation____________________________

#game screen object is called win
win   = pygame.display.set_mode((WIDTH,HEIGHT)) 
pygame.display.set_caption("stoppybus") 

#initializes the clock object for use in the time attack mode
clock = pygame.time.Clock()

#_________Image Resizer____________________________________
def img_resize(img,x,y):
     return pygame.transform.scale(img,(x,y))
def img_rotate(img,theta):
    return pygame.transform.rotate(img,theta)

#___________Game Assets______________________________________________________________Game Assets...
BUS        = img_resize(BUS_IMG,150,150)
MINI_BUS   = img_resize(BUS_IMG,100,100)
ROAD       = img_resize(img_rotate(ROAD_IMG,90),ROAD_WIDTH,ROAD_HEIGHT)
SCOREBOARD = img_resize(SCOREBOARD_IMG,SCOREBOARD_WIDTH,SCOREBOARD_HEIGHT)
MENU_BLOCK = (win, DARK_BLUE, [610, 10, MENU_WIDTH, MENU_HEIGHT],)
EXIT       = img_resize(EXIT_IMG,50,50)
STOP       = img_resize(STOP_IMG,100,100)
VICTORY    = img_resize(VICTORY_IMG,50,50)


#_________writing_____________________________________________________________Writing Functions...

def write(text,color,x,y): #inserts text onto the screen 
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    return(win.blit(text,text_rect))


def write_big(text,color,x,y): #inserts text onto the screen 
    font = pygame.font.Font('freesansbold.ttf', 72)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    return(win.blit(text,text_rect))


def write_heading(heading_layer):
    write_big("StoppyBus",WHITE,heading_layer.x,heading_layer.y)


def write_btns(game_mode_layer,time_attack_layer,classic_layer):
    write("<Game Modes>",GREY,center_x(game_mode_layer),center_y(game_mode_layer))
    write("[not ready]",WHITE,center_x(time_attack_layer),center_y(time_attack_layer))
    write("2 Playas",WHITE,center_x(classic_layer),center_y(classic_layer))


#find the centre of a layer
def center_x(layer): 
    return ((layer.right + layer.left)/2)
def center_y(layer):
    return ((layer.bottom+layer.top)/2)

#________Doing the drawings___________________________________________________________Drawing functions...


def draw_bg():
    win.fill(SKY_BLUE)
    

def draw_menu_bar(menu_bar_layer,game_mode_layer,time_attack_layer,classic_layer):
    
    pygame.draw.rect(win,LIGHT_SKY_BLUE,game_mode_layer,border_radius=0)
    pygame.draw.rect(win,MENU_BTN,time_attack_layer,border_radius=15)
    pygame.draw.rect(win,MENU_BTN,classic_layer,border_radius=15)


def draw_heading():
    write('StoppyBus',GREY,100,100 )


def draw_bus(bus_layer):
    win.blit(BUS,(bus_layer.x,bus_layer.y))


def draw_road(road1_layer,road2_layer,road3_layer,road4_layer):
    win.blit(ROAD,(road1_layer.x,road1_layer.y))
    win.blit(ROAD,(road2_layer.x,road2_layer.y))
    win.blit(ROAD,(road3_layer.x,road3_layer.y))
    win.blit(ROAD,(road4_layer.x,road4_layer.y))


def draw_scoreboard(scoreboard_layer):
    win.blit(SCOREBOARD,(scoreboard_layer.x,scoreboard_layer.y))


def draw_timer(timer_layer,scoreboard_layer,counter):
    write("TIME",WHITE,center_x(timer_layer),center_y(timer_layer)-60)
    pygame.draw.rect(win,WHITE,timer_layer,border_radius=15)
    write(str(counter).rjust(3),GREY,center_x(timer_layer),center_y(timer_layer))





def draw_game_board(alpha,vert1,vert2,hor1,hor2):
    draw_rect_alpha(win,(255,255,255,alpha),vert2)
    draw_rect_alpha(win,(255,255,255,alpha),vert1)
    draw_rect_alpha(win,(255,255,255,alpha),hor1)
    draw_rect_alpha(win,(255,255,255,alpha),hor2)


def draw_minibus(x,y):
    win.blit(MINI_BUS,(x+15,y+10)) # adding values in order to centre the images in the block
    

def draw_stopsign(x,y):
    win.blit(STOP,(x+15,y+15))  # adding values in order to centre the images in the block
    

def draw_victory_drive(victory_bus):
        win.blit(BUS,(victory_bus.x,victory_bus.y))


def draw_score(score_layer,score):
    write("SCORE",WHITE,center_x(score_layer),center_y(score_layer)-60)
    pygame.draw.rect(win,WHITE,score_layer,border_radius=15)
    write(str(score).rjust(3),GREY,center_x(score_layer),center_y(score_layer))


def draw_ta_result(ta_result_layer,score_layer,score):
    if ta_result_layer.x!=325:
        ta_result_layer.x=325
        ta_result_layer.y=35
    pygame.draw.rect(win,DARK_BLUE,ta_result_layer,border_radius=15)
    move_score_to_ta_result_layer(score_layer,ta_result_layer)
    draw_ta_score(score_layer,score)


def draw_ta_score(score_layer,score):
    write("SCORE",WHITE,center_x(score_layer),center_y(score_layer)-60)
    pygame.draw.rect(win,WHITE,score_layer,border_radius=15)
    write(str(score).rjust(3),GREY,center_x(score_layer),center_y(score_layer))


def draw_rect_alpha(surface, color, rect):
   
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect(),border_radius=5)
    surface.blit(shape_surf, rect)


def calc_alpha_fade_in(layer,alpha):

    layer_delta=layer.right # ( 0->180 )
    if layer_delta>0:
        alpha = (layer_delta*2/3)//1
        return(int(alpha))
    else:
        return(0)


def draw_exit(exit_layer):
    win.blit(EXIT,(exit_layer.x,exit_layer.y))


#change curser when hovered over a button__________________
def btn_hover(btn,btn1):
    mouse_pos=pygame.mouse.get_pos()
    if btn.collidepoint(mouse_pos) or btn1.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(*pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
        pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        #win.blit(curser,mouse_pos)


#___________Game Logic_______________________________________________________________Game Event functions go here...

#_________TIC TACK TOE ______________________________________________________________Tacky tic toes...
def normalise_selection(x,y):
    x=x-325
    y=y-35
    row = x//120
    col = y//120
    
    return(row,col)


#loops through the game boards to check if there is a 3 in a row anywhere

#check if board is full 
def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col]==0:
                return False
    return True


def victory_conditions():#the victory variable is set equal to the player who has won... returns 3 for a tie
    victory=0
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            #horizontal
            if row ==1:
                if board[row-1][col] == board[row][col] == board[row+1][col] !=0:
                        victory=board[row][col]
                        
            #vertical
            if col ==1 :
                if board[row][col-1] == board[row][col] == board[row][col+1] !=0:
                        victory=board[row][col]
                        
            #left diagonal
            if row ==1 and col ==1:
                if board[row-1][col-1] == board[row][col] == board[row+1][col+1] !=0:
                        victory=board[row][col]
                        
            #right diagonal
            if row ==1 and col==1 :
                if board[row-1][col+1] == board[row][col] == board[row+1][col-1] !=0:
                        victory=board[row][col]
            
            if is_board_full()==True:
                victory = 3

                        
            if victory!=0:
                return victory
    return victory


#marks a square if it is availbale when a player selects that square
def player_turn(row,col,player):
   if available_square(row,col):
        mark_square(row,col,player)
    

# Mark a square as a circle or cross
def mark_square(row,col,player):
    board[row][col] = player

#check if a square is still available
def available_square(row,col):
    return board[row][col]==0


# loops through the board an updates the images to the corresponding player selcted squares
def update_square_imgs():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col]==1:
                x = row*120 + 325
                y = col*120 + 35
                
                draw_minibus(x,y)
            if board[row][col]==2:
                x = row*120 + 325
                y = col*120 + 35
                draw_stopsign(x,y)


def reset_board():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            board[row][col]=0

# return a value indicating which players turn it is next.
def next_player(player):
    if player==1:
        return(2)
    else:
        return(1)
#______game movements and animations____________________________

def move_bus(bus_layer):
    if bus_layer.x < WIDTH*1.5:
            bus_layer.x+=4


def move_screen(vel,heading_layer,bus_layer,road1_layer,road2_layer,road3_layer,road4_layer,exit_layer,scoreboard_layer,timer_layer,score_layer):

    if bus_layer.x >= WIDTH:
        if road1_layer.x<500:
            
            road1_layer.x+=vel
            road2_layer.x+=vel
            road3_layer.x+=vel
            road4_layer.x+=vel
            heading_layer.x+=vel
            scoreboard_layer.x+=vel
            timer_layer.x+=vel
            exit_layer.x+=vel
            score_layer.x+=vel


def move_menu(bus_layer,menu_bar_layer,heading_layer,game_mode_layer,time_attack_layer,classic_layer):
    
    if bus_layer.right>(menu_bar_layer.x):

        x_delta=5
        menu_bar_layer.x+=x_delta
        heading_layer.x+=x_delta
        game_mode_layer.x+=x_delta
        time_attack_layer.x+=x_delta
        classic_layer.x+=x_delta


def move_victory_bus(victory_bus):
    x=5
    
    victory_bus.x+=x


def move_score_to_ta_result_layer(score_layer,ta_result_layer):
    x_offset = (score_layer.right - score_layer.left)//2
    y_offset = (score_layer.bottom - score_layer.top)//2

    score_layer.x = center_x(ta_result_layer)-x_offset
    score_layer.y = center_y(ta_result_layer)-y_offset
     


def reset_victory_bus(victory_bus):
    victory_bus.x=-150


def start_timer():
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    counter, text = 30, '30'.rjust(3)
    print('timer started')


def hide_game_board():
    a=1




#__________Main Game Loop_____________________________________________________________Main Loop...
def main():

    run = True
    pygame.mixer.music.play(-1, 0.0)# ___________Music_______________Music_____________________________________________Music
    #create the hidden layers to draw the game objects onto - these layers are easy to move around on the screen
    menu_bar_layer      = pygame.Rect(610,10,MENU_WIDTH,MENU_HEIGHT)
    heading_layer       = pygame.Rect(280,90,600,200)
    bus_layer           = pygame.Rect(100,435,BUS_WIDTH,BUS_HEIGHT)
    road1_layer         = pygame.Rect(-10,430,ROAD_WIDTH,ROAD_HEIGHT)
    road2_layer         = pygame.Rect(440,430,ROAD_WIDTH,ROAD_HEIGHT)
    road3_layer         = pygame.Rect(-440,430,ROAD_WIDTH,ROAD_HEIGHT)
    road4_layer         = pygame.Rect(-890,430,ROAD_WIDTH,ROAD_HEIGHT)
    game_mode_layer     = pygame.Rect(620,70,MENU_BTN_WIDTH,(MENU_BTN_HEIGHT)-100)
    time_attack_layer   = pygame.Rect(620,210,MENU_BTN_WIDTH,MENU_BTN_HEIGHT)
    classic_layer       = pygame.Rect(620,400,MENU_BTN_WIDTH,MENU_BTN_HEIGHT)   
    exit_layer          = pygame.Rect(-500,10,EXIT_WIDTH,EXIT_HEIGHT)
    scoreboard_layer    = pygame.Rect(-480,75,SCOREBOARD_WIDTH,SCOREBOARD_HEIGHT)
    timer_layer         = pygame.Rect(scoreboard_layer.x+25,scoreboard_layer.y+100,TIMER_WIDTH,TIMER_HEIGHT)
    game_board_layer    = pygame.Rect(325,35,LINE_LENGTH,LINE_LENGTH)
    vert_line1_layer    = pygame.Rect(445,35,LINE_THICKNESS,LINE_LENGTH)
    vert_line2_layer    = pygame.Rect(565,35,LINE_THICKNESS,LINE_LENGTH)
    hor_line1_layer     = pygame.Rect(325,155,LINE_LENGTH,LINE_THICKNESS)
    hor_line2_layer     = pygame.Rect(325,275,LINE_LENGTH,LINE_THICKNESS)
    victory_bus         = pygame.Rect(-150,435,BUS_WIDTH,BUS_HEIGHT)
    score_layer         = pygame.Rect(scoreboard_layer.x+25,scoreboard_layer.y+100,TIMER_WIDTH,TIMER_HEIGHT)
    ta_result_layer     = pygame.Rect(325-1000,35-1000,360,360)
    

    # Setting all the Booleans to False...
    time_attack    = False       #True when user clicks time attack btn
    classic        = False       #True when user clicks classic btn
    timer_started  = False       #True when user places first bus down on game board -> this starts the timer
    game_ready     = False       #True when the game is rady for the player to make selections
    victory_parade = False       #True when the bus is doing a victory lap
    big_time_loser = False       #True when user loses a game
    score_updated  = False       #Used to figure out if the score has been updated (who would of guessed)
    timer_ended    = False       #When true the game board will dissapear and score will be show


    score   = 0
    player  = 1
    counter = TIME_ATTACK_DURATION 
    alpha   = 0

    while run ==True:
        clock.tick(FPS)  #limiting fps to 59
        
        for event in pygame.event.get(): #looks for any event (most are built in already defined by pygame (can have User defined events as well))

            if event.type == pygame.QUIT:# Exit the game when the application is quit
                run = False
                sys.exit()

            # perform these actions when the mouse button is clicked
            if event.type==pygame.MOUSEBUTTONDOWN:
                
                clicked_X=event.pos[0]
                clicked_Y=event.pos[1]
                
                # Do this stuff when a user clicks somewhere..._____________________________________
                if exit_layer.collidepoint(event.pos):
                    exit.play()
                    time_attack=False     #True when user clicks time attack btn
                    classic=False         #True when user clicks classic btn
                    timer_started=False   #True when user places first bus down on game board -> this starts the timer
                    pygame.time.set_timer(pygame.USEREVENT,0)
                    reset_board()
                    main()

                if time_attack_layer.collidepoint(event.pos): #time attack button is clicked
                    time_attack=True
                    crash.play() #play crash sound

                if classic_layer.collidepoint(event.pos):     #classic button is clicked
                    classic=True
                    crash.play()
                
                
                # game board is clicked on when intro is finished
                # intro finishes when the x coordinate of the exit layer equals ten
                # starts the game (when the board is in the correct position) for both game modes
                if game_board_layer.collidepoint(event.pos) and exit_layer.x==10:  
                    game_ready=True

                    if time_attack == True and timer_started == False: #first click on gameboard initializes the timer
                        start_timer()
                        timer_started=True
                        timer_ended=False
                
                    if game_ready:
                        row= normalise_selection(clicked_X,clicked_Y)[0]
                        col= normalise_selection(clicked_X,clicked_Y)[1]
                        
                        if available_square(row,col):
                            pebble.play()
                            mark_square(row,col,player)
                            player = next_player(player)  

                
            if event.type==pygame.USEREVENT:
                if counter>0:
                    counter-=1
                    


        # game mode specific tasks go in here (this is done before game assets are drawn)
        if time_attack==True:
            move_bus(bus_layer)
            
        if classic==True:
            move_bus(bus_layer)
               

        # move screen moves the road ,heading and scoreboard assets oncw the bus has left the view 
        move_screen(2,heading_layer,bus_layer,road1_layer,road2_layer,road3_layer,road4_layer,exit_layer,scoreboard_layer,timer_layer,score_layer)

        #moves the menu when the bus crashes into it
        move_menu(bus_layer,menu_bar_layer,heading_layer,game_mode_layer,time_attack_layer,classic_layer)

        # Just drawing all the assets into their initial positions
        draw_bg()
        
        # game board fades in as the scoreboard enters the screen

        draw_game_board(calc_alpha_fade_in(scoreboard_layer,alpha),vert_line1_layer,vert_line2_layer,hor_line1_layer,hor_line2_layer)
        draw_road(road1_layer,road2_layer,road3_layer,road4_layer)
        draw_scoreboard(scoreboard_layer)
        draw_menu_bar(menu_bar_layer,game_mode_layer,time_attack_layer,classic_layer)
        write_heading(heading_layer)
        write_btns(game_mode_layer,time_attack_layer,classic_layer)
        draw_bus(bus_layer)
        draw_victory_drive(victory_bus)
        draw_exit(exit_layer)

        if time_attack==True or classic==True:
            update_square_imgs()

        #makes the curser change when the buttons are hovered over
        btn_hover(time_attack_layer,classic_layer)

        # do this according to active game mode (duplicated as this is done after other assets are drawn)
        if time_attack==True:
            draw_timer(timer_layer,scoreboard_layer,counter)
            if counter==0:
                timer_ended=True
                draw_ta_result(ta_result_layer,score_layer,score)
            
            #check if there is a victory
            if victory_conditions()==1:
                print("victory")
                score+=1
                
                
            #check if there is a loss
            if victory_conditions()==2:
                print("loser")
            

            #stop game board from being clickable when the time ends


        
        if classic==True:
            draw_score(score_layer,score)
        
            if victory_conditions()==1:
                print("victory")
                victory_parade=True

            if victory_conditions()==2:
                big_time_loser=True
                print("loser")
                pygame.time.wait(1000)
                reset_board()

            if victory_bus.x>900: 
                score+=1
                reset_board()
                victory_parade=False
                reset_victory_bus(victory_bus)
            if victory_bus.x==0:
                yay.play()
            if victory_parade:
                move_victory_bus(victory_bus)


        #--------Update Display-------------------Update Display----------------Updat Display----------||       /__________
        pygame.display.update()    #-----------------------------------------------------------||       \
        #----------------------------------------------------------------------------------------------||       

        #reset the game board in time attack mode - done after display is updated in order to draw the 3 in a row and have a delay before game board is reset
        if time_attack==True:
            if victory_conditions()!=0:
                pygame.time.wait(500)
                reset_board()
                
            
            if is_board_full():
                pygame.time.wait(500)
                reset_board()
            
            
        
        if big_time_loser: # for classic mode
            boo.play()
            pygame.time.wait(1000)
            reset_board()
            big_time_loser=False
        
    pygame.quit()


if __name__== '__main__':
    main()