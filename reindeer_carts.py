#   @author Raymond Qu
#   @instructor Mr. Reid
#   @course ICS3U1
#   @date 2018/01/22

#   REINDEER CARTS: By R. Qu

#importing libraries
import random
import pygame
 
#colours
BLACK = (0, 0, 0) #rgb code for pure black
WHITE = (255, 255, 255) #rbg code for pure white

# --- PYGAME SETUP ---
pygame.init() #initlization of pygame

#monitors time
clock = pygame.time.Clock()

#screen specifications
size = (1000, 700) #1000 pixels wide, 700 pixels tall
screen = pygame.display.set_mode(size)

#window title
pygame.display.set_caption("Reindeer Carts")

# --- CLASSES FOR SPRITE CREATION ---
#player class w/ methods for other sprites
class Player(pygame.sprite.Sprite): #allows pygame sprite commands to work
    def __init__(self):
        super().__init__()
        #player attributes
        self.image = pygame.image.load("reindeer_minecart.png").convert() #loads image
        self.image.set_colorkey(WHITE) #makes white transparent
        self.rect = self.image.get_rect() #draws hitbox and calls rect for positioning
        self.health_points = 10 #preset health points
        #speed of movement (only for player sprite)
        self.speed_x = 0 #values change when keyboard pressed
        self.speed_y = 0 
    #player movement
    def move(self):
        #moves by changing location of sprite at a certain speed
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
    #resets xy positions of coal / presents
    def reset_pos(self):
        self.rect.y = random.randrange(-25, 675) #limits positions to the height of the screen
        self.rect.x = random.randrange(1000, 2000) #makes it seem like the sprites spawn at irregular intervals
    #moves coal / presents, also checks if it's offscreen
    def update(self, speed): #sprite movespeed is predetermined here
        self.rect.x += speed #moves sprites from the right to left at the determined speed
        #moves sprites back onto the screen
        if self.rect.x < -100: #if the sprites move off the screen
            self.reset_pos() #reset them back to the left at new positions

#coal class to load seperate sprite image
class Coal(Player):#inherits from Player class
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coal.png").convert() #loads image
        self.image.set_colorkey(WHITE) #makes white transparent
        self.rect = self.image.get_rect() #draws hitbox and calls rect for positioning'

#presents class to load seperate sprite image
class Presents(Player): #Player class inheritance
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("present.png").convert() #loads image
        self.image.set_colorkey(WHITE) #transparency
        self.rect = self.image.get_rect() #draws hitbox

##failed health visualization, used numbers instead
##class Health(Player): ##the health bar
##    def __init__(self):
##        super().__init__()
##        self.image = pygame.image.load("heart.png").convert()
##        self.image.set_colorkey(BLACK)
##        self.rect = self.image.get_rect()

# --- SPRITE GENERATION ---        
#generate random starting coal positions
def createCoal():
    #create all the coal
    for i in range(4): #initial generation number
        coal_block = Coal()
        #spawn in random positions
        coal_block.rect.x = random.randrange(1000, 2000)
        coal_block.rect.y = random.randrange(-25, 675)
        #adds coal objects to lists
        coal_list.add(coal_block) #used for coal hit detection
        all_sprites_list.add(coal_block) #to be drawn all at once

#generate random starting present positions
def createPresents():
    #create all the coal
    for i in range(4): #initial generation number
        presents = Presents()
        #spawn in random positions
        presents.rect.x = random.randrange(1000, 2000)
        presents.rect.y = random.randrange(-25, 675)
        #adds presents objects to lists
        presents_list.add(presents)
        all_sprites_list.add(presents)


# --- LISTS OF SPRITES ---
#list of all coal
coal_list = pygame.sprite.Group()

#list of presents
presents_list = pygame.sprite.Group()

#list of health hearts
hearts_list = pygame.sprite.Group()

#list of all the sprites in the game
all_sprites_list = pygame.sprite.Group()

# --- INITIALIZING THE PLAYER SPRITE ---
#create player
player_main = Player() #a player sprite is created from the Player class
player_main.rect.y = 250 #presets starting position of the sprite
all_sprites_list.add(player_main) #adds sprite to all sprites list

# --- COAL & PRESENTS SPRITE GENERATION ---
#calls functions to generate all randomly placed non-player sprites
createPresents()
createCoal()

# --- SPRITE HIT COUNTING VARIABLES ---
#counts non-player sprites collected by the player
coal_hit_counter = 0
presents_hit_counter = 0

# --- IMAGES AND SOUND ---
#background images
background_image = pygame.image.load("game_background.png").convert() #minecraft background
death_image = pygame.image.load("death.png").convert() #dark souls styled death screen
start_image = pygame.image.load("startscreen.png").convert() #main menu
instructions_image = pygame.image.load("instructions.png").convert() #instructions for player

#sound effects
death_sound = pygame.mixer.Sound("death_sound.ogg") #dark souls death sound
main_music = pygame.mixer.Sound("legendsneverdie.ogg") #league soundtrack

# --- CONTROLLING THE LOOPS ---
#loop controllers
program_start = True #allows program to run
start_screen = True #first screen polayers see
end_screen = False #shown when game ends
instructions_screen = False #shown after start_screen
game_start = False #the actual game loop
show_instructions = True #used to check if instructions have been shown

# --- MAIN PROGRAM LOOP ---
while program_start: #keeps game running as the program checks which while loop to loop through

    #main menu
    while start_screen: #first screen to show since it starts as True
        screen.blit(start_image, [0,0]) #blit the start screen background
        for event in pygame.event.get(): #checks for any commands
            #exititing the game
            if event.type == pygame.QUIT: #if the user wants to quit
                #sets all variables as False to quit
                start_screen = False
                program_start = False
            #continue to play
            elif event.type == pygame.KEYDOWN: #checks for keypresses downwards
                if event.key == pygame.K_RETURN: #when the player hits enter
                    for sprite in all_sprites_list: #resets all sprite positions
                        sprite.reset_pos()          #by calling the method
                    player_main.rect.y = 250 #resets player's starting position
                    player_main.rect.x = 5   #by placing it at an arbitrary position
                    #starts the game
                    start_screen = False #stops looping through the start screen
                    instructions_screen = True #goes to instructions screen
        #refreshes screen
        pygame.display.flip()
        clock.tick(60)

    #end of game screen
    while end_screen: #become True when player loses all health
        screen.blit(death_image, [0,0]) #blit the end of game background
        font = pygame.font.SysFont('Hobo STD', 100, True, False) #initializes font
        score = font.render(str(int(presents_hit_counter)*10),True,WHITE) #calculates final score
        screen.blit(score, [500, 120]) #blit the final score
        #check for key presses
        for event in pygame.event.get():
            #force quit
            if event.type == pygame.QUIT: #if user exits using the window
                end_screen = False #stops looping the end of game screen
                program_start = False #stops looping the main program
            elif event.type == pygame.KEYDOWN:
                #play again
                if event.key == pygame.K_RETURN: #when enter is hit
                    death_sound.stop() #stops playing dark souls death sound
                    end_screen = False  #stops the end screen
                    start_screen = True #goes back to the main menu
                    #reset counting variables
                    coal_hit_counter = 0 #coal counter reset
                    presents_hit_counter = 0 #presents counter reset
                #exit game
                elif event.key == pygame.K_ESCAPE: #if ESC is pressed
                    #any True variables set to False to quit
                    end_screen = False
                    program_start = False
        #refreshes screen
        pygame.display.flip()
        clock.tick(60)

    #displays instructions
    while instructions_screen: #becomes True when player hits ENTER on start screen
        if show_instructions == True: #show instructions if never played before
            screen.blit(instructions_image, [0,0]) #blit the instructions image on screen
            for event in pygame.event.get():
                #exit game
                if event.type == pygame.QUIT: #if the user hits exit
                    #sets all variables as False to quit
                    instructions_screen = False
                    program_start = False
                #play game
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: #when the player hits enter
                        main_music.play() #starts playing main theme
                        main_music.set_volume(0.25) #sets music volume to 25%
                        instructions_screen = False #stops looping through instructions
                        game_start = True           #begins the game loop
        else:
            instructions_screen = False #stops looping through instructions
            game_start = True           #starts game
        #refreshes screen
        pygame.display.flip()
        clock.tick(60)

    #GAME LOOP
    while game_start: #begins after instructions screen
        #event loops
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if user hits exits button
                #set all True variables to false to quit
                game_start = False
                program_start = False
            #when WASD keys are pressed
            elif event.type == pygame.KEYDOWN:
                #controlling the reindeer
                if event.key == pygame.K_w: #move up
                    #stops sprite from going offscreen
                    if player_main.rect.y <= 0: #if the sprite's too high
                        player_main.speed_y = 0 #stops moving
                    else:
                        player_main.speed_y = -10 #otherwise move normally
                elif event.key == pygame.K_a: #move left
                    if player_main.rect.x <= 0: #if sprite's moving to the left offscreen
                        player_main.speed_x = 0 #stop moving
                    else:
                        player_main.speed_x = -10          
                elif event.key == pygame.K_s: #move down
                    if player_main.rect.y >= 533: #if sprite's too low
                        player_main.speed_y = 0 #stop moving
                    else:
                        player_main.speed_y = 10
                elif event.key == pygame.K_d: #move right
                    if player_main.rect.x >= 856: #if sprite's moving to the right offscreen
                        player_main.speed_x = 0 #stop moving
                    else:
                        player_main.speed_x = 10

            #when WASD is released
            elif event.type == pygame.KEYUP: #when keys are released
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player_main.speed_y = 0 #stop moving on the y axis
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player_main.speed_x = 0 #stop moving on the x axis

        #check if player hits any block / must be false to reset position
        coal_blocks_hit_list = pygame.sprite.spritecollide(player_main, coal_list, False) #adds coal sprite to list when hit

        #when a coal sprite is hit
        for coal in coal_blocks_hit_list: #for each sprite in the list
            coal_hit_counter += 1 #adds 1 to the counter
            player_main.health_points += -1 #decreases health points by 1
            print("Coal blocks hit: " + str(coal_hit_counter))
            print ("Health points: " + str(player_main.health_points))
            coal.reset_pos() #resets position of coal sprite

        #check if player hits any block / must be false to reset position
        presents_hit_list = pygame.sprite.spritecollide(player_main, presents_list, False) #adds present sprite to list when hit

        #when present sprite is hit
        for present in presents_hit_list:
            presents_hit_counter += 1 #add 1 to present hit counter
            print("Presents collected: " + str(presents_hit_counter))
            present.reset_pos() #reset present sprite position

        #drawing
        screen.blit(background_image, [0,0]) #draws background
        all_sprites_list.draw(screen) #draws all sprites on screen
        player_main.move()#allows for player movement

        #sets player boundaries and stops player
        if player_main.rect.y <= 0 or player_main.rect.y >= 533: #if y axis out of bounds
            player_main.speed_y = 0 #stops player
        if player_main.rect.x <= 0 or player_main.rect.x >= 856: #if x axis out of bounds
            player_main.speed_x = 0 #stops player

        #displaying score
        font = pygame.font.SysFont('Hobo STD', 50, True, False) #initializes font
        score = font.render(str(int(presents_hit_counter)*10),True,WHITE) #gets score from presents hit
        score_text = font.render(("Score: "),True,WHITE)
        screen.blit(score_text, [10, 10]) #blits "Score "
        screen.blit(score, [150, 10]) #blits score to the screen

        #displaying health
        health = font.render(str(player_main.health_points),True,(232, 25, 25))
        health_text = font.render(("Health: "),True,(232, 25, 25))
        screen.blit(health_text, [10, 50]) #blits "Health: "
        screen.blit(health, [170, 50]) #blits health left as a number
        
        #moving the non-player sprites, moving them back to a random starting position
        presents_list.update(-8)#handles present sprites
        coal_list.update(-10)   #handles coal sprites

        #game finishes
        if player_main.health_points == 0: #when player health hits zero
            main_music.stop() #stop the background music
            death_sound.play() #play dark souls death sound
            player_main.speed_y = 0 #stops sprite movement
            player_main.speed_x = 0 #stops sprite movement
            game_start = False #stops looping through game
            end_screen = True #starts looping through end of game screen
            show_instructions = False #will not show instructions on next games
            player_main.health_points = 10 #resets hp back to 10

        #refreshing screen
        pygame.display.flip()
        clock.tick(60)

#exit pygame
pygame.quit()
