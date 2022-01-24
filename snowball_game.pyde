add_library('minim')

from random import randint


def get_game_info(img_line_end, settings_line_start):
    images = {}
    image_names = ['background', 'crosshair', 'player_aim', 'player_idle', 'player_pickup1', 'player_pickup2', 'player_throw1',
                   'player_throw2', 'present', 'snowball', 'snowball_break1', 'snowball_break2', 'snowflake', 'sword', 'target_slide1',
                   'target_slide2', 'target_walk1', 'target_walk2', 'target_walk3', 'player_wait', 'player_walk1', 'player_walk2', 
                   'player_walk3', 'santa_fly1', 'santa_fly2', 'background2', 'player_dying1', 'player_dying2', 
                   'blood_splatter1', 'blood_splatter2', 'player_fall1', 'player_fall2']
    image_files = []
    with open("info.txt") as f:
        lines = f.readlines()
        for line in lines[1:img_line_end]:
            image_files += line.rstrip(',\n').split(', ')
        for index, image_name in enumerate(image_names):
            images[image_name] = image_files[index]
            
        game_settings = [line.rstrip().split(' = ') for line in lines[settings_line_start:]]
    return images, game_settings


def draw_player():
    global playerThrow, player_count
    
    image(*player_sprites[player_count])
    if mousePressed:
        player_count = 1
    elif playerThrow:
        sb_throw_sound.play()
        sb_throw_sound.rewind()
        player_count += 1
        if player_count == len(player_sprites)-1:
            playerThrow = False
    else:
        player_count = 0
    

def draw_snowball():
    global sb_vertexX, sb_vertexY, d, Vi, score, sb_inverse, scene, win
    
    if sb_vertexX:
        t = frameCount - sb_start_time    # [t] = 1/60s
        d = sb_vertexY - SB_START_Y
        Vi = (Vt**2 - 2*a*d)**0.5
        snowball_sprites[0][2] = int(round((16) * t**2 - Vi*t*1000000/3600 + 585))
        #print((snowball_sprites[0][2] - sb_vertexY))
        #print((SB_START_Y - sb_vertexY)/(SB_START_X - sb_vertexX)**2)
        
        n = ( abs(snowball_sprites[0][2] - sb_vertexY) /
            ((SB_START_Y-sb_vertexY) / float((SB_START_X-sb_vertexX)**2)) )
        if snowball_sprites[0][2] - sb_vertexY <= 0:
            sb_inverse = True

        snowball_sprites[0][1] = n**0.5+sb_vertexX if not sb_inverse else -n**0.5+sb_vertexX
        snowball_sprites[0][1] = int(round(snowball_sprites[0][1]))
            
        targetHit = goingDown and detect_collision(snowball_sprites[0][1:], toboggan_down_sprites[0][1:]) or \
                    not goingDown and detect_collision(snowball_sprites[0][1:], toboggan_up_sprites[0][1:])
        if targetHit:
            target_hit_sound.play()
            target_hit_sound.rewind()
            score += 1
        
        snowballCollided = targetHit or \
                detect_collision(snowball_sprites[0][1:], (bgX-50, bgY, 50, canvasH)) or \
                detect_collision(snowball_sprites[0][1:], (bgX, int(hill_points[-1][1])-snowball_sprites[0][-1], canvasW, canvasH)) or \
                detect_collision(snowball_sprites[0][1:], hill_points, True)
        
        if snowballCollided:                
            snowball_sprites[1][1], snowball_sprites[1][2] = snowball_sprites[0][1], snowball_sprites[0][2]
            snowball_sprites[2][1], snowball_sprites[2][2] = snowball_sprites[0][1], snowball_sprites[0][2]
            sb_vertexX, sb_vertexY = None, None
            snowball_sprites[0][1], snowball_sprites[0][2] = SB_START_X, SB_START_Y   
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
    global point_count, goingDown, toboggan_index
    
    if goingDown:
        if frameCount % game_setting_options[game_settings[2][0]][game_settings[2][1]][0] == 0:
            if point_count % 2 == 0:
                toboggan_down_sprites[0][1] = round(hill_points[point_count][0])
                toboggan_down_sprites[0][2] = round(hill_points[point_count][1])-67
                index = 0
            elif point_count % 2 == 1:
                toboggan_down_sprites[1][1] = round(hill_points[point_count][0])
                toboggan_down_sprites[1][2] = round(hill_points[point_count][1])-67
                index = 1
            
            point_count += 1
            if point_count == len(hill_points)-1:
                goingDown = False
    
    else:
        if frameCount % game_setting_options[game_settings[2][0]][game_settings[2][1]][1] == 0:
            if point_count % 3 == 1:
                toboggan_up_sprites[0][1] = round(hill_points[point_count][0])
                toboggan_up_sprites[0][2] = round(hill_points[point_count][1])-67
                index = 0 
            elif point_count % 3 == 2:
                toboggan_up_sprites[1][1] = round(hill_points[point_count][0])
                toboggan_up_sprites[1][2] = round(hill_points[point_count][1])-67
                index = 1      
            elif point_count % 3 == 0:
                toboggan_up_sprites[2][1] = round(hill_points[point_count][0])
                toboggan_up_sprites[2][2] = round(hill_points[point_count][1])-67
                index = 2
        
            point_count -= 1
            if point_count == 0:
                goingDown = True

    pushMatrix()
    if goingDown:
        translate(toboggan_down_sprites[toboggan_index][1], toboggan_down_sprites[toboggan_index][2])    # Moves the origin to the pivot point
        rotate(toboggan_radians[point_count-1])
        image(toboggan_down_sprites[toboggan_index][0], 0, 0, toboggan_down_sprites[toboggan_index][-2], toboggan_down_sprites[toboggan_index][-1])
    else:
        translate(toboggan_up_sprites[toboggan_index][1], toboggan_up_sprites[toboggan_index][2])
        rotate(toboggan_radians[point_count-1])
        image(toboggan_up_sprites[toboggan_index][0], 0, 0, toboggan_up_sprites[toboggan_index][-2], toboggan_up_sprites[toboggan_index][-1])
    popMatrix()


def draw_snowflakes():
    snowflake_sprites.append([loadImage(images['snowflake']), randint(0, canvasW-10), -10, 10, 10])
    count = 0
    while count < len(snowflake_sprites):
        image(*snowflake_sprites[count])
        snowflake_sprites[count][2] += 5
        
        if detect_collision(snowflake_sprites[count][1:], hill_points, curveObj=True) or \
        detect_collision(snowflake_sprites[count][1:], (bgX, int(hill_points[-1][1]), canvasW, canvasH)):
            del snowflake_sprites[count]
        else:
            count += 1
            

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
    global startX, num_snowballs

    textFont(font, 20)
    fill(255, 255, 255)
    text("High Score: "+str(high_score), canvasW-83, 40)
    text("Score: "+str(score), canvasW-60, 80)
    text("Snowballs: "+str(num_snowballs), canvasW-80, 120)
        
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


def detect_button_pressed(boundary):
    return boundary[0][0] <= mouseX <= boundary[1][0] and boundary[0][1] <= mouseY <= boundary[1][1]


def menu_system():
    """Checks if a button is pressed and if it is, then perform that action"""

    global buttonActivated, buttonPressed, prev_index, scene
    
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
        scene = 1
 

def game_middle():
    image(bg, bgX, bgY, canvasW, canvasH)
    draw_menu()
    draw_snowball()
    draw_player()
    draw_crosshair()
    draw_tobogganer()
    draw_snowflakes()
    if num_snowballs == 0:
        win = score >= 0.3 * initial_snowballs    # If the player hits at least 30% of his shots, he wins the game
        scene = 3
    

def game_end():
    global scene, win, bgX, bg_endX, player_count, santa_count
    global presentX, presentY, drop_initial_time
    global swordX, swordY
    
    image(bg, bgX, bgY, canvasW, canvasH)
    image(bg_end, bg_endX, bg_endY, bg_endW, bg_endH)
    draw_snowflakes()
    
    if bg_endX > canvasW-bg_endW:
        bg_endX -= 5
        bgX -= 5
        
        for i in range(len(player_sprites_end)):
            player_sprites_end[i][1] -= 2
        if player_count % 4 == 0 or player_count % 4 == 2:
            image(*player_sprites_end[2])
        elif player_count % 4 == 1:
            image(*player_sprites_end[1])
        elif player_count % 4 == 3:
            image(*player_sprites_end[3])
        
        player_count += 1
    
    elif win:
        if presentY < player_sprites_end[0][2] - PRESENT_H:
            if santa_flying_sprites[0][1] < canvasW:
                santa_sound.play()
                if santa_count % 2 == 0:
                    image(*santa_flying_sprites[0])
                if santa_count % 2 == 1:
                    image(*santa_flying_sprites[1])
                santa_flying_sprites[0][1] += 5
                santa_flying_sprites[1][1] += 5
                santa_count += 1
            
            if presentX >= player_sprites_end[0][1]:
                if not drop_initial_time:
                    drop_initial_time = frameCount    
                t = frameCount-drop_initial_time    # [t] = 1/60s
                vel = (a*t - 0.0001*t) * 1000000 / 3600
                presentY += vel
                image(present, presentX, presentY, PRESENT_W, PRESENT_H)
            else:
                presentX += 5
            image(*player_sprites_end[0])
        else:
            win = "game end"
    
    elif not win:
        if swordY < player_sprites_end[0][2] - SWORD_H:
            if santa_flying_sprites[0][1] < canvasW:
                santa_sound.play()
                if santa_count % 2 == 0:
                    image(*santa_flying_sprites[0])
                if santa_count % 2 == 1:
                    image(*santa_flying_sprites[1])
                santa_flying_sprites[0][1] += 5
                santa_flying_sprites[1][1] += 5
                santa_count += 1
            
            if swordX >= player_sprites_end[0][1]:
                if not drop_initial_time:
                    drop_initial_time = frameCount
                t = frameCount - drop_initial_time    # [t] = 1/60s
                vel = (a*t - 0.0001*t) * 1000000 / 3600
                swordY += vel
                image(sword, swordX, swordY, SWORD_W, SWORD_H)
            else:
                swordX += 5
            
            player_count = 4
            image(*player_sprites_end[0])
        
        else:
            death_sound.play()
            if player_count <= len(player_sprites_end) - 1:
                image(*player_sprites_end[player_count])
                player_count += 1
            else:
                win = "game end"

    if win == "game end":
        delay(4000)
        scene = 1

    
def mouseReleased():
    global sb_vertexX, sb_vertexY, sb_start_time, sb_inverse, scene, buttonPressed, playerThrow, num_snowballs
    
    # Checking restart button pressed
    if scene == 1 and detect_button_pressed(( (canvasW/2-100, canvasH/2-50), (canvasW/2+100, canvasH/2+50) )):
        buttonPressed = True
        scene = 2
        loop()
        noCursor()
    
    menu_system()
    
    # Checking snowball thrown
    if not buttonPressed and not sb_vertexX and mouseY < SB_START_Y and mouseX <= SB_START_X:
        playerThrow = True
        num_snowballs -= 1
        sb_start_time = frameCount
        sb_vertexX, sb_vertexY = mouseX, mouseY
        sb_inverse = False
    
    buttonPressed = False


def game_start():
    """Sets up all the key variables in the game and draws the start screen"""
    
    global player_sprites, player_sprites_end, player_count, playerThrow, win, images
    global santa_sound, target_hit_sound, sb_throw_sound, music, death_sound
    global snowball_sprites, num_snowballs, initial_snowballs, snowflake_sprites
    global a, d, Vt, Vi, sb_inverse, SB_START_X, SB_START_Y, sb_vertexX, sb_vertexY, sb_start_time
    global crosshair, CROSSHAIR_W, CROSSHAIR_H
    global bg, bgX, bgY, canvasW, canvasH, bg_end, bg_endX, bg_endY, bg_endW, bg_endH
    global hill_points, point_count, toboggan_down_sprites, toboggan_up_sprites, toboggan_radians, goingDown, toboggan_index
    global game_settings, game_setting_options, high_score, score, scene
    global all_boundaries, button_lengths, BUTTON_HEIGHT, startX, startY, buttonActivated, buttonPressed
    global font, button_texts, prev_index
    global santa_flying_sprites, santa_count
    global present, presentY, presentX, PRESENT_W, PRESENT_H, drop_initial_time
    global sword, swordX, swordY, SWORD_W, SWORD_H

    noLoop()
    
    minim = Minim(this)
    santa_sound = minim.loadFile("santa.mp3")
    target_hit_sound = minim.loadFile("target_hit.mp3")
    sb_throw_sound = minim.loadFile("snowball_throw.mp3")
    music = minim.loadFile("music.mp3")
    death_sound = minim.loadFile("death.mp3")

    game_setting_options = {
                            'starting_snowballs':
                                {'10': 10, '20': 20, '30': 30},
                            'snowball_speed':
                                {'low': 10, 'medium': 15, 'high': 20},    # u = x-inc
                            'toboggan_speed':
                                {'low': [3, 10], 'medium': [2, 6], 'high': [1, 6]},    # u = frameCount/deltaFrames, [a, b] a=down, b=up
                            'crosshair_width':
                                {'low': 30, 'medium': 50, 'high': 70},    # u = p
                            'crosshair_height':
                                {'low': 30, 'medium': 50, 'high': 70},    # u = p
                            'snowing_rate':
                                {'low': 5, 'medium': 10, 'high': 15}    # u = delta snowballs / 60 frameCount
                                }
    images, game_settings = get_game_info(7, 9)
    high_score = game_settings.pop(0)[1]
    score = 0
    scene = 1
    
    bg = loadImage(images['background'])
    bgX, bgY = 0, 0
    canvasW, canvasH = 1000, 800
    
    bg_end = loadImage(images['background2'])    # The bg for the end of the game
    bg_endX = canvasW-10
    bg_endY = 0
    bg_endW = 400
    bg_endH = canvasH
    
    # Drawing the menu
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
    
    playerThrow = False
    player_count = 0
    player_sprites_end = [
                          [loadImage(images['player_wait']), 870, 683-125, 75, 125],
                          [loadImage(images['player_walk1']), 870, 683-125, 75, 125],
                          [loadImage(images['player_walk2']), 870, 683-125, 75, 125],
                          [loadImage(images['player_walk3']), 870, 683-125, 75, 125],
                          [loadImage(images['player_dying1']), 870, 683-170, 100, 170],
                          [loadImage(images['blood_splatter1']), 849, 683-135, 118, 45],
                          [loadImage(images['player_fall1']), 870, 683-150, 120, 150],
                          [loadImage(images['blood_splatter2']), 814, 683-135, 220, 110],
                          [loadImage(images['player_fall2']), 870, 683-113, 150, 113],
                          [loadImage(images['player_dying2']), 870, 683-70, 180, 75]
                          ]
    win = False
    
    santa_flying_sprites = [[loadImage(images['santa_fly1']), -200, 50, 200, 138], [loadImage(images['santa_fly2']), -200, 50, 200, 138]]
    santa_count = 0
    
    present = loadImage(images['present'])
    presentX = -200
    presentY = 50
    PRESENT_W = 58
    PRESENT_H = 73
    drop_initial_time = None
    
    sword = loadImage(images['sword'])
    swordX = -200
    swordY = 40
    SWORD_W = 72
    SWORD_H = 136
    
    crosshair = loadImage(images['crosshair'])
    CROSSHAIR_W = game_setting_options[game_settings[3][0]][game_settings[3][1]]
    CROSSHAIR_H = game_setting_options[game_settings[4][0]][game_settings[4][1]]
    
    snowball_sprites = [
                         [loadImage(images['snowball']), 920, 585, 18, 18],
                         [loadImage(images['snowball_break1']), 920, 585, 25, 25],
                         [loadImage(images['snowball_break2']), 920, 585, 40, 40]
                         ]
    # scale of the bg (p:m) = 1000: 100 = 10:1 and game is at 60fps
    # snowball is thrown at 90m/s = 900p/s = 15p/frame #NOTE! FPS is at 20 but should be at 60 so the snowball is 3 times slower 
    SB_START_X, SB_START_Y = 872, 604
    sb_vertexX, sb_vertexY = None, None
    sb_start_time = frameCount
    a = 0.0004
    d = None
    Vt = 0
    Vi = None
    sb_inverse = False
    num_snowballs = game_setting_options[game_settings[0][0]][game_settings[0][1]]
    initial_snowballs = num_snowballs
    
    snowflake_sprites = []
    
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
    toboggan_index = 0
    
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
    

def setup():
    size(1000, 800)
    frameRate(60)
    game_start()
    music.loop()


def draw():
    """Redraws every sprite 60 fps to show the change in motion"""
    
    if scene == 1:
        game_start()
    elif scene == 2:
        game_middle()
    elif scene == 3:
        game_end()


def stop():
    """Closes these audio files to ensure they are not corrupted"""
    
    santa_sound.close()
    target_hit_sound.close()
    sb_throw_sound.close()
    music.close()
    death_sound.close()
    minim.stop()
    super.stop()
    
