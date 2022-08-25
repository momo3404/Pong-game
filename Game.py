# This program simulates a pong game between two players 

# importing libraries
import pygame

# User-defined functions
# main function that runs game
def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Pong')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes
# Game class that runs game
class Game:
   # initializing game elements
   def __init__(self, surface):
      self.surface = surface
      self.bg_color = pygame.Color('black')
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
      # Ball object
      self.small_dot = Ball('white', 6, [50, 50], [3,4], self.surface)
      # Creating two paddles
      self.pad_one = Paddle('white', 80, 170, 4,50, [0,7], self.surface)
      self.pad_two = Paddle('white', 406, 170, 4,50, [0,7], self.surface)
      self.max_frames = 150
      self.frame_counter = 0  
      # two instance attributes that will be used to move paddles
      self.pad_one_move = 0
      self.pad_two_move = 0
     
   
              
   # function that plays the game until the player presses the close box
   # - self is the Game that should be continued or not 
   def play(self):
      # while top right x has not been clicked
      while not self.close_clicked:
         self.handle_events()
         self.draw()  
         # if game is still going
         if self.continue_game:
            self.update()
            self.decide_continue()
         # run at most with FPS Frames Per Second 
         self.game_Clock.tick(self.FPS) 
         
   # function that handles user input
   # self is the Game that is changed
   def handle_events(self):
      events = pygame.event.get()
      for event in events:
         # if x is clicked
         if event.type == pygame.QUIT:
            self.close_clicked = True
         
         # if a key is pressed
         if event.type == pygame.KEYDOWN:
            # for player and paddle 1
            if event.key == pygame.K_q:
               self.pad_one_move = 'up_1'
            elif event.key == pygame.K_a:
               self.pad_one_move = 'down_1'
            # for player and paddle 2
            elif event.key == pygame.K_p:
               self.pad_two_move = 'up_2'
            elif event.key == pygame.K_l:
               self.pad_two_move = 'down_2'
         
         # if key lifted then stop movement of paddle
         if event.type == pygame.KEYUP:
            # for player and paddle 1
            if event.key == pygame.K_q:
               self.pad_one_move = 0
            elif event.key == pygame.K_a:
               self.pad_one_move = 0
            # for player and paddle 2
            elif event.key == pygame.K_p:
               self.pad_two_move = 0
            elif event.key == pygame.K_l:
               self.pad_two_move = 0
            
   # function that returns pad_one_move
   # self is Game 
   def get_pad_one_move(self):
      return self.pad_one_move
   
   # function that returns pad_two_move
   # self is Game    
   def get_pad_two_move(self):
      return self.pad_two_move   
      
   # function that draws all game objects
   # - self is the Game to draw         
   def draw(self):
      # clear the display surface first
      self.surface.fill(self.bg_color) 
      # draw small dot and paddles
      self.small_dot.draw()
      self.pad_one.draw()
      self.pad_two.draw()
      # draw score
      self.small_dot.draw_score()
      # make the updated surface appear on the display
      pygame.display.update() 


   # function that updates the game objects for the next frame
   # - self is the Game to update
   def update(self):
      # move ball and change score based on where ball goes
      self.small_dot.move()
      self.small_dot.score()
      # move paddles in accordance with user input
      #print(self.small_dot.velocity[0])
      self.pad_one.move_one(self, self.pad_one)
      self.pad_two.move_two(self, self.pad_two)
      # keep paddles in window
      self.pad_one.keep()
      self.pad_two.keep()
      # check for collisions between ball and paddle
      self.pad_one.collide(self.small_dot, self.pad_one, self.pad_two)
      self.pad_two.collide(self.small_dot, self.pad_one, self.pad_two)
      self.frame_counter = self.frame_counter + 1
      
   # Check and remember if the game should continue
   # - self is the Game to check
   def decide_continue(self):
      if self.frame_counter > self.max_frames:
         self.continue_game = True
         
      if self.small_dot.decide_game_continue():
         self.continue_game = False
      

# Ball class that creates game ball
class Ball:
   def __init__(self, dot_color, dot_radius, dot_center, dot_velocity, surface):
      self.color = pygame.Color(dot_color)
      self.radius = dot_radius
      self.center = dot_center
      self.velocity = dot_velocity
      self.surface = surface 
      self.position = 0
      self.pad_two_score = 0
      self.pad_one_score = 0
      
   
   # function that moves ball
   # self is Ball moving
   def move(self):
      # get size of window surface
      size = self.surface.get_size()
      for i in range(0,2):
         # move center of the ball in accordance with the velocity
         self.center[i] = (self.center[i] + self.velocity[i])
         if self.center[i] < self.radius :
            # make sure ball does not go through left or the top edge 
            self.velocity[i] = -self.velocity[i]
         if self.center[i] + self.radius > size[i]: 
            # make sure ball does not go through right or bottom edge
            self.velocity[i] = - self.velocity[i]    
    
   # function that keeps track of each player's score throughout game
   # self is Ball moving
   def score(self):
      size = self.surface.get_size()
      # if ball hits right edge 
      if self.center[0] + self.radius > size[0]:
         self.pad_one_score = self.pad_one_score + 1

      # if ball hits left edge 
      if self.center[0] < self.radius:
         self.pad_two_score = self.pad_two_score + 1
         
   def decide_game_continue(self):
      # game over when any player's score hits 11 
      return self.pad_one_score == 11 or self.pad_two_score == 11
         
         
   # function that draws score for each player  
   # self is Ball 
   def draw_score(self):
      size = self.surface.get_size()
      score1_string = str(self.pad_one_score)
      # step 1 create a font object
      font_size = 80
      fg_color = pygame.Color('white')
      font = pygame.font.SysFont('',font_size)
      # step 2 render the font
      text_box = font.render(score1_string, True,fg_color, 'black')
      # step 3  compute the location 
      location = (0,0)   
      self.surface.blit(text_box,location)
      
      score2_string = str(self.pad_two_score)
      # step 1 create a font object
      font_size = 80
      fg_color = pygame.Color('white')
      font = pygame.font.SysFont('',font_size)
      # step 2 render the font
      text_box = font.render(score2_string, True,fg_color, 'black')
      # step 3  compute the location
      # code for drawing score in the top right corner of the window
      y = 0
      a = size[0]
      b = text_box.get_width()
      x = a -b
      location = (x,y)    
      self.surface.blit(text_box,location) 
      
   # function that returns velocity in x direction for use in other classes
   # self is Ball object
   def get_velocity(self):
      return self.velocity[0]
   
   # function that reverses velocity in the x direction
   # self if Ball object
   def reverse_velocity(self):
      self.velocity[0] =  - self.velocity[0]
    
   # function that returns center of the ball
   # self is Ball object
   def get_center(self):
      return self.center
      
   # function that draws ball as a circle
   # self is Ball
   def draw(self):
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)


# class that creates Paddle
class Paddle:
   def __init__(self, pad_color, pad_x, pad_y, pad_width, pad_height, pad_velocity, surface):
      self.rect = pygame.Rect(pad_x,pad_y, pad_width, pad_height)
      self.color = pygame.Color(pad_color)
      self.width = pad_width
      self.height = pad_height
      self.velocity = pad_velocity
      self.x = pad_x
      self.rect.top = pad_y
      self.surface = surface
      self.movement = 0

   
   # function that moves paddle one
   # self is Paddle, game is Game object that contains get_pad_one_move function, pad_one is paddle one
   def move_one(self, game, pad_one):
      # move paddle across y axis in accordance with user input
      if game.get_pad_one_move() == 'up_1':
         pad_one.rect.top =  pad_one.rect.top - pad_one.velocity[1]
      elif game.get_pad_one_move() == 'down_1':
         pad_one.rect.top =  pad_one.rect.top + pad_one.velocity[1]
   
   # function that moves paddle two
   # self is Paddle, game is Game that contains get_pad_two_move function, pad_two is paddle two
   def move_two(self, game, pad_two):
      if game.get_pad_two_move() == 'up_2':
         pad_two.rect.top =  pad_two.rect.top - pad_two.velocity[1]
      elif game.get_pad_two_move() == 'down_2':
         pad_two.rect.top =  pad_two.rect.top + pad_two.velocity[1]
         
   
    
   # function that keeps paddle inside window 
   # self is Paddle
   def keep(self):
      # if top left point of paddle reaches top edge 
      if self.rect.top < 0:
         self.rect.top =  self.rect.top + self.velocity[1]
      # if top left point of paddle reaches top edge
      elif self.rect.top > 350 :
         self.rect.top =  self.rect.top - self.velocity[1]

         
   # function that checks if paddle has collided with ball
   # self is Paddle, other is Ball, pad_one is left paddle, pad_two is right paddle
   def collide(self, other, pad_one, pad_two):
      # checks for collision only if ball is coming at paddle from an oncoming direction
      if abs(other.get_velocity()) != other.get_velocity():
         if pad_one.rect.collidepoint((other.get_center()[0], other.get_center()[1])):
            # changing velocity in the x direction when collision occurs
            other.reverse_velocity()
      if abs(other.get_velocity()) == other.get_velocity():
         if pad_two.rect.collidepoint((other.get_center()[0], other.get_center()[1])):
            # changing velocity in the x direction when collision occurs
            other.reverse_velocity()
              
   # function that draws paddle as a rectangle
   # parameter is Paddle
   def draw(self):
      pygame.draw.rect(self.surface, self.color, [self.x,  self.rect.top, self.width, self.height])

# calling main function to run game
main()
