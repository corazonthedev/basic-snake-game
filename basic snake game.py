import pygame, sys, time
from random import randrange
pygame.init()

#resume: esc_menu = falseimport pygame
from random import randrange
import sys
pygame.init()

#display
pygame.display.set_caption("basic snake game")
font = pygame.font.SysFont(None,70)
WINDOW = 1000 #set window size
TILE_SIZE = 50 #set tile size 
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE) #set boundries of game area
screen = pygame.display.set_mode([WINDOW]*2) #set screen resolution
width = screen.get_width()
height = screen.get_height()
#funcs
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)] #get random X and Y (1,2)
#snake BODY>DIRECTION>FOOD>snake_parts rect.Rect=RECTANGLE 
snake = pygame.rect.Rect([0,0,TILE_SIZE-2,TILE_SIZE-2]) #x,y w,h
snake.center = get_random_position() #get random snake start
snake_length = 1
snake_parts = [snake.copy()] #parts of snake 
snake_dir = (0,0) #snake direction
dirs = {pygame.K_w: 1,pygame.K_s: 1,pygame.K_a: 1,pygame.K_d: 1,} # available directions
food = snake.copy() #food
food.center = get_random_position() #get food on random position
#time
time, time_step = 0,160 #starting time and speed(bigger-slower)
clock = pygame.time.Clock()
#score
score = 0
high_score = 0
died = False
#playing
running = True
exiting = False
#esc
esc_menu = False
esc_resume = False
esc_restart = False
esc_exit = False
#show grid
grid = [pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE) for x in range(width) for y in range(height)]
light_green = (152, 251, 152)
dark_green = (0, 100, 0)



#play
while running:
    #draw colorful backgronud
    for x in range(0, WINDOW, TILE_SIZE):
        for y in range(0, WINDOW, TILE_SIZE):
            if (x + y) % (2 * TILE_SIZE) == 0:
                color = light_green
            else:
                color = dark_green
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
    #HANDLE INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #QUIT FUNC
            exit()
        if event.type == pygame.KEYDOWN: #PRESSED ANY BUTTON
            if event.key == pygame.K_w:
                snake_dir = (0, -TILE_SIZE)
                dirs = {pygame.K_w: 1, pygame.K_s : 1, pygame.K_a : 1, pygame.K_d : 1,}
            if event.key == pygame.K_s:
                snake_dir = (0, TILE_SIZE)
                dirs = {pygame.K_w: 1, pygame.K_s : 1, pygame.K_a : 1, pygame.K_d : 1,}
            if event.key == pygame.K_a:
                snake_dir = (-TILE_SIZE, 0)
                dirs = {pygame.K_w: 1, pygame.K_s : 1, pygame.K_a : 1, pygame.K_d : 1,}
            if event.key == pygame.K_d:
                snake_dir = (TILE_SIZE, 0)
                dirs = {pygame.K_w: 1, pygame.K_s : 1, pygame.K_a : 1, pygame.K_d : 1,}
            if event.key == pygame.K_ESCAPE:
                esc_menu = True
    current_option = 0
    while esc_menu: #draw esc menu & options
        #select option
        esc_menu_options = ["Continue","Restart","Exit"]
        #esc menu background
        pygame.draw.rect(screen,"orange",(TILE_SIZE*7,TILE_SIZE*5,TILE_SIZE*6,TILE_SIZE*10),border_radius=25) #x,y w,h
        #resume button
        button_resume_text = font.render("Resume",True,("white"))
        button_resume_rect = button_resume_text.get_rect(center=(width//2,height//3))
        screen.blit(button_resume_text,button_resume_rect)
        #restart button
        button_restart_text = font.render("Restart",True,("white"))
        button_restart_rect = button_restart_text.get_rect(center=(width//2,height//2))
        screen.blit(button_restart_text,button_restart_rect)
        #exit button
        button_exit_text = font.render("Exit",True,("white"))
        button_exit_rect = button_exit_text.get_rect(center=(width//2,height//1.49))
        screen.blit(button_exit_text,button_exit_rect)
        #highlight selected option
        pygame.draw.rect(screen, (123,123,123), (TILE_SIZE*7, (TILE_SIZE*6.1) + current_option * (TILE_SIZE*3.4),
                                                    (TILE_SIZE*6),(TILE_SIZE)), 4,25)
        #handle input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: #UP 
                    current_option = (current_option - 1) % len(esc_menu_options)
                    pygame.display.flip()
                elif event.key == pygame.K_DOWN: #DOWN
                    current_option = (current_option + 1) % len(esc_menu_options)
                    pygame.display.flip()
                if event.key == pygame.K_RETURN: #SELECT
                    current_option += 1
                    if current_option == 1: #resume
                        esc_menu = False
                    if current_option == 2: #restart
                        esc_restart = True
                        esc_menu = False
                    if current_option == 3: #exit
                        esc_menu = False
                        exiting = True                
        pygame.display.flip()
        
    current_option = 0
    while exiting:
        #background
        pygame.draw.rect(screen,"orange",(TILE_SIZE*5,TILE_SIZE*5,TILE_SIZE*10,TILE_SIZE*6),border_radius=25)
        #sure to exit button
        button_exit_text1 = font.render("Are you sure to exit?",True,("red"))
        button_exit_rect1 = button_exit_text1.get_rect(center=(width//2,height//3))
        mouse_pos = pygame.mouse.get_pos()
        #yes button
        button_yes_text = font.render("Yes",True,("white"))
        button_yes_rect = button_yes_text.get_rect(center=(width//2-(TILE_SIZE*2),height//2))
        #no button
        button_no_text = font.render("No",True,("white"))
        button_no_rect = button_no_text.get_rect(center=(width//2+(TILE_SIZE*2),height//2))
        #draw buttons
        screen.blit(button_exit_text1,button_exit_rect1)
        screen.blit(button_yes_text,button_yes_rect)
        screen.blit(button_no_text,button_no_rect)
        #highlight selected option
        pygame.draw.rect(screen, (123,123,123), (TILE_SIZE*6.5 + current_option * (TILE_SIZE*4), (TILE_SIZE*9.5),
                                                    (TILE_SIZE*3),(TILE_SIZE)), 4,25)
        exit_menu_options = ["yes","no"]
        #handle input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: #left
                    current_option = (current_option - 1) % len(exit_menu_options)
                    pygame.display.flip()
                elif event.key == pygame.K_RIGHT: #right
                    current_option = (current_option + 1) % len(exit_menu_options)
                    pygame.display.flip()
                if event.key == pygame.K_RETURN: #SELECT
                    current_option += 1
                    if current_option == 1: #yes
                        pygame.quit()
                        sys.exit()
                    if current_option == 2: #no
                        exiting = False
                        running = True
                        esc_menu = True
        pygame.display.flip()
    
    #screen.fill("black")
    #draw food & snake
    pygame.draw.rect(screen,"red", food)
    #head is black body parts are gray
    for index, snake_part in enumerate(snake_parts):
        if index == 0 and len(snake_parts) - 1:
            pygame.draw.rect(screen, "gray", snake_part)
        elif index == len(snake_parts) - 1:
            pygame.draw.rect(screen, "black", snake_part)
        else:
            pygame.draw.rect(screen, "gray", snake_part)
    #move snake with certain speed, accelerating
    time_now = pygame.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        snake_parts.append(snake.copy())
        snake_parts = snake_parts[-snake_length:]
    #draw score
    if died == True:
        fontf = pygame.font.SysFont(None,170)
        eliminated_text = fontf.render("ELIMINATED!",True,("red"))
        eliminated_rect = eliminated_text.get_rect(center=(width//2,height//2))
        screen.blit(eliminated_text,eliminated_rect)
        pygame.display.flip()
        pygame.time.delay(1500)
        if score > high_score:
            high_score = score
        time_step = 160
        score = 0
        esc_restart = False
        died = False
    #set top bar & draw score & draw high-score
    top_bar = pygame.draw.rect(screen,('black'),(0,0,width,50)) #x,y w,h
    fontt = pygame.font.SysFont(None,55)
    score_text = fontt.render(f"score: {score}",True,("white")) #score text
    screen.blit(score_text,(0,5))
    high_score_text = fontt.render(f"high score: {high_score}",True,("white")) #high score text
    screen.blit(high_score_text,(width - high_score_text.get_width() -10,5))
    #check borders & selfeating & spawn on food
    self_eating = pygame.Rect.collidelist(snake,snake_parts[:-1]) != -1 # =-1 for collision check
    if snake.left < 0 or snake.right > WINDOW or snake.bottom > WINDOW or snake.colliderect(top_bar) or self_eating or esc_restart:
        died = True
        snake.center, food.center = get_random_position(), get_random_position()
        snake_length, snake_dir = 1,(0,0)
        snake_parts = [snake.copy()]
    #check food
    food_in_tail = pygame.Rect.collidelist(food, snake_parts[:-1]) !=-1
    if food_in_tail or food.colliderect(top_bar):
        food.center = get_random_position()
    if snake.center == food.center:
        food.center = get_random_position()
        snake_length += 1 #bigger snake
        time_step -= 15 #faster snake
        score += 5 
    # draw grid --DEBUG-- 
    #[pygame.draw.rect(screen, (250, 0, 0), i_rect, 1) for i_rect in grid] 
    pygame.display.flip()
    clock.tick(75)
    
