# game module that hold the game being played
import pygame, sys
from pygame.locals import *
from networking import NetworkGame, Server
FPS = pygame.time.Clock() 

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
  def __init__(self, location):
    super(Game, self).__init__(location)
    self.GRID_SIZEX = 10 # will probably need to be rectangular
    self.GRID_SIZEY = 10
    self.loc = []
    for x in range(0,self.GRID_SIZEX ):
      self.loc.append([])
      for y in range(0,self.GRID_SIZEY ):
        self.loc[x].append(0) # 0 means not moved there yet
    print self.tile
    self.SCALE = 60
    self.WIDTH = len(self.loc) * self.SCALE
    self.HEIGHT = len(self.loc[0]) * self.SCALE
    self.SIZE = (self.WIDTH, self.HEIGHT) # widt
    self.player1 = LightBike([0,0],  [1,0])
    self.player2 = LightBike([1,1], [-1,0])
    pygame.init()
    self.window = pygame.display.set_mode(self.SIZE)
    self.image_dict = self.load_images()

  def update(self, data):
    head_pos_1 = self.translate_position(data['player1_locs'][0])
    head_pos_2 = self.translate_position(data['player2_locs'][0])
    if head_pos_1 != 0:
      print head_pos_1
      self.player1.location = head_pos_1
      if self.loc_collision(self.loc, self.player1):
      # will have to send to master node that there is a winner!
        print 'PLAYER 2 WINS'
        data_struct = {'player_locations':
                    ([self.player1.location[0],self.player1.location[1]],
                     [self.player2.location[0],self.player2.location[1]]),
                     'msg': 'Cont',
                     'state': 1}  
        return data_struct
      else:
        self.loc[self.player1.location[0]][self.player1.location[1]] = 1
        self.draw(self.player1.location, self.image_dict[data['player1_images'][0]])

    if head_pos_2 != 0:
      self.player2.location = head_pos_2
      print head_pos_2
      if self.loc_collision(self.loc, self.player2):
      # will have to send to master node that there is a winner!
        print 'PLAYER 2 WINS'
        data_struct = {'player_locations':
                    ([self.player1.location[0],self.player1.location[1]],
                     [self.player2.location[0],self.player2.location[1]]),
                     'msg': 'Cont',
                     'state': 1}  
        # sys.exit()  
        return data_struct
      else:
        self.loc[self.player2.location[0]][self.player2.location[1]] = 1
        self.draw(self.player2.location, self.image_dict[data['player2_images'][0]])

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

    pygame.display.flip()

    data_struct = {'player_locations':
                  ([self.player1.location[0],self.player1.location[1]],
                    [self.player2.location[0],self.player2.location[1]]),
                  'msg': 'Cont',
                  'state': 0}

    return(data_struct)

  def loc_collision(self, loc, bike):
    if loc[bike.location[0]][bike.location[1]] == 1:
      print "location already occupied at " + str(bike.location[0]) + " " + str(bike.location[1])
      return True
    else:
      return False

  def draw(self, location, image):
    """draws the image at the location, properly scaled from the grid space,
    draws a black square first where it will be drawn"""
    pygame.draw.rect(self.window, (0,0,0), 
                        (location[0]*self.SCALE, 
                        location[1]*self.SCALE, 
                        self.SCALE, self.SCALE))
    self.window.blit(image, (location[0]*self.SCALE, location[1]*self.SCALE))

  def load_images(self):
    image_dict = {}
    image_dict['c_hd_rt'] = pygame.image.load('assets/comet_head.png').convert_alpha()
    image_dict['c_hd_dn'] = pygame.transform.rotate(image_dict['c_hd_rt'], -90)
    image_dict['c_hd_lf'] = pygame.transform.rotate(image_dict['c_hd_rt'], -180)
    image_dict['c_hd_up'] = pygame.transform.rotate(image_dict['c_hd_rt'], -270)

    image_dict['m_hd_rt'] = pygame.image.load('assets/meteor_head.png').convert_alpha()
    image_dict['m_hd_dn'] = pygame.transform.rotate(image_dict['m_hd_rt'], -90)
    image_dict['m_hd_lf'] = pygame.transform.rotate(image_dict['m_hd_rt'], -180)
    image_dict['m_hd_up'] = pygame.transform.rotate(image_dict['m_hd_rt'], -270)

    image_dict['c_md_hor_r'] = pygame.image.load('assets/comet_mid.png').convert_alpha()
    image_dict['c_md_ver_u'] = pygame.transform.rotate(image_dict['c_md_hor_r'], 90)
    image_dict['c_md_hor_l'] = pygame.transform.rotate(image_dict['c_md_hor_r'], 180)
    image_dict['c_md_ver_d'] = pygame.transform.rotate(image_dict['c_md_hor_r'], 270)

    image_dict['c_tl_hor'] = pygame.image.load('assets/comet_tail.png').convert_alpha()
    image_dict['c_tl_ver'] = pygame.transform.rotate(image_dict['c_tl_hor'], 90)

    image_dict['m_md_hor_r'] = pygame.image.load('assets/meteor_mid.png').convert_alpha()
    image_dict['m_md_ver_u'] = pygame.transform.rotate(image_dict['m_md_hor_r'], 90)
    image_dict['m_md_hor_l'] = pygame.transform.rotate(image_dict['m_md_hor_r'], 180)
    image_dict['m_md_ver_d'] = pygame.transform.rotate(image_dict['m_md_hor_r'], 270)

    image_dict['m_tl_hor'] = pygame.image.load('assets/meteor_tail.png').convert_alpha()
    image_dict['m_tl_ver'] = pygame.transform.rotate(image_dict['m_tl_hor'], 90)

    image_dict['m_co_ur'] = pygame.image.load('assets/meteor_corner.png').convert_alpha()
    image_dict['m_co_lr'] = pygame.transform.rotate(image_dict['m_co_ur'], -90)
    image_dict['m_co_ll'] = pygame.transform.rotate(image_dict['m_co_ur'], -180)
    image_dict['m_co_ul'] = pygame.transform.rotate(image_dict['m_co_ur'], -270)
 
    image_dict['c_co_ur'] = pygame.image.load('assets/comet_corner.png').convert_alpha()
    image_dict['c_co_lr'] = pygame.transform.rotate(image_dict['c_co_ur'], -90)
    image_dict['c_co_ll'] = pygame.transform.rotate(image_dict['c_co_ur'], -180)
    image_dict['c_co_ul'] = pygame.transform.rotate(image_dict['c_co_ur'], -270)

    return image_dict
 


  def translate_position(self, pos):
    """tanslates the entire game board to the local one"""

    if (pos[0] < (self.tile[0]+1)*(self.GRID_SIZEX) and 
        pos[0] >= self.tile[0]*(self.GRID_SIZEX) and 
        pos[1] < (self.tile[1]+1)*(self.GRID_SIZEY) and 
        pos[1] >= self.tile[1]*(self.GRID_SIZEY)):
        translated_pos = [pos[0] - self.tile[0]*(self.GRID_SIZEX),
                           (self.tile[1])*(self.GRID_SIZEY) + pos[1]] 
        # print "player 1 trans at " + str(translated_pos_1)
    else: translated_pos = 0
    return translated_pos #, translated_pos_2)

  def make_data_struct(self, message, state):
    return


















