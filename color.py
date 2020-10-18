import pygame, sys
from os import path

WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
ORANGE = (255, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (0, 0, 255)
BLACK  = (0, 0, 0)

WIDTH  = 480
HEIGHT = 600
POWERUP_TIME = 5000

font_name = pygame.font.match_font('arial') 
pygame.init()
pygame.display.set_mode((WIDTH,HEIGHT))
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'msc')
meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()

                   
# load all game graphics
background = pygame.image.load(path.join(img_dir, "space.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_blue.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_small2.png', 'meteorBrown_big3.png',
                'meteorBrown_big2.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png',
               'meteorBrown_tiny1.png'
               ]

for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
# load all game sounds
explosion_anim = {} # explode animation
explosion_anim['lg']     = []
explosion_anim['sm']     = []
explosion_anim['player'] = []

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
    
# making in game power ups
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()

player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))    
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'Powerup1.wav'))
gun_power = pygame.mixer.Sound(path.join(snd_dir, 'Powerup2.wav'))
hit_player = pygame.mixer.Sound(path.join(snd_dir,'Hit_Hurt1.wav')) 
#explode_sound = pygame.mixer.Sound(path.join(snd_dir, 'Explosion.wav'))
explode_sounds = []
for snd in ['Explosion.wav','Explosion2.wav']:
    explode_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

# adding music
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.3)
