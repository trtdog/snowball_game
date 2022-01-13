add_library('minim')
import random


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
        if snowball_sprites[0][1] < 0:
            sb_vertexX, sb_vertexY = None, None
            snowball_sprites[0][1], snowball_sprites[0][2] = 872, 604    
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
        if frameCount % 4 == 0:
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


def detect_collision(sprite1X, sprite1Y, sprite2X, sprite2Y, sprite2W, sprite2H):
    collided = False
    if sprite2X < sprite1X < sprite2X+sprite2W or sprite2Y < sprite1Y < sprite2Y+sprite2H:
        collided = True
    return collided


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

    canvasW, canvasH = 1000, 800

    bg = loadImage("background.png")
    bgX, bgY = 0, 0
    
    player_sprites = [
                [loadImage("player_idle.png"), 870, 683-125, 75, 125],
                [loadImage("player_aim.png"), 870, 683-125, 75, 125],
                [loadImage("player_throw1.png"), 870, 683-125, 75, 125],
                [loadImage("player_throw2.png"), 870, 683-125, 75, 125],
                [loadImage("player_pickup1.png"), 870, 683-125, 75, 125],
                [loadImage("player_pickup2.png"), 870, 683-125, 75, 125]
                ]    #Sprite parameters: image, x, y, w, h
      
    crosshair = loadImage("crosshair.png")
    CROSSHAIR_W, CROSSHAIR_H = 50, 50
    
    snowball_sprites = [
                         [loadImage("snowball.png"), 920, 585, 18, 18],
                         [loadImage("snowball_break1.png"), 920, 585, 18, 18],
                         [loadImage("snowball_break2.png"), 920, 585, 18, 18]
                         ]
    # scale of the bg (p:m) = 1000: 100 = 10:1 and game is at 60fps
    sbXincr = 15*3    # snowball is thrown at 90m/s = 900p/s = 15p/frame #NOTE! FPS is at 20 but should be at 60 so the snowball is 3 times slower
    SB_START_X, SB_START_Y = 920, 585
    sb_vertexX, sb_vertexY = None, None
    
    hill_points = get_hill_points(40)
    point_count = 1
    toboggan_radians = get_tobaggan_radians(hill_points)
    toboggan_down_sprites = [
                             [loadImage("target_slide1.png"), hill_points[0][0], hill_points[0][1]-67, 75, 67],
                             [loadImage("target_slide2.png"), hill_points[0][0], hill_points[0][1]-67, 75, 67]
                             ]
    toboggan_up_sprites = [
                           [loadImage("target_walk1.png"), hill_points[-1][0], hill_points[-1][1]-67, 75, 67],
                           [loadImage("target_walk2.png"), hill_points[-1][0], hill_points[-1][1]-67, 75, 67],
                           [loadImage("target_walk3.png"), hill_points[-1][0], hill_points[-1][1]-67, 75, 67]
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
