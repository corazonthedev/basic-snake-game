import pygame
from random import randrange
import sys
pygame.init()

#display
pygame.display.set_caption("basic snake game")
WINDOW = 1000 #set window size
TILE_SIZE = 50 #set tile size 
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE) #set boundries of game area
screen = pygame.display.set_mode([WINDOW]*2) #set screen resolution
width = screen.get_width()
height = screen.get_height()
#funcs
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)] #get random X and Y (1,2)
#snake BODY>DIRECTION>FOOD>snake_parts rect.Rect=RECTANGLE 
snake = pygame.rect.Rect([0,0,TILE_SIZE-2,TILE_SIZE-2]) #0,0 means top left corner | rectangle size = tile_size -2 | (X,Y width,height)
snake.center = get_random_position() #get random snake start
snake_length = 1 #snake snake_length
snake_parts = [snake.copy()] #parts of snake 
snake_dir = (0,0) #DIRECTIONS
dirs = {pygame.K_w: 1,pygame.K_s: 1,pygame.K_a: 1,pygame.K_d: 1,} # AVAILABLE DIRECTIONS
food = snake.copy() #FOOD 
food.center = get_random_position() #get food on random
#time
time, time_step = 0,160 #starting time and speed(bigger-slower)
clock = pygame.time.Clock()
#score
score = 0
high_score = 0
died = False
#playing
menu = True
running = False
exiting = False
#esc
esc_menu = False
esc_resume = False
esc_restart = False
esc_exit = False


while True:
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_play_rect.collidepoint(mouse_pos):
                    running = True
                    menu = False
                elif button_exit_rect.collidepoint(mouse_pos):
                    menu = False
                    exiting = True   
        screen.fill("orange")
        font = pygame.font.SysFont(None,55)
        #keybinds info 
        text_keybinds = font.render(f"W A S D for move ESC for pause menu ",True,("black"))
        rect_keybinds = text_keybinds.get_rect(center=(width//2.5,height//20))
        screen.blit(text_keybinds,rect_keybinds)
        #play button
        button_play_text = font.render(f"Play",True,("black"))
        button_play_rect = button_play_text.get_rect(center=(width // 2, height // 4))
        screen.blit(button_play_text,button_play_rect)
        #exit button
        button_exit_text = font.render(f"Exit",True,("black"))
        button_exit_rect = button_exit_text.get_rect(center=(width//2,height//3))
        screen.blit(button_exit_text,button_exit_rect)
        pygame.display.flip()
        
    while exiting:
        #sure to exit buttons
        screen.fill("black")
        button_exit_text1 = font.render("exiting are you sure?",True,("red"))
        button_exit_rect1 = button_exit_text1.get_rect(center=(width//2,height//3))
        screen.blit(button_exit_text1,button_exit_rect1)
        mouse_pos = pygame.mouse.get_pos()
        button_yes_text = font.render("Yes",True,("white"))
        button_yes_rect = button_yes_text.get_rect(center=(width//2.5,height//2))
        button_no_text = font.render("No",True,("white"))
        button_no_rect = button_no_text.get_rect(center=(width//2,height//2))
        screen.blit(button_yes_text,button_yes_rect)
        screen.blit(button_no_text,button_no_rect)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_yes_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif button_no_rect.collidepoint(mouse_pos):
                    menu = True
                    exiting = False
        pygame.display.flip()

    while running:
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
        while esc_menu:
            pygame.draw.rect(screen,"grey",(250,200,500,600)) #x,y w,h
            button_resume_text = font.render("Resume",True,("white"))
            button_resume_rect = button_resume_text.get_rect(center=(width//2,height//3))
            screen.blit(button_resume_text,button_resume_rect)
            
            button_restart_text = font.render("Restart",True,("white"))
            button_restart_rect = button_restart_text.get_rect(center=(width//2,height//2))
            screen.blit(button_restart_text,button_restart_rect)
            
            button_exit_text = font.render("Exit",True,("white"))
            button_exit_rect = button_exit_text.get_rect(center=(width//2,height//1.5))
            screen.blit(button_exit_text,button_exit_rect)
            
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_resume_rect.collidepoint(mouse_pos):
                        esc_menu = False
                    elif button_restart_rect.collidepoint(mouse_pos):
                        esc_restart = True
                        esc_menu = False
                    elif button_exit_rect.collidepoint(mouse_pos):
                        esc_menu = False
                        running = False
                        exiting = True
                        

            pygame.display.flip()
            
        screen.fill("black")
        #draw food & snake
        pygame.draw.rect(screen,"red", food)
        #[pygame.draw.rect(screen,"green", snake_part) for snake_part in snake_parts]
        for index, snake_part in enumerate(snake_parts):
            if index == 0 and len(snake_parts) - 1:
                pygame.draw.rect(screen, "green", snake_part)
            elif index == len(snake_parts) - 1:
                pygame.draw.rect(screen, "lightgreen", snake_part)
            else:
                pygame.draw.rect(screen, "green", snake_part)
                
        #move snake
        time_now = pygame.time.get_ticks()
        if time_now - time > time_step:
            time = time_now
            snake.move_ip(snake_dir)
            snake_parts.append(snake.copy())
            snake_parts = snake_parts[-snake_length:]
            
        #draw score
        if died == True:
            if score > high_score:
                high_score = score
            time_step = 160
            score = 0
            died = False
            esc_restart = False
        top_bar = pygame.draw.rect(screen,('gray'),(0,0,width,50)) #x,y w,h
        font = pygame.font.SysFont(None,55)
        score_text = font.render(f"score: {score}",True,("black")) #score text
        screen.blit(score_text,(0,5))
        high_score_text = font.render(f"high score: {high_score}",True,("black")) #high score text
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
        pygame.display.flip()
        clock.tick(60)