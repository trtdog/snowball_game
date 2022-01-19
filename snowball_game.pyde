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
        for line in lines[1:4]:
            image_files += line.rstrip(',\n').split(', ')
        for index, image_name in enumerate(image_names):
            images[image_name] = image_files[index]
            
        game_settings = [line.rstrip().split(' = ') for line in lines[6:]]
    return images, game_settings

                                    
def player_throw():
    for i in range(1, len(player_sprites)):
        image(player_sprites[i][0], player_sprites[i][1], player_sprites[i][2],
                player_sprites[i][3], player_sprites[i][4])


def draw_snowball():
    global sb_vertexX, sb_vertexY, d, Vi, score, sb_inverse
    
    if sb_vertexX:
        t = frameCount - sb_start_time    # [t] = 1/60s
        d = sb_vertexY - SB_START_Y
        Vi = (Vt**2 - 2*a*d)**0.5
        snowball_sprites[0][2] = int(round((15) * t**2 - Vi*t*1000000/3600 + 585))
        #print((snowball_sprites[0][2] - sb_vertexY))
        #print((SB_START_Y - sb_vertexY)/(SB_START_X - sb_vertexX)**2)
        n = ( abs(snowball_sprites[0][2] - sb_vertexY) /
             ((SB_START_Y-sb_vertexY) / float((SB_START_X-sb_vertexX)**2)) )
        if snowball_sprites[0][2] - sb_vertexY <= 0:
            sb_inverse = True
        snowball_sprites[0][1] = n**0.5+sb_vertexX if not sb_inverse else -n**0.5+sb_vertexX
        snowball_sprites[0][1] = int(round(snowball_sprites[0][1]))
        #print(snowball_sprites[0][2], Vi*t, (0.0002*1000000/3600) * t**2 * t**2)
                
        playerHit = detect_collision(snowball_sprites[0][1:], toboggan_down_sprites[0][1:]) or \
                    detect_collision(snowball_sprites[0][1:], toboggan_up_sprites[0][1:])
        if playerHit:
            score += 1
        
        snowballCollided = playerHit or \
                detect_collision(snowball_sprites[0][1:], (bgX-50, bgY, 50, canvasH)) or \
                detect_collision(snowball_sprites[0][1:], (bgX, int(hill_points[-1][1])-snowball_sprites[0][-1], canvasW, canvasH+10000)) or \
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
        return (sprite2X <= sprite1X <= sprite2X+sprite2W or sprite2X <= sprite1X+sprite1W <= sprite2X+sprite2W) and \
            (sprite2Y <= sprite1Y <= sprite2Y+sprite2H or sprite2Y <= sprite1Y+sprite1H <= sprite2Y+sprite2H)
    else:
        # if the sprite2 is a curve, pass a list of points as the argument
        for p in sprite2:
            if sprite1X <= p[0] and sprite1Y+sprite1H >= p[1]:
                return True
    
    
def draw_menu():
    global startX

    textFont(font, 20)
    fill(255, 255, 255)
    text("Score: "+str(score), canvasW-60, 40)
    text("High Score: "+str(high_score), canvasW-83, 80)
        
    for i, boundary in enumerate(all_boundaries):
        top_left = boundary[0]
        bottom_right = boundary[1]
        rectMode(CORNERS)
        rect(top_left[0], top_left[1], bottom_right[0], bottom_right[1])

        textAlign(CENTER, CENTER)
        fill(0, 0, 0)
        # Use the midpoint formula to find the midpoint of the side of the button
        text(button_texts[i], (top_left[0]+bottom_right[0])/2, (top_left[1]+bottom_right[1])/2)
        noFill()


def draw_setting():
    fill(160)
    rectMode(CORNERS)
    rect((1000-500)/2, (800-400)/2, (1000-500)/2+500, (800-400)/2+400)
    
    startY = 275
    fill(0, 0, 0)
    textFont(font, 20)
    textAlign(CENTER, CENTER)
    for option, amounts in game_setting_options.items():
        option = option.split('_')
        option = [option[i].title() for i in range(len(option))]
        option = ' '.join(option) + ':'
        
        startX = 270
        top_left = (startX, startY)
        bottom_right = (450, startY+40)
        parameter = text(option, (top_left[0]+bottom_right[0])/2, (top_left[1]+bottom_right[1])/2)
        noFill()
        rect(top_left[0], top_left[1], bottom_right[0], bottom_right[1])
        
        startX = 500
        for amount in amounts:
            top_left = (startX-10, startY)
            bottom_right = (startX+textWidth(amount)+10, startY+40)            
            fill(0, 0, 0)
            parameter = text(amount, (top_left[0]+bottom_right[0])/2, (top_left[1]+bottom_right[1])/2)
            noFill()
            rect(top_left[0], top_left[1], bottom_right[0], bottom_right[1])
            startX += textWidth(amount)+30
        startY += 50
            

def draw_help():
    rectMode(CORNERS)
    fill(160)
    rect((canvasW-500)/2, (canvasH-400)/2, canvasW, (canvasH-400)/2+400)
    textFont(font, 18)
    textAlign(LEFT, LEFT)
    with open("help.txt") as f:
        startX = (canvasW-500)/2+10
        startY = (canvasH-400)/2 + 20
        fill(0, 0, 0)
        for line in f:
            line = line.rstrip()
            text(line, startX, startY)
            startY += 25
            

def draw_resume():
    top_left = all_boundaries[2][0]
    bottom_right = all_boundaries[2][1]
    fill(255, 255, 255)
    rect(top_left[0], top_left[1], bottom_right[0], bottom_right[1])
    
    textAlign(CENTER, CENTER)
    textFont(font, 19)
    fill(0, 0, 0)    
    text("Resume", (top_left[0]+bottom_right[0])/2, (top_left[1]+bottom_right[1])/2)
    noFill()
        

def game_end():
    pass


def detect_button_pressed(boundary):
    return boundary[0][0] <= mouseX <= boundary[1][0] and boundary[0][1] <= mouseY <= boundary[1][1]


def menu_system():
    """Checks if a button is pressed and if it is, then perform that action"""

    global buttonActivated, buttonPressed, prev_index, startGame
    
    index = None
    for boundary in all_boundaries:
        if detect_button_pressed(boundary) and (all_boundaries.index(boundary) == prev_index or not buttonActivated):
            index = all_boundaries.index(boundary)
            buttonPressed = True
            if index != 3:
                buttonActivated = not buttonActivated
                if buttonActivated:
                    cursor()
                    noLoop()    # stops draw() from executing
                    prev_index = index
                else:
                    noCursor()
                    loop()    # resumes draw() to execute
                    prev_index = None
            break
            
    # Using an if-elif-else chain instead of multiple if statements because you can't press multiple buttons simultaneously
    if index == 0:
        draw_setting()
    elif index == 1:    
        draw_help()
    elif index == 2:
        draw_resume()
    elif index == 3:
        startGame = True
    
    
def mouseReleased():
    global sb_vertexX, sb_vertexY, drawThrow, sb_start_time, sb_inverse, startGame, buttonPressed
    
    if startGame and detect_button_pressed(( (canvasW/2-100, canvasH/2-50), (canvasW/2+100, canvasH/2+50) )):
        buttonPressed = True
        startGame = False
        noCursor()
    
    menu_system()
    
    # Checking snowball thrown
    if not buttonPressed and not sb_vertexX:     # !!!! change the if statement to only run if a button isn't pressed
        player_throw()
        sb_start_time = frameCount
        sb_vertexX, sb_vertexY = mouseX, mouseY
        snowballX, snowballY = SB_START_X, SB_START_Y
        sb_inverse = False
    
    buttonPressed = False


def setup():
    """Sets up all the key variables in the game"""
    
    global player_sprites
    global snowball_sprites, SB_START_X, SB_START_Y, sb_vertexX, sb_vertexY, sb_start_time, a, d, Vt, Vi, sb_inverse
    global crosshair, CROSSHAIR_W, CROSSHAIR_H
    global bg, bgX, bgY, canvasW, canvasH
    global hill_points, point_count, toboggan_down_sprites, toboggan_up_sprites, toboggan_radians, goingDown
    global game_settings, game_setting_options, high_score, score, startGame
    global all_boundaries, button_lengths, BUTTON_HEIGHT, startX, startY, buttonActivated, buttonPressed
    global font, button_texts, prev_index
    
    game_setting_options = {
                            'snowball_speed':
                                {'low': 10, 'medium': 15, 'high': 20},    # u = x-inc
                            'toboggan_speed':
                                {'low': [3, 10], 'medium': [2, 8], 'high': [1, 6]},    # u = frameCount/deltaFrames, [a, b] a=down, b=up
                            'crosshair_width':
                                {'low': 30, 'medium': 50, 'high': 70},    # u = p
                            'crosshair_height':
                                {'low': 30, 'medium': 50, 'high': 70},    # u = p
                            'snowing_rate':
                                {'low': 5, 'medium': 10, 'high': 15}    # u = delta snowballs / 60 frameCount
                                }
    images, game_settings = get_game_info()
    high_score = game_settings.pop(0)[1]
    score = 0
    startGame = True
    
    bg = loadImage(images['background'])
    bgX, bgY = 0, 0
    canvasW, canvasH = 1000, 800
    
    all_boundaries = []
    button_lengths = (120, 100, 110, 110)    # Order: Most left -> Most right on the canvas
    BUTTON_HEIGHT = 50
    button_texts = ('Settings', 'Help', 'Pause', 'Restart')
    font = createFont("Arial", 16, True)    # loads the font into RAM, memory intensive and a slow process
    startX, startY = 879, 730
    
    for i in range(len(button_lengths)):
        top_left = (startX, startY)
        bottom_right = (startX+button_lengths[i], startY+BUTTON_HEIGHT)
        all_boundaries.append((top_left, bottom_right))    
        if i != 3:
            startX -= button_lengths[i+1]
    buttonActivated = False
    buttonPressed = False
    prev_index = None
    
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
    SB_START_X, SB_START_Y = 920, 585
    sb_vertexX, sb_vertexY = None, None
    sb_start_time = frameCount
    a = 0.0004
    d = None
    Vt = 0
    Vi = None
    sb_inverse = False
    
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

    size(1000, 800)
    frameRate(60)

    
def draw():
    """Redraws every sprite 60 fps to show the change in motion"""
    
    global score, sb_vertexX, sb_vertexY
    
    if startGame:
        rectMode(CORNER)
        fill(150)
        rect(0, 0, canvasW, canvasH)
        cursor()
        rectMode(CENTER)
        fill(255)
        rect(canvasW/2, canvasH/2, 200, 100)

        fill(0)
        textAlign(CENTER, CENTER)
        textFont(font, 60)
        text("Snowball Game", canvasW/2, 200)
        textFont(font, 40)
        text("PLAY", canvasW/2, canvasH/2)        
        
        score = 0
        sb_vertexX, sb_vertexY = None, None

    else:
        image(bg, bgX, bgY, canvasW, canvasH)
        draw_menu()
        draw_snowball()
        draw_crosshair()
        draw_tobogganer()
        image(*player_sprites[0])
