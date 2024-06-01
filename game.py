import pygame
import random

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH ,WINDOW_HEIGHT))
pygame.display.set_caption("Space invaders")

#set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#define classes
class Game():
    def __init__(self , player , alien_group , player_bullet_group , alien_bullet_group):
        
        self.round_number = 1
        self.score = 0

        self.player = player
        self.alien_group = alien_group
        self.player_bullet_group = player_bullet_group
        self.alien_bullet_group = alien_bullet_group

        #soundds
        self.new_round_sound = pygame.mixer.Sound('Assets/new_round.wav')
        self.alien_hit = pygame.mixer.Sound('Assets/alien_hit.wav')
        self.player_hit = pygame.mixer.Sound('Assets/player_hit.wav')

        #set font
        self.font = pygame.font.Font('Assets/custom.ttf' , 32)
    def update(self):
        self.shift_aliens()
        self.check_collision()
        self.check_round_completion()
    def draw(self):
        #set colors
        WHITE = (255 ,255 , 255)

        #set text
        score_text = self.font.render('Score: '  + str(self.score) , 1 ,WHITE)
        score_rect = score_text.get_rect()
        score_rect.centerx = WINDOW_WIDTH // 2
        score_rect.top = 10

        round_text = self.font.render('Round: ' + str(self.round_number) , 1 ,WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (20 , 10)

        lives_text = self.font.render('Lives: ' +str(self.player.lives) , 1, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (WINDOW_WIDTH - 20 , 10) 

        #blit
        display_surface.blit(score_text , score_rect)
        display_surface.blit(round_text , round_rect)
        display_surface.blit(lives_text , lives_rect)
        pygame.draw.line(display_surface , WHITE , (0 , 50) , (WINDOW_WIDTH , 50) , 4)
        pygame.draw.line(display_surface , WHITE , (0 , WINDOW_HEIGHT - 100) , (WINDOW_WIDTH , WINDOW_HEIGHT - 100))
    def shift_aliens(self):
        #determine if alien group has it the edge
        shift = False
        for alien in (self.alien_group.sprites()):
            if alien.rect.left <= 0 or alien.rect.right >= WINDOW_WIDTH:
                shift = True
        #shift down and change direction
        if shift:
            breach = False
            for alien in (self.alien_group.sprites()):
                alien.rect.y += 75 * self.round_number
                
                #reverse direction
                alien.direction = -1 * alien.direction
                alien.rect.x += alien.direction * alien.velocity

                #check breach
                if alien.rect.bottom > WINDOW_HEIGHT - 100:
                    breach = True
            
            if breach:
                self.player.lives -= 1
                self.check_game_status("Aliens breached the line" , "Press any key to continue")


    def check_collision(self):
        if pygame.sprite.groupcollide(self.player_bullet_group , self.alien_group , 1 ,1):
            self.alien_hit.play()
            self.score += 100
        
        if pygame.sprite.spritecollide(self.player , self.alien_bullet_group , [0 , 1]):
            self.player_hit.play()
            self.player.lives -= 1
            self.check_game_status("Alien hit" , "press enter")
    def check_round_completion(self):
        if not (self.alien_group):
            self.round_number += 1
            self.score += 1000 * self.round_number
            self.start_new_round()

    def start_new_round(self):
        #create a grid of alien
        for i in range(11):
            for j in range(5):
                alien = Alien(64 + i*64, 64 + j*64 ,self.round_number , self.alien_bullet_group)
                self.alien_group.add(alien)
        #pause the game prompt the user to enter
        self.new_round_sound.play()
        self.pause_game("Space invaders Round" + str(self.round_number) , "PRess enter to begin")
    def check_game_status(self ,  main_text , sub_text):
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()
        self.player.reset()
        for alien in self.alien_group:
            alien.reset()
        
        #check if game game is over
        if self.player.lives == 0:
            self.reset_game()
        else:
            self.pause_game(main_text , sub_text)
    def pause_game(self , main_text , sub_text):
        #set colors
        WHITE = (255 , 255, 255)
        BLACK = (0 , 0 , 0)

        #create main text
        main_text = self.font.render(main_text ,1 , WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH // 2 , WINDOW_WIDTH // 2)

        #create sub text
        sub_text = self.font.render(sub_text , 1 , WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH // 2 , WINDOW_HEIGHT // 2  + 64)

        #blit text
        display_surface.fill(BLACK)
        display_surface.blit(main_text , main_rect)
        display_surface.blit(sub_text , sub_rect)
        pygame.display.update()

        #pause game
        global running
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                    if event.type == pygame.QUIT:
                        is_paused = False
                        running = False
    def reset_game(self):
        self.pause_game("Final Score " + str(self.score) , "Press enter to play again")

        #reset game values
        self.score = 0
        self.round_number = 1

        self.player.lives = 3

        #empty groups 
        self.alien_group.empty()
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()

        #start new game
        self.start_new_round()

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self , bullet_group):
        super().__init__()
        self.image = pygame.image.load('Assets/spaceship.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH //2 
        self.rect.bottom = WINDOW_HEIGHT

        self.lives = 3
        self.velocity = 8
        self.bullet_group = bullet_group

        self.shoot_sound = pygame.mixer.Sound('Assets/player_fire.wav')

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity

    def fire(self):
        if len(self.bullet_group) < 4:
            self.shoot_sound.play()
            PlayerBullet(self.rect.centerx , self.rect.top , self.bullet_group)
    def reset(self):
        self.rect.centerx = WINDOW_WIDTH //2
    
#alien class
class Alien(pygame.sprite.Sprite):
    def __init__(self , x , y , velocity , bullet_group):
        super().__init__()
        self.image = pygame.image.load('Assets/alien.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x , y)

        self.starting_x = x
        self.starting_y = y

        self.direction = 1
        self.velocity = velocity
        self.bullet_group = bullet_group

        self.shoot_sound = pygame.mixer.Sound("Assets/alien_fire.wav")
    def update(self):
        self.rect.x += self.velocity * self.direction

        if random.randint(0 , 1000) > 999 and len(self.bullet_group) < 3:
            self.shoot_sound.play()
            self.fire()
    def fire(self):
        AlienBullet(self.rect.centerx , self.rect.bottom , self.bullet_group)
    def reset(self):
        self.rect.topleft =(self.starting_x , self.starting_y)
        self.direction = 1
#player bullet class
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self , x, y , bullet_group):
        super().__init__()
        self.image = pygame.image.load('Assets/green_laser.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)
    def update(self):
        self.rect.y -= self.velocity

        if self.rect.bottom < 0:
            self.kill()
#alien bullet class
class AlienBullet(pygame.sprite.Sprite):
    def __init__(self , x , y , bullet_group):
        super().__init__()
        self.image = pygame.image.load('Assets/red_laser.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)
    def update(self):
        self.rect.y += self.velocity

        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
#bullet group 
my_player_bullet_group = pygame.sprite.Group()
my_alien_bullet_group = pygame.sprite.Group()

#create a player
my_player_group = pygame.sprite.Group()
my_player = Player(my_player_bullet_group)
my_player_group.add(my_player)

#create an alien group
my_alien_group = pygame.sprite.Group()

#game object
my_game = Game(my_player , my_alien_group , my_player_bullet_group , my_alien_bullet_group)
my_game.start_new_round()
#game loop 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #fire bullets
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.fire()
    #fill the display
    display_surface.fill(( 0, 0, 0))

    #update the display the sprite groups
    my_player_group.update()
    my_player_group.draw(display_surface)

    my_alien_group.update()
    my_alien_group.draw(display_surface)

    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)

    my_alien_bullet_group.update()
    my_alien_bullet_group.draw(display_surface)

    #update game object 
    my_game.update()
    my_game.draw()
    pygame.display.update()
    clock.tick(60)
pygame.quit()