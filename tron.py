# game module that hold the game being played
import pygame, sys, time
from pygame.locals import *
from networking import NetworkGame, Server
from helper import load_images
from pprint import pprint
FPS = pygame.time.Clock() 
WIN_PAUSE = 3
SCORE_SIZE = 16
INFO_SIZE = 5

class LightBike():
  def __init__(self, startloc, startvel):
    self.location = startloc
    self.velocity = startvel
    self.color = color
  def movedown(self):
    self.velocity[0] = 0
    self.velocity[1] = 1
  def moveup(self): 
    self.velocity[0] = 0 
    self.velocity[1] = -1
  def moveleft(self):
    self.velocity[0] = -1
    self.velocity[1] = 0  
  def moveright(self):
    self.velocity[0] = 1 
    self.velocity[1] = 0
  def update(self):
    self.location[0][0] += self.velocity[0]
    self.location[0][1] += self.velocity[1]

class Game(NetworkGame):
  """holds the Game class"""
  def __init__(self, location, scale, mode):
    """Initialize all the varibles"""
    super(Game, self).__init__(location, mode)
    self.GRID_SIZEX = 32 # 
    self.GRID_SIZEY = 20
    self.bezelx = 33
    self.bezely = 21
    self.loc = []
    for x in range(0,self.bezelx ):
      self.loc.append([])
      for y in range(0,self.bezely ):
        self.loc[x].append(0) # 0 means not moved there yet
    self.SCALE = scale
    self.WIDTH = self.GRID_SIZEX * self.SCALE # scale the pixels from gridspace
    self.HEIGHT = self.GRID_SIZEY * self.SCALE
    SIZE = (self.WIDTH, self.HEIGHT) 
    self.player1 = LightBike([0,0],  [1,0])
    self.player2 = LightBike([1,1], [-1,0])
    self.score = {'p1':0, 'p2':0}
    pygame.init()
    self.window = pygame.display.set_mode(SIZE, mode, 0)
    pygame.mouse.set_visible(False)
    self.image_dict = load_images()
    image_path = 'assets/backgrounds/' + str(self.tile[0]) + '-' + str(self.tile[1]) + '.jpg'
    self.background = pygame.image.load(image_path)
    self.background = pygame.transform.scale(self.background, SIZE)
    self.background = self.background.convert()
    self.backPos = pygame.Rect((0, 0), (0, 0))
    self.window.blit(self.background, self.backPos)
    self.p1_death_loc = [0,0]
    self.p2_death_loc = [0,0]
    self.p1_died = False
    self.p2_died = False

  def update(self, data):
    # print "in update"
    # pprint(data)
    if data['state'] == 'play':
      return self.play_state(data)
    elif data['state'] == 'win':
      #print self.player1.location
      #print self.player2.location
      return self.win_state(data)
    elif data['state'] == 'over':
      return self.game_over(data)


  def play_state(self, data):
    head_pos_1 = self.translate_position(data['player1_locs'][0])
    head_pos_2 = self.translate_position(data['player2_locs'][0])
    player1hit = False
    player2hit = False

    if self.info_tile:
      self.time = data['time']

    if head_pos_1 == head_pos_2 and head_pos_1 != 0:
      self.player2.location = head_pos_2
      self.player1.location = head_pos_1
      self.p1_death_loc = self.player1.location[:]
      self.p2_death_loc = self.player2.location[:]
      self.p1_died = True
      self.p2_died = True
      #print "DRAW!"
      data_struct = {'state': 'draw', 'which':'draw', 
                     'death_loc': [self.p1_death_loc, self.p2_death_loc],
                     'tile': self.tile}  
      return data_struct

    if head_pos_1 != 0:
      # print head_pos_1
      self.player1.location = head_pos_1
      if self.loc_collision(self.loc, self.player1):
      # will have to send to master node that there is a winner!
        player1hit = True
        self.p1_death_loc = self.player1.location[:]
        self.p1_died = True
        # print 'PLAYER 2 WINS'
        # data_struct = {'state': 'win', 'which':2}  
        # return data_struct
      else:
        self.loc[self.player1.location[0]][self.player1.location[1]] = 1
        self.draw(self.player1.location, self.image_dict[data['player1_images'][0]])

    if head_pos_2 != 0:
      self.player2.location = head_pos_2
      # print head_pos_2
      if self.loc_collision(self.loc, self.player2):
      # will have to send to master node that there is a winner!
        player2hit = True
        self.p2_death_loc = self.player2.location[:]
        self.p2_died = True
        # print 'PLAYER 2 WINS'
        # data_struct = {'state': 'win', 'which':1}  
        # sys.exit()  
        # return data_struct
      else:
        self.loc[self.player2.location[0]][self.player2.location[1]] = 1
        self.draw(self.player2.location, self.image_dict[data['player2_images'][0]])

    # check for draw on same screen
    if player1hit and player2hit:
      
    #if (head_pos_1 != 0 and head_pos_1 == head_pos_2) or (player2hit and player1hit) :
      #print "DRAW"
      data_struct = {'state': 'draw', 'which':'draw', 
                     'death_loc': [self.p1_death_loc, self.p2_death_loc],
                     'tile': self.tile}  
      return data_struct
    if player1hit:
      data_struct = {'state': 'win', 'which':2, 'death_loc': [self.p1_death_loc],
                     'tile': self.tile}  
      return data_struct
    if player2hit:
      data_struct = {'state': 'win', 'which':1, 'death_loc': [self.p2_death_loc],
                     'tile': self.tile} 
      return data_struct 

    for idx in range(1, len(data['player1_locs'])):
      # print "coords is "+str(data['player1_locs'][idx])
      # print "idx is " + str(idx)
      temp = self.translate_position(data['player1_locs'][idx])
      if temp != 0 and data['player1_images'][idx] != 'corner':
        self.draw(temp, self.image_dict[data['player1_images'][idx]])  

    for idx in range(1, len(data['player2_locs'])):
      temp = self.translate_position(data['player2_locs'][idx])
      if temp != 0 and data['player2_images'][idx] != 'corner':
        self.draw(temp, self.image_dict[data['player2_images'][idx]]) 

    ##if self.info_tile:
      #self.drawTime(self.time)

    pygame.display.flip()
    #if self.info_tile:
    #  self.saved = self.window.copy()
    #  self.drawTime(self.time)
    #  pygame.display.flip()
    data_struct = {'state': 'play'}
    return(data_struct)

  def win_state(self, data):
    # self.window.fill((0,0,0))
    trans_death = []
    for death in data['death_loc']:
      # print "BEFORE TRANS" + str(death)
      trans_death.append([death[0] - self.tile[0]*(self.bezelx),
                          death[1] - (self.tile[1])*(self.bezely)])
      # print "after" + str(trans_death[-1])
    for idx in range(0,5):
      for death in trans_death:
        im_rect = self.image_dict['explode' + str(idx)].get_rect()
        im_rect.centerx = death[0]*self.SCALE
        im_rect.centery = death[1]*self.SCALE

        self.window.blit(self.image_dict['explode' + str(idx)],im_rect)
        pygame.display.flip()
      time.sleep(.1)


    if hasattr(self, 'saved'):
      del self.saved
    self.window.blit(self.background, self.backPos)
    if self.score_tile:
      font = pygame.font.Font(None, SCORE_SIZE * self.SCALE)
      score = str(data['score'][self.player_score])
      if self.player_score == 'p1':
        color = 0, 0, 255
      else:
        color = 255, 0, 0
      text = font.render(score, 1, color)
      textpos = text.get_rect()
      textpos.centerx = self.window.get_width()/2
      textpos.centery = self.window.get_height()/2
      self.window.blit(text, textpos)
    if self.info_tile:
      font = pygame.font.Font(None, INFO_SIZE * self.SCALE)
      msg = str(data['msg'])
      if msg == 'Player 1 Scored':
        color = (0, 0, 255)
      elif msg == 'Player 2 Scored':
        color = (255, 0, 0)
      else:
        color = (255, 255, 255)
      msg = font.render(msg, 1, color)
      msgpos = msg.get_rect()
      msgpos.centerx = self.window.get_width()/2 
      msgpos.centery = self.window.get_height()/2 + (INFO_SIZE * self.SCALE)
      self.window.blit(msg, msgpos)
      self.drawTime(str(data['time']))
    pygame.display.flip()

    self.loc = []
    for x in range( 0,self.bezelx ):
      self.loc.append([])
      for y in range( 0,self.bezely ):
        self.loc[x].append(0) # 0 means not moved there yet
    #display score for a bit
    time.sleep(WIN_PAUSE)
    
    # self.window.fill((0,0,0))
    self.window.blit(self.background, self.backPos)
    
    pygame.display.flip()

    return  {'state': 'play'}  

  def drawTime(self, el_time):
    font = pygame.font.Font(None, INFO_SIZE * self.SCALE)
    el_time = font.render(str(el_time), 1, (255, 255, 255))
    el_timepos = el_time.get_rect()
    el_timepos.centerx = self.window.get_width()/2 
    el_timepos.centery = self.window.get_height()/2 - (INFO_SIZE * self.SCALE)
    self.window.blit(el_time, el_timepos)
      

  def game_over(self, data):
    # self.window.fill((0,0,0))
    self.window.blit(self.background, self.backPos)
    if self.score_tile:
      font = pygame.font.Font(None, SCORE_SIZE * self.SCALE)
      score = str(data['score'][self.player_score])
      if self.player_score == 'p1':
        color = 0, 0, 255
      else:
        color = 255, 0, 0
      text = font.render(score, 1, color)
      textpos = text.get_rect()
      textpos.centerx = self.window.get_width()/2
      textpos.centery = self.window.get_height()/2 
      self.window.blit(text, textpos)
    pygame.display.flip()

    self.loc = []
    for x in range(0,self.bezelx ):
      self.loc.append([]) 
      for y in range(0,self.bezely ):
        self.loc[x].append(0) # 0 means not moved there yet
    #display score for a bit
    # time.sleep(WIN_PAUSE)
    # self.window.fill((0,0,0))
    pygame.display.flip()
    return  {'state': 'over'}
  
  def clear(self):
    """clears any graphics on screen"""
    # self.window.fill((0,0,0))
    self.window.blit(self.background, self.backPos)
    pygame.display.flip()

  def loc_collision(self, loc, bike):
    if loc[bike.location[0]][bike.location[1]] == 1:
      return True
    else:
      return False

  def draw_scrap(self, location, image):
    if not self.info_tile:# or self.time == -1:
      self.originalDraw(location, image)
    else:
      self.newDraw(location, image)

  def newDraw(self, location, image):
    if hasattr(self, 'saved'):
      self.window.blit(self.saved, self.backPos)
    self.originalDraw(location, image)
    self.saved = self.window.copy()


  def draw(self, location, image):
    """draws the image at the location, properly scaled from the grid space,
    draws a black square first where it will be drawn"""
    x_cor = location[0]*self.SCALE
    y_cor = location[1]*self.SCALE
    if not (x_cor > 1920 or y_cor > 1200):
      self.window.blit(self.background, (x_cor, y_cor),
        pygame.Rect(x_cor, y_cor, self.SCALE, self.SCALE))
      # pygame.draw.rect(self.window, (0,0,0), 
      #                     (location[0]*self.SCALE, 
      #                     location[1]*self.SCALE, 
      #                     self.SCALE, self.SCALE))
      self.window.blit(image, (location[0]*self.SCALE, location[1]*self.SCALE))

  def translate_position(self, pos):
    """tanslates the entire game board to the local one"""

    if (pos[0] < (self.tile[0]+1)*(self.bezelx) and 
        pos[0] >= self.tile[0]*(self.bezelx) and 
        pos[1] < (self.tile[1]+1)*(self.bezely) and 
        pos[1] >= self.tile[1]*(self.bezely)):
        translated_pos = [pos[0] - self.tile[0]*(self.bezelx),
                          pos[1] - (self.tile[1])*(self.bezely)] 
        # print "player 1 trans at " + str(translated_pos_1)
    else: translated_pos = 0
    return translated_pos #, translated_pos_2)

