#   @author Raymond Qu
#   @instructor Mr. Reid
#   @course ICS3U1
#   @date 2018/01/22

#   REINDEER CARTS: By R. Qu

#importing libraries
import random
import pygame

# --- PYGAME SETUP ---
pygame.init()
clock = pygame.time.Clock()
size = (1000, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Reindeer Carts")
 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# --- CLASSES FOR SPRITE CREATION ---
#Built for the player class but applies for other child classes.
#Each class loads their own .png for sprite usage.
#.png's are made transparent.
#Methods for movement created from Player class.
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #Attributes
        self.image = pygame.image.load("reindeer_minecart.png").convert()
        self.image.set_colorkey(WHITE) #transparency
        self.rect = self.image.get_rect() #sprite hitbox
        self.health_points = 10
        #Movement (only for player sprite).
        self.speed_x = 0
        self.speed_y = 0 
    #Player movement.
    def move(self):
        #Changes location by speed.
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
    #Reset non-player sprite positions when called.
    #The reset position is randomly staggered and limited to the screen.
    def reset_pos(self):
        self.rect.y = random.randrange(-25, 675) 
        self.rect.x = random.randrange(1000, 2000) 
    #Handles movement for all non-player sprites.
    def update(self, speed):
        self.rect.x += speed
        #When the sprites move offscreen, call the method to reset their positions.
        if self.rect.x < -100:
            self.reset_pos()

#Child Coal class.
#Seperate sprite and "get_rect".
class Coal(Player):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coal.png").convert() 
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect() 

#Child Presents class.
class Presents(Player):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("present.png").convert() 
        self.image.set_colorkey(WHITE) 
        self.rect = self.image.get_rect() 

##Attempt at creating a health bar.
##class Health(Player):
##    def __init__(self):
##        super().__init__()
##        self.image = pygame.image.load("heart.png").convert()
##        self.image.set_colorkey(BLACK)
##        self.rect = self.image.get_rect()

# --- SPRITE GENERATION ---
#Function to spawn random coal.
#Randomly creates coal objects within a location.
#This creates a "staggered" feeling of movement from each sprite.
def createCoal():
    for i in range(4):
        #Class call.
        coal_block = Coal()
        #Positions.
        coal_block.rect.x = random.randrange(1000, 2000)
        coal_block.rect.y = random.randrange(-25, 675)
        #Adds objects to seperate list.
        coal_list.add(coal_block)
        #Adds objects to list with all sprites.
        all_sprites_list.add(coal_block)

#Function to spawn random presents.
#Randomly creates present objects.
def createPresents():
    for i in range(4):
        presents = Presents()
        #Spawn randomly.
        presents.rect.x = random.randrange(1000, 2000)
        presents.rect.y = random.randrange(-25, 675)
        #Add objects to lists.
        presents_list.add(presents)
        all_sprites_list.add(presents)


# --- LISTS OF SPRITES ---
#Sprite Lists
#Used to hold objects to be drawn.
coal_list = pygame.sprite.Group()
presents_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

# --- INITIALIZING THE PLAYER SPRITE ---
#Generate one player sprite.
#Set the y value manually and add it the list to be drawn.
player_main = Player() 
player_main.rect.y = 250
all_sprites_list.add(player_main)

# --- COAL & PRESENTS SPRITE GENERATION ---
#Generate non-player sprites using the function.
createPresents()
createCoal()

# --- SPRITE HIT COUNTING VARIABLES ---
#Counts non-player sprites collected by the player.
coal_hit_counter = 0
presents_hit_counter = 0

# --- IMAGES AND SOUND ---
#Background images.
background_image = pygame.image.load("game_background.png").convert() #background
death_image = pygame.image.load("death.png").convert() #end screen
start_image = pygame.image.load("startscreen.png").convert() #main menu
instructions_image = pygame.image.load("instructions.png").convert() #instructions

#Sound effects.
death_sound = pygame.mixer.Sound("death_sound.ogg") #dark souls death sound
main_music = pygame.mixer.Sound("legendsneverdie.ogg") #league soundtrack

# --- CONTROLLING THE LOOPS ---
#Controlling the game loops.
program_start = True #Starting the game.
start_screen = True #Splash screen.
end_screen = False #Endgame screen.
instructions_screen = False #Instructions for controls.
game_start = False #Gameplay loop.
show_instructions = True #Check if player has seen instructions.

# --- MAIN PROGRAM LOOP ---
#Keeps the program running through the sub-loops.
while program_start:

    #Main menu.
    while start_screen:
        screen.blit(start_image, [0,0]) #Blit background.

        #Checks for any commands.
        for event in pygame.event.get(): 
            #Force-closing the game.
            if event.type == pygame.QUIT:
                #Sets all variables as False to quit.
                start_screen = False
                program_start = False

            #Continue.
            #Checking for key presses.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    #Resets all positions (for replaying players).
                    for sprite in all_sprites_list:
                        #Call method to reset any sprites.
                        sprite.reset_pos()
                    #Reset player starting position.
                    player_main.rect.y = 250
                    player_main.rect.x = 5
                    #Moves to instructions screen.
                    start_screen = False
                    instructions_screen = True

        #Refresh rate.
        pygame.display.flip()
        clock.tick(60)

    #Endgame screen.
    while end_screen:
        #Blit background and text.
        screen.blit(death_image, [0,0])
        font = pygame.font.SysFont('Hobo STD', 100, True, False) 
        score = font.render(str(int(presents_hit_counter)*10),True,WHITE) 
        screen.blit(score, [500, 120]) #Final score.

        for event in pygame.event.get():
            #Force-closing the game.
            if event.type == pygame.QUIT:
                end_screen = False 
                program_start = False

            #Check for key presses.
            elif event.type == pygame.KEYDOWN:
                #Enter to play again.
                if event.key == pygame.K_RETURN:
                    #End endgame elements and restart game.
                    death_sound.stop()
                    end_screen = False 
                    start_screen = True 
                    #Reset the counters.
                    coal_hit_counter = 0 
                    presents_hit_counter = 0 

                #ESC to quit.
                elif event.key == pygame.K_ESCAPE:
                    #All True variables set to False to quit.
                    end_screen = False
                    program_start = False

        #Refresh.
        pygame.display.flip()
        clock.tick(60)

    #Instructions.
    while instructions_screen:
        #Show the instructions by blitting it.
        #Only shown once (before the first playthrough).
        if show_instructions == True: 
            screen.blit(instructions_image, [0,0]) 

            for event in pygame.event.get():
                #If player wants to quit.
                if event.type == pygame.QUIT:
                    instructions_screen = False
                    program_start = False

                #Continue to play the game.
                elif event.type == pygame.KEYDOWN:
                    #Starts the game with music.
                    if event.key == pygame.K_RETURN:
                        main_music.play() 
                        instructions_screen = False 
                        game_start = True

        #Start game if the instructions has already been shown before.
        else:
            main_music.play() 
            instructions_screen = False
            game_start = True

        #Refresh.
        pygame.display.flip()
        clock.tick(60)

    #Actual game loop.
    while game_start:
        
        for event in pygame.event.get():
            #If player wants to quit.
            if event.type == pygame.QUIT:
                game_start = False
                program_start = False

            #Player control.
            elif event.type == pygame.KEYDOWN:
                #Moving up.
                if event.key == pygame.K_w:
                    #Prevent offscreen movement.
                    #When the sprite is moving offscreen, then stop any input in that direction.
                    if player_main.rect.y <= 0: #Stops movement at a certain point.
                        player_main.speed_y = 0
                    else:
                        player_main.speed_y = -10 #Move normally.
                #Moving to the left.
                elif event.key == pygame.K_a: 
                    if player_main.rect.x <= 0: 
                        player_main.speed_x = 0 
                    else:
                        player_main.speed_x = -10          
                #Moving down.
                elif event.key == pygame.K_s:
                    if player_main.rect.y >= 533: 
                        player_main.speed_y = 0 
                    else:
                        player_main.speed_y = 10
                #Moving to the right.
                elif event.key == pygame.K_d: 
                    if player_main.rect.x >= 856:
                        player_main.speed_x = 0 
                    else:
                        player_main.speed_x = 10

            #Stop movement when keys are released.
            #Speed is set to 0.
            elif event.type == pygame.KEYUP: 
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player_main.speed_y = 0 
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player_main.speed_x = 0 

        #Collision check for player against other sprites..
        #False == collision with the player sprite.
        #After each collion, the object is added to the collision list.
        coal_blocks_hit_list = pygame.sprite.spritecollide(player_main, coal_list, False)
        presents_hit_list = pygame.sprite.spritecollide(player_main, presents_list, False)


        #--- NON-PLAYER SPRITE POSITION RESETS ---
        #After colliding with the player, the position of the object is reset.
        #A counter also records the score and health of the player due to these collisions.
        
        #Coal.
        for coal in coal_blocks_hit_list:
            coal_hit_counter += 1 #Counter.
            player_main.health_points += -1 #Decrease HP.
            print("Coal blocks hit: " + str(coal_hit_counter))
            print ("Health points: " + str(player_main.health_points))
            coal.reset_pos() #Resets the position.

        #Presents.
        for present in presents_hit_list:
            presents_hit_counter += 1 #Counter
            print("Presents collected: " + str(presents_hit_counter))
            present.reset_pos()

        
        # --- DRAWING ---
        #Background.
        screen.blit(background_image, [0,0]) 
        #Draws all sprites on the screen.
        all_sprites_list.draw(screen)
        #Player movement.
        player_main.move()

        #Player boundaries.
        #When player is detected out of bounds, the sprite is stopped.
        #This works in conjucture with the input halt.
        if player_main.rect.y <= 0 or player_main.rect.y >= 533: 
            player_main.speed_y = 0 
        if player_main.rect.x <= 0 or player_main.rect.x >= 856:
            player_main.speed_x = 0

        #Displaying the score.
        #Using the number of presents hit, add up a total score.
        #Multiply the presents hit by ten and print it as the score.
        font = pygame.font.SysFont('Hobo STD', 50, True, False)
        score = font.render(str(int(presents_hit_counter)*10),True,WHITE)
        score_text = font.render(("Score: "),True,WHITE)
        screen.blit(score_text, [10, 10])
        screen.blit(score, [150, 10]) 

        #Displaying HP.
        #Blits "Health: " and the number.
        health = font.render(str(player_main.health_points),True,(232, 25, 25))
        health_text = font.render(("Health: "),True,(232, 25, 25))
        screen.blit(health_text, [10, 50]) 
        screen.blit(health, [170, 50]) 
        
        #Moving the non-player sprites.
        #Calls the "update" method for movement and to reset their positions if they move offscreen.
        #Presents move a bit slower than the coal.
        presents_list.update(-8)
        coal_list.update(-10)

        # --- GAME OVER ---
        #When the player dies, death sound plays and the end game screen is shown.
        #This is triggered by the health becoming to zero.
        #The music is stopped and the game over sound is played.
        if player_main.health_points == 0:
            #Music.
            main_music.stop() 
            death_sound.play() 
            #Stos any movement.
            player_main.speed_y = 0 
            player_main.speed_x = 0
            #Stops game loop.
            game_start = False
            #Shows end screen.
            end_screen = True
            #Prevent instructions from showing again.
            show_instructions = False
            #HP is reset.
            player_main.health_points = 10

        #Refresh.
        pygame.display.flip()
        clock.tick(60)

#Exit pygame.
pygame.quit()
