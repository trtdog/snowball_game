add_library('minim')
import random


def get_game_info():
    images = {}
    image_names = ['background', 'crosshair', 'player_aim', 'player_idle', 'player_pickup1', 'player_pickup2', 'player_throw1',
                   'player_throw2', 'present', 'snowball', 'snowball_break1', 'snowball_break2', 'snowflake', 'sword', 'target_slide1',
                   'target_slide2', 'target_walk1', 'target_walk2', 'target_walk3']
    image_files = []
    with open("info.txt") as f:
        lines = f.readlines()
        for l in lines[1:4]:
            image_files += l.rstrip(',\n').split(', ')
        for index, image_name in enumerate(image_names):
            images[image_name] = image_files[index]
            
        game_settings = [l.rstrip().split(' = ') for l in lines[6:]]
    return images, game_settings

                
def player_throw():
    for i in range(1, len(player_sprites)):
        image(player_sprites[i][0], player_sprites[i][1], player_sprites[i][2],
                player_sprites[i][3], player_sprites[i][4])


def draw_snowball():
    global sb_vertexX, sb_vertexY
    if sb_vertexX:
        snowball_sprites[0][1] -= sbXincr
        a = (SB_START_Y-sb_vertexY) / (SB_START_X-sb_vertexX)**2
        snowball_sprites[0][2] = (SB_START_Y-sb_vertexY) * (snowball_sprites[0][1]-sb_vertexX)**2\
        // (SB_START_X-sb_vertexX)**2 + sb_vertexY
        
        snowballCollided = detect_collision(snowball_sprites[0][1:], toboggan_down_sprites[0][1:]) or \
                detect_collision(snowball_sprites[0][1:], toboggan_up_sprites[0][1:]) or \
                detect_collision(snowball_sprites[0][1:], (bgX-50, bgY, 50, canvasH)) or \
                detect_collision(snowball_sprites[0][1:], (bgX, int(hill_points[-1][1])-snowball_sprites[0][-1], canvasW, canvasH)) or \
                detect_collision(snowball_sprites[0][1:], hill_points, True)
        
        if snowballCollided:
            snowball_sprites[1][1], snowball_sprites[1][2] = snowball_sprites[0][1], snowball_sprites[0][2]
            snowball_sprites[2][1], snowball_sprites[2][2] = snowball_sprites[0][1], snowball_sprites[0][2]
            sb_vertexX, sb_vertexY = None, None
            snowball_sprites[0][1], snowball_sprites[0][2] = 872, 604   
            image(*snowball_sprites[1])
            image(*snowball_sprites[2])
    
    image(*snowball_sprites[0])


def draw_crosshair():
    crosshairX, crosshairY = mouseX - CROSSHAIR_W//2+1, mouseY - CROSSHAIR_H//2+3
    image(crosshair, crosshairX, crosshairY, CROSSHAIR_W, CROSSHAIR_H)
    

def get_hill_points(num_points):
    hill_points = []
    for i in range(num_points): 
        t = i / float(num_points-1)
        x = bezierPoint(0, 85, 160, 360, t)
        y = bezierPoint(435, 435, 685, 683, t)
        hill_points.append((x, y))
    return hill_points


def get_tobaggan_radians(hill_points):
    t_radians = []
    for i, p in enumerate(hill_points, -1):
        m = (p[1]-hill_points[i][1]) / float((p[0]-hill_points[i][0]))
        t_radians.append(atan(m))    # atan() returns a value in radians
    return t_radians
        

def draw_tobogganer():
    global point_count, goingDown
    
    pushMatrix()
    translate(toboggan_down_sprites[0][1], toboggan_down_sprites[0][2]-67)    # Moves the origin to the pivot point
    rotate(toboggan_radians[point_count-1])
    popMatrix()
    if goingDown:
        if frameCount % game_setting_options[game_settings[1][0]][game_settings[1][1]][0] == 0:
            if point_count % 2 == 0:
                toboggan_down_sprites[0][1] = round(hill_points[point_count][0])
                toboggan_down_sprites[0][2] = round(hill_points[point_count][1])-67
                image(*toboggan_down_sprites[0])        
            elif point_count % 2 == 1:
                toboggan_down_sprites[1][1] = round(hill_points[point_count][0])
                toboggan_down_sprites[1][2] = round(hill_points[point_count][1])-67
                image(*toboggan_down_sprites[1])
            
            point_count += 1
            if point_count == len(hill_points)-1:
                goingDown = False
    
    else:
        if frameCount % game_setting_options[game_settings[1][0]][game_settings[1][1]][1] == 0:
            if point_count % 3 == 1:
                toboggan_up_sprites[0][1] = round(hill_points[point_count][0])
                toboggan_up_sprites[0][2] = round(hill_points[point_count][1])-67
                image(*toboggan_up_sprites[0])        
            elif point_count % 3 == 2:
                toboggan_up_sprites[1][1] = round(hill_points[point_count][0])
                toboggan_up_sprites[1][2] = round(hill_points[point_count][1])-67
                image(*toboggan_up_sprites[1])        
            elif point_count % 3 == 0:
                toboggan_up_sprites[2][1] = round(hill_points[point_count][0])
                toboggan_up_sprites[2][2] = round(hill_points[point_count][1])-67
                image(*toboggan_up_sprites[2])
        
        point_count -= 1
        if point_count == 0:
            goingDown = True        


def draw_snowflakes():
    pass


def detect_collision(sprite1, sprite2, curveObj=False):
    sprite1X, sprite1Y, sprite1W, sprite1H = sprite1
    if not curveObj:
        sprite2X, sprite2Y, sprite2W, sprite2H = sprite2
        return (sprite2X < sprite1X < sprite2X+sprite2W or sprite2X < sprite1X+sprite1W < sprite2X+sprite2W) and \
            (sprite2Y < sprite1Y < sprite2Y+sprite2H or sprite2Y < sprite1Y+sprite1H < sprite2Y+sprite2H)
    else:
        # if the sprite2 is a curve, I'm passing a list of points as the argument
        for p in sprite2:
            if sprite1X <= p[0] and sprite1Y+sprite1H >= p[1]:
                return True


def draw_menu():
    pass


def game_end():
    pass


def mousePressed():
    global sb_vertexX, sb_vertexY, drawThrow
    if not sb_vertexX:
        player_throw()
        sb_vertexX, sb_vertexY = mouseX, mouseY
        snowballX, snowballY = SB_START_X, SB_START_Y


def setup():
    """Sets up all the key variables in the game"""
    
    global player_sprites
    global snowball_sprites
    global sbXincr, SB_START_X, SB_START_Y, sb_vertexX, sb_vertexY
    global crosshair, CROSSHAIR_W, CROSSHAIR_H
    global bg, bgX, bgY, canvasW, canvasH
    global hill_points, point_count, toboggan_down_sprites, toboggan_up_sprites, toboggan_radians, goingDown
    global game_settings, game_setting_options
    
    game_setting_options = {
                            'snowball_speed':
                                {'low': 10, 'medium': 15, 'high': 20},    # u = x-inc
                            'toboggan_speed':
                                {'low': [3, 10], 'medium': [2, 8], 'high': [1, 6]},    # u = frameCount/deltaFrames, [a, b] a=down, b=up
                            'crosshair_width':
                                {'low': 30, 'medium': 50, 'high': 70},    # u = p
                            'crosshair_height':
                                {'low': 30, 'medium': 50, 'high': 70},    # u = p
                            'snowing':
                                {'low': 5, 'medium': 10, 'high': 15}    # u = delta snowballs / 60 frameCount
                                }
    images, game_settings = get_game_info()
    high_score = game_settings.pop(0)[1]
    
    canvasW, canvasH = 1000, 800
    bg = loadImage(images['background'])
    bgX, bgY = 0, 0
    
    player_sprites = [
                [loadImage(images['player_idle']), 870, 683-125, 75, 125],
                [loadImage(images['player_aim']), 870, 683-125, 75, 125],
                [loadImage(images['player_throw1']), 870, 683-125, 75, 125],
                [loadImage(images['player_throw2']), 870, 683-125, 75, 125],
                [loadImage(images['player_pickup1']), 870, 683-125, 75, 125],
                [loadImage(images['player_pickup2']), 870, 683-125, 75, 125]
                ]    #Sprite parameters: image, x, y, w, h
      
    crosshair = loadImage(images['crosshair'])
    CROSSHAIR_W = game_setting_options[game_settings[2][0]][game_settings[2][1]]
    CROSSHAIR_H = game_setting_options[game_settings[3][0]][game_settings[3][1]]
    
    snowball_sprites = [
                         [loadImage(images['snowball']), 920, 585, 18, 18],
                         [loadImage(images['snowball_break1']), 920, 585, 25, 25],
                         [loadImage(images['snowball_break2']), 920, 585, 40, 40]
                         ]
    # scale of the bg (p:m) = 1000: 100 = 10:1 and game is at 60fps
    # snowball is thrown at 90m/s = 900p/s = 15p/frame #NOTE! FPS is at 20 but should be at 60 so the snowball is 3 times slower
    sbXincr = game_setting_options[game_settings[0][0]][game_settings[0][1]]*3    
    SB_START_X, SB_START_Y = 920, 585
    sb_vertexX, sb_vertexY = None, None
    
    hill_points = get_hill_points(40)
    point_count = 1
    toboggan_radians = get_tobaggan_radians(hill_points)
    toboggan_down_sprites = [
                             [loadImage(images['target_slide1']), hill_points[0][0], hill_points[0][1]-67, 75, 67],
                             [loadImage(images['target_slide2']), hill_points[0][0], hill_points[0][1]-67, 75, 67]
                             ]
    toboggan_up_sprites = [
                           [loadImage(images['target_walk1']), hill_points[-1][0], hill_points[-1][1]-67, 75, 67],
                           [loadImage(images['target_walk2']), hill_points[-1][0], hill_points[-1][1]-67, 75, 67],
                           [loadImage(images['target_walk3']), hill_points[-1][0], hill_points[-1][1]-67, 75, 67]
                           ]
    goingDown = True
    
    image(bg, bgX, bgY, canvasW, canvasH)
    image(*snowball_sprites[0])
    image(crosshair, 0, 0, CROSSHAIR_W, CROSSHAIR_H)
    image(*toboggan_down_sprites[0])
    image(*player_sprites[0])

    size(1000, 800)
    noCursor()
    frameRate(60)

    
def draw():
    """Redraws every sprite 60 fps to show the change in motion"""
    
    image(bg, bgX, bgY, canvasW, canvasH)
    draw_snowball()
    draw_crosshair()
    draw_tobogganer()
    image(*player_sprites[0])
    noFill()
