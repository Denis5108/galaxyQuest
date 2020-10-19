import pygame, sys
from shooter import *
from color import *
from os import path
import random

# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder>
# licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial') # instead of knowing the exact name pygame
# will serch through the system to find it.

class Button(pygame.sprite.Sprite):

    def __init__(self, width, height, x, y, color, text=''):
        pygame.sprite.Sprite.__init__(self)
        self.width  = width
        self.height = height
        self.color = color
        self.image  = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.rect.x = x
        self.rect.y = y
        self.text = text
        if (self.text != ''):
            self.font = pygame.font.Font(None, 20)
            self.surf = self.font.render(self.text, True, BLACK)
            imgW = self.surf.get_width()
            imgH = self.surf.get_height()
            self.image.blit(self.surf, [width/2 - imgW/2, height/2 - imgH/2])
            
    def onClick(self, event, place):
        if self.rect.collidepoint(event.pos):
            # btn_snd.play()
            if self.text == 'Play':
                place = 2
            if self.text == 'Back':
                place = 3
            if self.text == 'Setting':
                place = 4
            if self.text == 'Quit':
                place = 0
            return place

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.life = 100
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
            
        # if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -5
        if keys[pygame.K_RIGHT]:
            self.speedx = 5
        if keys[pygame.K_SPACE]:
            self.shoot()
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
        self.rect.x += self.speedx
        
    def powerup(self):
        self.power += 1
        self.power_timer = pygame.time.get_ticks()
        
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
        
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        #self.image_orig = meteor_img
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9)
        # collision circles
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-12, 12)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360 # divide by 360 and give me what is remaining
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
def draw_shieldBar(surf, x, y, pct): # pct means percentage
    if pct < 0:
        pct = 0
        
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
  
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    #fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    for i in range(int(fill / 5)):
        pygame.draw.rect(surf, (8 * i, i, 0), (x + 5 * i, y, 5, BAR_HEIGHT))
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def game_over_screen():
    global highScore
    gameScreen = 1
    #all_sprites.add(btn3)
    waiting = True
    while waiting:
        clock.tick(30)
        if gameScreen == 1:
            all_sprites = pygame.sprite.Group()
            screen.blit(background, background_rect)
            draw_text(screen,"Galaxy Quest", 50, WIDTH/2, 90)
            draw_text(screen, "High Score", 20, WIDTH/2,160)
            draw_text(screen, str(highScore), 20, WIDTH/2,200)
            btn1 = Button(100, 40, 190,  HEIGHT/2, WHITE,  'Play')
            all_sprites.add(btn1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                gameScreen = btn1.onClick(event, gameScreen)

        if gameScreen == 2:
            waiting = False
        
        all_sprites.draw(screen)
        pygame.display.update()

pygame.mixer.music.play(loops=-1)
gameOver = True

file = open("HighScore.txt", "r")
highScore = int(file.read())
file.close()

gamePause = False
while True:

    if gameOver:
        game_over_screen()
        gameOver = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group() # create a group of mobs
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(random.randrange(8, 24)):
            newmob()
        score = 0
            
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                if gamePause:
                    gamePause = False
                else:
                    draw_text(screen, "Game Paused", 50, WIDTH/2, HEIGHT/2)
                    gamePause = True
    if not gamePause:
        # update      
        all_sprites.update()
        # check to see if a bullet hit a mob
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += hit.radius
            random.choice(explode_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            # explode_sound.play()
            if random.random() > 1.5:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            newmob()

        # check to see if a mob hit the player. Set the value to true if you want to check for collision
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            hit_player.play()
            expl = Explosion(hit.rect.center, 'sm')
            player.shield -= hit.radius * .7
            all_sprites.add(expl)

            newmob()
            if player.shield <= 0:
                player_die_sound.play()
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100
            
        # check to see if player hit a powerup
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                shield_sound.play()
                player.shield += 20
                if player.shield >= 100:
                    player.shield = 100
            if hit.type == 'gun':
                gun_power.play()
                player.powerup()
                
        # if the player dies and the explosion has finshed playing
        if player.lives == 0 and not death_explosion.alive():
            gameOver = True
            file = open("HighScore.txt", "w")
            file.write(str(highScore))
            file.close()

        # draw / render
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)

        if highScore < score:
            highScore = score

        draw_text(screen, "Player Score {}".format(score), 18, WIDTH / 2, 10)
        draw_text(screen, "High Score " + str(highScore), 18, WIDTH/2, 30)


        draw_shieldBar(screen, 5, 5, player.shield)
        draw_lives(screen, WIDTH -100, 5, player.lives, player_mini_img)
        draw_text(screen, "Press 'p' to pause Game",15, 410, 30)
    pygame.display.update()