# This program runs a helicopter game. 
# Written by Ramit Kataria

# Import statements
import simplegui, math, random

# Load image
BACKGROUND_IMAGE = simplegui.load_image("https://drive.google.com/uc?id=0B2ZIImfCEkf4Nnl1eVlFZmpwXzQ")
PLAYER_IMAGE = simplegui.load_image("https://drive.google.com/uc?id=0B2ZIImfCEkf4VmJ4QnQ5VlpMTms")
LAVA_IMAGE = simplegui.load_image("https://drive.google.com/uc?id=0B2ZIImfCEkf4N1ktalVnazlEVW8")
BALLOON_IMAGE = simplegui.load_image("https://drive.google.com/uc?id=0B2ZIImfCEkf4VWlyLXFVMF85eDQ")
LASER_IMAGE = simplegui.load_image("https://drive.google.com/uc?id=0B2ZIImfCEkf4NTZMQkxEOE0wWEk")
EXPLOSION_IMAGE = simplegui.load_image("https://drive.google.com/uc?id=0B2ZIImfCEkf4NnZ5WjZPTDdEcjg")
LANDMINE_IMAGE = simplegui.load_image("https://drive.google.com/uc?id=0B2ZIImfCEkf4VTdRblR5Y1djZzg")
COMPL_IMAGE = simplegui.load_image("https://drive.google.com/uc?id=1rNjagoe4LTgHb25X77wupOLPo3JM4UI5")
BULLET_IMAGE = simplegui.load_image("https://drive.google.com/uc?id=1xoUlB1sQ1is3K984_Zqv1N2s-RlgtGRd")
START_SCREEN_IMAGE = simplegui.load_image("https://drive.google.com/uc?id=1J9urO62x76nm3qOvp7ieI1-0Xd_tsI9u")
SCORE_BACK_IMAGE = simplegui.load_image("https://drive.google.com/uc?id=1F2G0AkYVL4_NXD0eKFN_s2P5AmkGa5Yf")

# Initialize global variables 
# Use all capital letters for constants.
WIDTH_FRAME = 1024
HEIGHT_FRAME = 576

WIDTH_BACK = 640
HEIGHT_BACK = 360

LASER_WIDTH = 111
LASER_HEIGHT = 678

# Starting values for variables
background_time = 0
THROTTLE = 4
gravity = 4.0
scroll_speed = 2.5
time = 0
cached_scspeed = 0
level = 1
game_on = False
game_won = False
started = False
forward = False
backward = False
landmine_list = []
lava_list = []
balloon_list = []
bullet_list = []

# Classes for diffent objects
class Player:
    def __init__(self):
        self.IMAGE = PLAYER_IMAGE
        self.EXPL = EXPLOSION_IMAGE
        self.pos = [WIDTH_FRAME / 2, HEIGHT_FRAME / 5]
        self.vel = [0, 0]
        self.rot = 0
        self.destroyed = False
        self.time = 0
        self.health = 100
        self.IMG_WIDTH = 295
        self.IMG_HEIGHT = 91
        self.EXPL_WIDTH = 157
        self.EXPL_HEIGHT = 229
        
    def draw(self, canvas):
        # draw helicopter image with animation
        tile_cen = (self.IMG_WIDTH / 2 + self.IMG_WIDTH * (int(self.time % 2)), 
                    self.IMG_HEIGHT / 2 + self.IMG_HEIGHT * (int(self.time // 2)))
        canvas.draw_image(self.IMAGE, tile_cen,
                          (self.IMG_WIDTH, 
                           self.IMG_HEIGHT),
                          self.pos, 
                          [self.IMG_WIDTH / 1.25, 
                           self.IMG_HEIGHT / 1.25], 
                          self.rot)
        self.time += 0.25
        
        # draw the explosion
        if self.destroyed:           
            cen_expl = (self.EXPL_WIDTH / 2 + self.EXPL_WIDTH * (int(self.time % 7)), 
                        self.EXPL_HEIGHT / 2 + self.EXPL_HEIGHT * (int(self.time // 7)))
           
            canvas.draw_image(self.EXPL, cen_expl,
                              (self.EXPL_WIDTH, 
                               self.EXPL_HEIGHT),
                              self.pos, 
                              [self.EXPL_WIDTH*2, 
                               self.EXPL_HEIGHT*2])
        
        # diffent number of columns in the spritesheets
        else:
            self.time %= 2
            
    def update(self):
        self.pos[0] += self.vel[0] - scroll_speed
        self.pos[1] += self.vel[1] + gravity
        # This is to prevent it from going outside the frame
        if self.pos[1] < 35:
            self.pos[1] = 35
            
        if self.pos[0] > 1125:
            self.pos[0] = 1125
        
        # Reduce health and end game
        if player.pos[1] > 510:
            player.health -= 2
        if player.pos[0] < 150:
            player.health = 0 
        if player.health <= 0:
            game_over()
            
    def has_collided(self, other):
        cond1 = math.fabs(other.pos[0] - self.pos[0]) < (70 - math.degrees(self.rot) + other.rad) 
        cond2 = math.fabs(other.pos[1] - self.pos[1]) < (15 - math.degrees(self.rot) + other.rad)
        if cond1 and cond2:
            return True
        
class Balloon:
    def __init__(self):
        self.IMAGE = BALLOON_IMAGE
        self.pos = [random.randrange(850, 1200), 
                    random.randrange(300, 672)]
        self.RISE = - random.randint(10, 200) / 100.0
        self.rad = 35
        self.IMG_WIDTH = 282
        self.IMG_HEIGHT = 500
 
    def draw(self, canvas):
        canvas.draw_image(self.IMAGE, 
                          (self.IMG_WIDTH / 2, 
                           self.IMG_HEIGHT / 2),
                          (self.IMG_WIDTH, 
                           self.IMG_HEIGHT),
                          self.pos, 
                          [self.IMG_WIDTH / 5.5, 
                           self.IMG_HEIGHT / 7])
        
    def update(self):
        # Horizontal movement
        self.pos[0] -=  scroll_speed
        # Vertical movement
        # Make the balloons glide on the top
        if self.pos[1] > 42.6:
            self.pos[1] += self.RISE
            
        # Pops the balloon when it gets to the laser
        if self.pos[0] < 68:
            balloon_list.remove(self)

class Lava:
    def __init__(self, image, position, time):
        self.IMAGE = image
        self.pos = position
        self.time = time
        self.IMG_WIDTH = 32
        self.IMG_HEIGHT = 32
        
    def draw(self, canvas):
        tile_cen = (self.IMG_WIDTH / 2 + self.IMG_WIDTH * (int(self.time % 6)), 
                    self.IMG_HEIGHT / 2 + self.IMG_HEIGHT * (int(self.time // 6)))
        canvas.draw_image(self.IMAGE, 
                          tile_cen,
                          (self.IMG_WIDTH, 
                           self.IMG_HEIGHT),
                          self.pos, 
                          [self.IMG_WIDTH, 
                           self.IMG_HEIGHT])
        self.time += 0.25
        self.time %= 38
        
    def update(self):
        self.pos[0] = (self.pos[0] - scroll_speed) % (WIDTH_FRAME)

class Bullet:
    def __init__(self, image, position):
        self.IMAGE = image
        self.pos = position
        self.IMG_WIDTH = 980
        self.IMG_HEIGHT = 296
                
    def draw(self, canvas):
        canvas.draw_image(self.IMAGE, 
                          (self.IMG_WIDTH / 2, 
                           self.IMG_HEIGHT / 2),
                          (self.IMG_WIDTH, 
                           self.IMG_HEIGHT),
                          self.pos, 
                          (49, 15),
                          math.radians(180))

    def update(self):
        self.pos[0] += 3
        
        # Remove the bullet when out of screen
        if self.pos[0] > 1100:
            bullet_list.remove(self)
            
    def has_collided(self, other):
        cond1 = math.fabs(other.pos[0] - self.pos[0]) < (20 + other.rad) 
        cond2 = math.fabs(other.pos[1] - self.pos[1]) < (5 + other.rad)
        if cond1 and cond2:
            return True
                
class Landmine:
    def __init__(self):
        self.IMAGE = LANDMINE_IMAGE
        self.EXPL = EXPLOSION_IMAGE
        self.SIZE = float(random.randint(10, 25)) / 100
        self.pos = [1200, random.randint(0, 500)]
        self.IMG_WIDTH = 1025
        self.IMG_HEIGHT = 1024
        self.rad = self.IMG_WIDTH / 2.0 * self.SIZE
        self.destroyed = False
        self.time = 0
        self.EXPL_WIDTH = 157
        self.EXPL_HEIGHT = 229
        
        
    def draw(self, canvas):
        canvas.draw_image(self.IMAGE, 
                          (self.IMG_WIDTH / 2, 
                           self.IMG_HEIGHT / 2),
                          (self.IMG_WIDTH, 
                           self.IMG_HEIGHT),
                          self.pos, 
                          (self.IMG_WIDTH*self.SIZE, 
                           self.IMG_HEIGHT*self.SIZE))
        
        # Explosion
        if self.destroyed: 
            if self.SIZE > 0.01:
                self.SIZE -= 0.01
            cen_expl = (self.EXPL_WIDTH / 2 + self.EXPL_WIDTH * (int(self.time % 7)), 
                        self.EXPL_HEIGHT / 2 + self.EXPL_HEIGHT * (int(self.time // 7)))
            self.time += 0.5
            canvas.draw_image(self.EXPL, cen_expl,
                              (self.EXPL_WIDTH, 
                               self.EXPL_HEIGHT),
                              self.pos, 
                              [self.EXPL_WIDTH * 5, 
                               self.EXPL_HEIGHT * 5])

    def update(self):
        self.pos[0] = (self.pos[0] - scroll_speed)
        # Remove it when out of frame
        if (self.pos[0] - self.rad) < -self.rad * 2:
            landmine_list.remove(self)

class Button:
    def __init__(self, position, text):
        self.pos = position
        self.WIDTH = 250
        self.HEIGHT = 70
        self.TEXT = text
        self.point_list = ((self.pos[0] - self.WIDTH / 2, 
                            self.pos[1] + self.HEIGHT / 2), 
                           (self.pos[0] + self.WIDTH / 2, 
                            self.pos[1] + self.HEIGHT / 2), 
                           (self.pos[0] + self.WIDTH / 2, 
                            self.pos[1] - self.HEIGHT / 2), 
                           (self.pos[0] - self.WIDTH / 2, 
                            self.pos[1] - self.HEIGHT / 2))
    
    def draw(self, canvas):
        canvas.draw_polygon(self.point_list, 6, 
                            "silver", "gray")
        canvas.draw_text(self.TEXT, 
                         (self.pos[0] - frame.get_canvas_textwidth(self.TEXT, 40) / 2, 
                          self.pos[1]+10), 40, "white")
    
    def is_clicked(self, mouse_pos):
        cond1 = math.fabs(mouse_pos[0] - self.pos[0]) <= (self.WIDTH/2) 
        cond2 = math.fabs(mouse_pos[1] - self.pos[1]) <= (self.HEIGHT/2)
        if cond1 and cond2:
            return True

# Class for calculating frames per second
class Fps:    
    def __init__(self):
        self.TIMER = simplegui.create_timer(1000, 
                                            self.update)
        self.fps = 0
        self.nb_frames_drawed = 0
        self.nb_seconds = 0

    def draw(self, canvas):
        self.nb_frames_drawed += 1
        canvas.draw_polygon(((2, 548), (106, 548), 
                             (106, 572), (2, 572)), 
                            1, "black", "red")
        canvas.draw_text("FPS: " + str(self.fps), 
                         (6, 570), 30, "black")
            
    def update(self):    
        self.fps = self.nb_frames_drawed
        self.nb_frames_drawed = 0

def draw_background(canvas):
    global background_time, WIDTH_BACK, HEIGHT_BACK
    global WIDTH_FRAME, HEIGHT_FRAME
    if game_on and game_won == False:
        background_time += 0.5
    background_time %= 359
    tile_cen_back = (WIDTH_BACK / 2 + WIDTH_BACK * (int(background_time % 14)), 
                     HEIGHT_BACK / 2 + HEIGHT_BACK * (int(background_time // 14)))
    canvas.draw_image(BACKGROUND_IMAGE, tile_cen_back,
                      (WIDTH_BACK, HEIGHT_BACK),
                      [WIDTH_FRAME / 2, HEIGHT_FRAME / 2], 
                      [WIDTH_FRAME, HEIGHT_FRAME])

# Handler to start game (resets everything)
def start_game():
    global started, game_on, game_won, balloon_list, time
    global landmine_list, scroll_speed, level
    global background_time
    started = True
    game_on = True
    game_won = False
    player.destroyed = False
    balloon_list = []
    landmine_list = []
    bullet_list = []
    player.time = 0
    background_time = 0.0
    time = 0.0
    level = 1
    player.health = 100
    scroll_speed = 2.5
    player.pos = [WIDTH_FRAME / 2,HEIGHT_FRAME / 5]
    label_pause.set_text("To pause, press 'p'")
    
def pause_game():
    global game_on, started, scroll_speed
    if started:
        if game_on:
            game_on = False
            label_pause.set_text("To resume, press 'P'")
        else:
            game_on = True
            label_pause.set_text("To pause, press 'P'")

# Handler to let the user set the THROTTLE of the 
# helicopter
def throttle_handler(text_input):
    global THROTTLE, scroll_speed
    if text_input.isdigit():
        val = int(text_input)
        # There is a limit to how high the user can set it to
        if val <= scroll_speed * 10 + 25 and val >= scroll_speed * 10:
            THROTTLE = val / 10.0
        elif val > scroll_speed * 10 + 25:
            THROTTLE = scroll_speed + 2.5
        else:
            THROTTLE = scroll_speed
    
def game_over():
    global started, game_on, balloon_list, scroll_speed
    started = False
    game_on = False
    player.destroyed = True
    player.time = 0
    scroll_speed = 0

# Stop the game when the level is complete    
def level_completed(canvas):
    global game_on, scroll_speed, cached_scspeed
    # Store the scroll_speed for after the game has 
    # started
    if scroll_speed != 0:
        cached_scspeed = scroll_speed
    scroll_speed = 0
    if player.pos[0] > 1100:
        game_on = False
        canvas.draw_image(COMPL_IMAGE, 
                          (320 / 2, 180 / 2), (320, 180), 
                          (WIDTH_FRAME / 2, HEIGHT_FRAME / 2), 
                          (WIDTH_FRAME, HEIGHT_FRAME))
        button_nextlvl.draw(canvas)
    
    # Remove the landmines and balloon that are spawned
    # but still are not on the frame in order to avoid
    # the player hitting them after the level is 
    # complete
    for lm in landmine_list:
        if lm.pos[0] > 950:
            landmine_list.remove(lm)
    for bal in balloon_list:
        if bal.pos[0] > 950:
            balloon_list.remove(bal)

# Set the values for the next level and resume movement
def next_level():
    global scroll_speed, game_on, game_won, balloon_list 
    global bullet_list, time, level, landmine_list
    scroll_speed = cached_scspeed + 0.5
    game_on = True
    game_won = False
    level += 1
    balloon_list = []
    landmine_list = []
    bullet_list = []
    time = 0
    player.health = 100
    player.pos = [WIDTH_FRAME / 2, HEIGHT_FRAME / 5]
    
# Mouse click handler
def mouse_handler(position):
    global time, started
    if started == False:
        if button_start.is_clicked(position):
            start_game()
    if game_won:
        if button_nextlvl.is_clicked(position):
            next_level()

# Handler for when keyboard key is pressed    
def key_down(key):
    global forward, backward, BULLET_IMAGE
    if key == simplegui.KEY_MAP["right"] or key == simplegui.KEY_MAP["d"]:
        player.vel[0] = THROTTLE
        forward = True
        backward = False
              
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["a"]:
        player.vel[0] = -THROTTLE
        backward = True
        forward = False
               
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["w"]:
        player.vel[1] = -THROTTLE * 2.5

    if key == simplegui.KEY_MAP["down"] or key == simplegui.KEY_MAP["s"]:
        player.vel[1] = THROTTLE * 2.5
        
    if key == simplegui.KEY_MAP["p"]:
        pause_game()
                          
    if key == simplegui.KEY_MAP["space"]:
        # Spawn and limit the bullets according to level
        if game_on:
            bullet_list.append(Bullet(BULLET_IMAGE, 
                                      [player.pos[0] + 50, 
                                       player.pos[1] + 30]))
            if level < 6:
                if len(bullet_list) > (7-level):
                    bullet_list.pop(0)
            elif len(bullet_list) > 2:
                bullet_list.pop(0)

# Handler for when keyboard key is released        
def key_up(key):
    global forward, backward
    if key == simplegui.KEY_MAP["right"] or key == simplegui.KEY_MAP["d"]:
        player.vel[0] = 0
        forward = False
        backward = False
        
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["a"]:
        player.vel[0] = 0
        backward = False
        forward = False
        
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["w"]:
        player.vel[1] = 0
        
    if key == simplegui.KEY_MAP["down"] or key == simplegui.KEY_MAP["s"]:
        player.vel[1] = 0
        
# Create a frame, timer and game objects
frame = simplegui.create_frame('Game', WIDTH_FRAME, 
                               HEIGHT_FRAME, 171)

player = Player()                
for lava in range(32):
    lava_list.append(Lava(LAVA_IMAGE, [lava * 32, 560], lava))
button_start = Button((WIDTH_FRAME / 2, 310), 
                      "Start Game")
button_nextlvl = Button((WIDTH_FRAME / 2, HEIGHT_FRAME / 2), 
                        "Next Level")

fps = Fps()

# Handler to draw on canvas
def draw_handler(canvas):
    global game_won, button_start, scroll_speed, level
    global time, balloon_list, BALLOON_IMAGE 
    global WIDTH_FRAME, HEIGHT_FRAME, game_on, lava_list 
    global player, started, THROTTLE, landmine_list
    
    score = int(time / (40 + 10 * level))
    
    draw_background(canvas)
    player.draw(canvas) 
    
    # tilts the player
    if forward:
        if player.rot <= math.radians(10):
            player.rot += math.radians(0.5)
    else:
        if player.rot >= 0:
            player.rot -= math.radians(0.5)
    if backward:
        if player.rot >= math.radians(-10):
            player.rot -= math.radians(0.5)
    else:
        if player.rot <= 0:
            player.rot += math.radians(0.5)
    
    if game_on:
        player.update()

        # keeps the timer going and health
        # regenerating as long as the game is on
        if game_won == False:
            time += 1 
            if player.health < 100:
                player.health += 0.01
            
            # Spawn balloons and landmines
            if level < 8 and time % random.randint(30 - level * 4, 
                                                   70 - level * 5) == 1:
                balloon_list.append(Balloon())
                
            elif level > 7 and time % random.randint(5, 35) == 1:
                balloon_list.append(Balloon())
                
            if len(balloon_list) > 15:
                balloon_list.pop(0)
    
            if time > 60 and scroll_speed > 0 and time % int(500 / (scroll_speed)) == 0:
                landmine_list.append(Landmine())
    
    for bul in bullet_list:
        bul.draw(canvas)
        if player.destroyed or game_on:
            bul.update()
    
    # Draw, update and check for collisions with the 
    # balloons
    for bal in balloon_list:
        bal.draw(canvas)
        if game_on:
            if player.has_collided(bal):
                player.health -= 0.5
            for bul in bullet_list:
                # Reason to check for balloon in balloon _list:
                # About 1 in 50 times the game was run, an
                # error came that said 
                # ValueError: list.index(x): x not in list
                # even though it is going through the 
                # balloons IN the list
                if bul.has_collided(bal) and bal in balloon_list:
                    balloon_list.remove(bal)
                    bullet_list.remove(bul)
        if player.destroyed or game_on:
            bal.update()
    
    # Draw, update and check for collisions with 
    # landmines
    for lm in landmine_list:
        lm.draw(canvas)
        if player.has_collided(lm):
            player.health = 0
            lm.destroyed = True
        elif game_on:
            lm.update()
            for bul in bullet_list:
                if bul.has_collided(lm):
                    bullet_list.remove(bul)
    
    # Draw laser
    canvas.draw_image(LASER_IMAGE, 
                      (LASER_WIDTH / 2, LASER_HEIGHT / 2), 
                      (LASER_WIDTH, LASER_HEIGHT), 
                      (48, HEIGHT_FRAME / 2), 
                      (LASER_WIDTH / 1.177, 
                       LASER_HEIGHT / 1.177))
    
    # Draw health bar
    canvas.draw_polygon(((791,37), 
                         (791 + player.health * 2,37), 
                         (791 + player.health * 2,68), 
                         (791, 68)), 
                        0.01, "white", "red")     
    canvas.draw_polygon(((789, 35), (993, 35), 
                         (993, 70), (789, 70)), 
                        4, "white")
    
    for lava in lava_list:
        lava.draw(canvas)
        if game_on:
            lava.update()
    
    # Draw frames per second        
    fps.draw(canvas)
     
    # Draw throttle and level    
    canvas.draw_text("Throttle: " + str(int(THROTTLE * 10))[0:4], 
                     (200, 30), 30, "black")
    canvas.draw_text("Level: " + str(level), (680, 30), 
                     30, "black")
    
    if score >= 100:
        game_won = True
        level_completed(canvas)
    
    # Draw start screen after game ends
    if (started == False and player.destroyed == False) or (player.destroyed and player.time > 50):
        canvas.draw_image(START_SCREEN_IMAGE, 
                          (WIDTH_FRAME / 2, HEIGHT_FRAME / 2), 
                          (WIDTH_FRAME, HEIGHT_FRAME), 
                          (WIDTH_FRAME / 2, HEIGHT_FRAME / 2), 
                          (WIDTH_FRAME, HEIGHT_FRAME))
        button_start.draw(canvas)
    
    # Draw score
    canvas.draw_image(SCORE_BACK_IMAGE, 
                      (WIDTH_FRAME / 2, HEIGHT_FRAME / 2), 
                      (WIDTH_FRAME, HEIGHT_FRAME), 
                      (WIDTH_FRAME / 2, HEIGHT_FRAME / 2), 
                      (WIDTH_FRAME, HEIGHT_FRAME))
    
    canvas.draw_text(str(score), (512 - 12.5 * len(str(score)), 50), 
                     50, "white")    

# Create buttons & text inputs
label_pause = frame.add_label("To pause, press 'p'", 150)
frame.add_label("\n", 150)
frame.add_label("\n", 150)
control_throttle = frame.add_input("Set Throttle", 
                                   throttle_handler, 150)
frame.add_label("\n", 150)
frame.add_label("\n", 150)
frame.add_label("When you reach 100 points, keep going towards the right side", 
                150)

# Assign callbacks to handler functions
frame.set_draw_handler(draw_handler)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(mouse_handler)

# Start the frame and timer for fps
fps.TIMER.start()
frame.start()