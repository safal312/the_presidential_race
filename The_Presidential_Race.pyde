
# adding necessary libraries
add_library('minim')
import os, random

path = os.getcwd()

music = Minim(this)

# This string is responsible for the various states our game will be in
# They are: player select, difficulty select, playing game, game over
state = "MAIN"
diff = "EASY"
player = None

# Basic global variables
HEIGHT = 600
WIDTH = 800
player = None
start_time = 0
timer = None

# maing game class
class Game:
    def __init__(self):
        self.state = state
        self.diff = diff
        self.player = player
        self.score = 0
        self.opp_score = 0
        self.votes = []
        self.speed = 0
        self.drop_rate = 30
        self.sprite_count = 0
        self.frames = 0
        self.bg_music = music.loadFile(path + "/sounds/music.mp3")
        self.bg_music.loop()
        
    
    def display(self):
        global score, opp_score, timer
        
        textAlign(CENTER, CENTER)
        textSize(20)
        
        
        # checking for game over right at the start
        if self.opp_score >= 270 or self.score >= 270:
            global state
            state = "OVER"
        
        # displaying different screens on the basis of the state
        if state == "MAIN":
            #main screen
            display = loadImage(path + "/images/" + "main.jpg")
            image(display,0,0, WIDTH, HEIGHT)
            
        
        if state == "INSTRUCTIONS":
            #instruction screen
            backdrop = loadImage(path + "/images/" + "instructions.jpg")
            image(backdrop,0,0, WIDTH, HEIGHT)
          
            
        if state == "PLAYER":
            # display on player select screen
            display = loadImage(path + "/images/" + "players.jpg")
            image(display,0,0, WIDTH, HEIGHT)


        elif state == "DIFF":
            #display on difficulty choosing screen
            back = loadImage(path + "/images/" + "diff.jpg")
            image(back,0,0,WIDTH, HEIGHT)


        elif state == "OVER":
            
            # display on game over
            textSize(48)
            
            if player.name == "TRUMP":
                if self.score > self.opp_score:
                    
                    self.trump_anim()
                    text("YOU WON", WIDTH/2, 100)
                elif self.score == self.opp_score:
                    text("IT'S A TIE\nPlay Again if you want a recount", WIDTH/2, 100)
                else:
                    
                    self.biden_anim()
                    text("YOU LOST", WIDTH/2, 100)
            elif player.name == "BIDEN":
                if self.score > self.opp_score:
                    
                    self.biden_anim()
                    text("YOU WON", WIDTH/2, 100)
                elif self.score == self.opp_score:
                    text("IT'S A TIE\nPlay Again if you want a recount", WIDTH/2, 100)
                else:
                    
                    self.trump_anim()
                    text("YOU LOST", WIDTH/2, 100)    
            
            
            textAlign(CENTER, CENTER)
        
            text("GAME OVER", WIDTH/2, 50)
            
            
            
            textSize(18)
            text("Time Elasped", WIDTH/2, 170)
            text(timer,WIDTH/2, 200)
            
            
            textAlign(LEFT, LEFT)
            text("Your Score:",WIDTH/2 - 100,250)
            text(self.score,WIDTH/2 + 70, 250)
            text("Opponent Score:",WIDTH/2 - 100, 280)
            text(self.opp_score,WIDTH/2 + 70, 280)
            

            textAlign(CENTER, BOTTOM)
            textSize(12)
            text("Please click on the screen\n to restart the game", WIDTH - 100, HEIGHT - 50)
        
        
        # main block that handles gameplay
        elif state == "PLAY":
            background(60, 59, 110)
            global start_time
            
            # I'm doing this becaue millis() starts when the program starts
            # our timer should start when the game starts
            # So I'm recording at how many seconds the game starts in the first iteration
            
            if start_time == 0:
                start_time = millis()
                
            time = (millis() - start_time) / 1000
            
            mins = 0
            seconds = 0
            
            if time < 60:
                seconds = time
            else:
                mins = time // 60
                seconds = time % 60
            
            timer = str(mins)+ " : " + str(seconds)
            
            fill(255,255,255)
            text("T I M E", WIDTH - 60, 20)
            text(timer, WIDTH - 60, 50)
            text("S C O R E", WIDTH - 60, 80)
            text(self.score, WIDTH - 60, 110)
            text("O P P O N E N T", WIDTH - 80, 140)
            text("S C O R E", WIDTH - 60, 160)
            text(self.opp_score, WIDTH - 60, 190)
            
                
            # our main game display here
            player.display()
            
            # diferent drop rate of ballots on basis of difficulty
            if diff == "EASY":
                self.drop_rate = 30
            elif diff == "MEDIUM":
                self.drop_rate = 20
            elif diff == "HARD":
                self.drop_rate = 10
            
            
            # every 100 frames we drop
            if frameCount % self.drop_rate == 0:    # changed from 100 to 50
                self.drop_object()
            
            # iterating over each vote to display, check collision, etc.
            for vote in self.votes:
                vote.display()
                
                # if a ballot passes the bottom, we remove it from the list and add to the opponent score
                if vote.y > HEIGHT:
                    self.opp_score += vote.worth
                    self.votes.remove(vote)
                    
                if vote.collides() == True:
                    self.score += vote.worth
                    self.votes.remove(vote)
                
                vote.update()
            
     # method to handle trump animation       
    def trump_anim(self):
        background(255)
        fill(0)
        # there are 25 images in the folder trump_win
        self.frames = 25
        frame = loadImage(path + "/images/trump_win/" + player.trump_sprite[self.sprite_count])
        image(frame, (WIDTH / 2) - 150, (HEIGHT / 2), 300, 300)
        
        # slowing down the animation by half
        if frameCount % 2 == 0:
            self.sprite_count = (self.sprite_count + 1) % self.frames
    
    # method to handle biden animation    
    def biden_anim(self):
        background(60, 59, 110)
        fill(255)
        # there are 56 images in the biden_win folder
        self.frames = 56
        frame = loadImage(path + "/images/biden_win/" + player.biden_sprite[self.sprite_count])
        image(frame, (WIDTH / 2) - 150, (HEIGHT / 2), 300, 300)
        
        if frameCount % 2 == 0:
            self.sprite_count = (self.sprite_count + 1) % self.frames
      
                  
    # we choose a randome x value and create an object with it
    def drop_object(self):
        x_pos = random.randint(0, WIDTH - 40)    # random x value
        type = random.randint(1, 50)
        ability = None
        
        # randomly choosing the ability
        if type < 5:
            ability = "FAST"
        
        if type > 45:
            ability = "BULK"
            
        if type > 10 and type <= 25:
            ability = "SLOW"
            
        # creating a new vote each time
        self.votes.append(Vote(x_pos, self.speed, ability))
        
        
#this is the character class
class Player:
    def __init__(self):
        self.w = 100
        self.h = 120
        self.g = 600
        self.x = WIDTH/2 - self.w/2    #x coordinate for image- start by positioning character in middle 
        self.y = HEIGHT - (HEIGHT - self.g) - self.h
        self.left = False
        self.right = False
        self.dir = RIGHT
        self.img = None
        self.speed = 5    
        self.fast_time = 0    # using this variable to reset the player's speed to normal
        self.slow_time = 0    # same with this
        self.name = None
        
        # loading all the trump image names in this array
        trump_images = []
        for frame in range(25):
            trump_images.append("frame_"+ str(frame) + "_delay-0.07s.gif")
        self.trump_sprite = trump_images
        
        # loading all the biden image names in this array
        biden_images = []
        for frame in range(56):
            biden_images.append("frame_"+ str(frame) + "_delay-0.04s.gif")
        self.biden_sprite = biden_images
        
    
    def display(self):
        
        # keeping track of the duration of the fast ability when speed is 10
        if self.speed == 10:
            self.fast_time += 1
            if self.fast_time == 100:
                self.fast_time = 0
                self.speed = 5  
        
        # keeping track of the duration of the slow ability when speed is 1
        if self.speed == 1:
            self.slow_time += 1
            if self.slow_time == 100:
                self.slow_time = 0
                self.speed = 5  
                
        self.update()
        
        # changing colors of the player on the basis of the special ballots
        if self.speed == 1:
            tint(214, 87, 77)
        elif self.speed == 10:
            tint(237, 211, 81)
        
        # flipping the image on the basis of direction
        if self.dir == RIGHT:
            image(self.img, self.x, self.y, self.w, self.h, 0, 0, self.w, self.h)
        elif self.dir == LEFT:
            image(self.img, self.x, self.y, self.w, self.h, self.w, 0, 0, self.h)
        noTint()
        
    def update(self):
        if self.left == True and self.x >= 0:
            self.dir = LEFT
            self.x -= self.speed
        if self.right == True and self.x <= WIDTH- self.w:
            self.dir = RIGHT
            self.x += self.speed
            
#this is child class for player 1 - trump
class Trump(Player):
    def __init__(self):
        Player.__init__(self)
        self.img = loadImage(path + "/images/" + "trump.png")
        self.img.resize(self.w, self.h)
        

#this is child class for player 2 - Biden
class Biden(Player):
    def __init__(self):
        Player.__init__(self)
        self.img = loadImage(path + "/images/" + "biden.png")
        self.img.resize(self.w, self.h)
        
        
#this is class for falling object
class Vote:
    def __init__(self, x, speed, ability):
        self.w = 40    # need the w and h to squeeze the image
        self.h = 50  
        
        self.y = -self.h   #y coordinate position
        self.x = x         #x coordinate position
        
        self.speed = speed
        self.ability = ability
        self.worth = 10
        
        # setting the worth and image of the object on the basis of their type
        if self.ability == "BULK":
            self.img = loadImage(path + "/images/" + "bulk.png")
            self.w = 55
            self.h = 65
            self.worth = 20
        elif self.ability == "FAST":
            self.img = loadImage(path + "/images/" +"fast.png")
            
        elif self.ability == "SLOW":
            self.worth = 0
            self.img = loadImage(path + "/images/" +"slow.png")
        else:
            self.img = loadImage(path + "/images/" +"vote.png")
        
        
    def display(self):
        
        #display the form falling
        image(self.img, self.x, self.y, self.w, self.h)
        
    def update(self):
        self.y += self.speed    #move down
  
    # we'll be returning true or false from here on
    def collides(self):
        if (player.x + player.w >= self.x and player.x <= self.x + self.w):
            if self.y + self.h >= player.y and self.y <= player.y + player.h:
                
                # checking if the ballot that we collide with has some special ability
                if self.ability == "FAST":
                    player.speed = 10
                elif self.ability == "SLOW":
                    player.speed = 1
                return True
        return False        
    

game = Game()

def setup():
    size(WIDTH, HEIGHT)
    
def draw():
    game.display()
    
def keyPressed():
    global player, diff, state
    
    # keeping track of the keys pressed on various screens
    if state == "PLAYER":
        
        if keyCode == 84:    # 84 = "t"
            player = Trump()
            player.name = "TRUMP"
            state = "DIFF"    # we change the state to move to a different screen
        elif keyCode == 66:    # 66 = "b"
            player = Biden()
            player.name = "BIDEN"
            state = "DIFF"
            
    elif state == "MAIN":
        
        if keyCode == 73:    # 73 = "i"
            state = "INSTRUCTIONS"
        elif keyCode == 71:    # 71 = "g"
            state = "PLAYER"
            
    elif state == "INSTRUCTIONS":
        
        if keyCode == 71:      # 71 = "g"
            state = "PLAYER"
        
    elif state == "DIFF":
        
        if keyCode == 69:    # 69 = "e"
            diff = "EASY"
            game.speed = 3
            state = "PLAY"
        elif keyCode == 77:    # 77 = "m"
            diff = "MEDIUM"
            game.speed = 6
            state = "PLAY"
        elif keyCode == 72:    # 72 = "h"
            diff = "HARD"
            game.speed = 10
            state = "PLAY"
            
    #start moving till key is pressed
    if state == "PLAY":
        if keyCode == RIGHT:
            player.right = True
        if keyCode == LEFT:
            player.left = True
            
            
#stop motion on keyRelease
def keyReleased():
    global state
    
    if state == "PLAY":
        if keyCode == RIGHT:
            player.right = False
        if keyCode == LEFT:
            player.left = False
            
# this is the part that will run to replay the game
def mouseClicked():
    global state, game, start_time
    
    if state == "OVER":
        state = "MAIN"
        start_time = 0
        game.bg_music.pause()
        noTint()
        game = Game()
            
