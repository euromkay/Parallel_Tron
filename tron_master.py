# tron master node
import pygame
from pygame.locals import *
import socket, struct, threading, sys
import cPickle, time
from pprint import pprint
# from helper import draw_logic, load_images, construct_list


FULL_GRID_SIZE = (20, 10) # number of locations in full game 
PLAYER1_START = [0, FULL_GRID_SIZE[1]/2]
PLAYER2_START = [FULL_GRID_SIZE[0]-1, FULL_GRID_SIZE[1]/2]
MONITOR_GRIDX = 2 # width 
MONITOR_GRIDY = 1 # height
SOCKET_DEL = '*ET*'


def load_images():
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

class LightBike():
  def __init__(self, startloc, start_orient, startvel, last_key):
    self.location = startloc
    self.velocity = startvel
    self.orientation = start_orient
    self.last_key = last_key
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
    self.location[0] += self.velocity[0]
    self.location[1] += self.velocity[1]

def get_whole_packet(socket):
  data = ''
  while True:
    data += socket.recv(4024)
    split = data.split(SOCKET_DEL) # split at newline, as per our custom protocol
    if len(split) != 2: # it should be 2 elements big if it got the whole message
      pass
    else:
      x = cPickle.loads(split[0])
      return x

def loc_collision(bike):
  # check the location array to see if colided.
  if bike.location[0] < 0 or bike.location[0] > FULL_GRID_SIZE[0]:
    print "died of screen in x"
    return True
  if bike.location[1] < 0 or bike.location[1] > FULL_GRID_SIZE[1]:
    print "died off screen in y"
    return True

def close_sockets(sock_list):
  kill_struct = {'kill_state': 1 }
  kill_pickle = cPickle.dumps(kill_struct, cPickle.HIGHEST_PROTOCOL) + '*ET*'
  for x in range(0, len(sock_list)):
    for y in range(0, len(sock_list[x])):
      sock_list[x][y].sendall(kill_pickle)
      sock_list[x][y].shutdown(socket.SHUT_RDWR)
      sock_list[x][y].close()
  sys.exit()
  
def construct_list(last_2_loc, last_loc, head, middle, tail):
  """logic for corner cases when drawing the corners. The case for 
  when there is a corner followed by another corner. Lets the drawing nodes
  know that the second to last location was also a corner so leave it unchagned"""
  if last_loc[1] == 'cor':
    return [head, middle, 'corner']
  else:
    return[head, middle, tail]

def draw_logic(last_2_loc, last_loc, player, which):
  """decides which images to tell the render nodes to draw"""
  image_key_list = []
  if last_loc[0][0] == player.location[0] and last_loc[0][0] == last_2_loc[0][0]:
    # traveling vertically straight
    if last_loc[0][1] > player.location[1]:
      # traveling UP
      image_key_list.append(which + '_hd_up')
      image_key_list.append(which + '_md_ver_u')
    else:
      # traveling DOWN
      image_key_list.append(which + '_hd_dn')
      image_key_list.append(which + '_md_ver_d')
    if last_2_loc[1] != 'cor':
      # don't override corners for tail
      image_key_list.append(which + '_tl_'+last_loc[1])
    else: 
      image_key_list.append('corner')
    last_loc[1] = 'ver'
    # player.orientation = 'ver'
  elif last_loc[0][1] == player.location[1] and last_loc[0][1] == last_2_loc[0][1]:
    # traveling horizontally straight
    if last_loc[0][0] > player.location[0]:
       # traveling left
      image_key_list.append(which + '_hd_lf')
      image_key_list.append(which + '_md_hor_l')
    else:
       # traveling right
      image_key_list.append(which + '_hd_rt')
      image_key_list.append(which + '_md_hor_r')
    if last_2_loc[1] != 'cor':
      # don't override corners for tail
      image_key_list.append(which + '_tl_'+last_loc[1])
    else:
      # don't need to update corner drawing
      image_key_list.append('corner')
    last_loc[1] = 'hor' 
  else:
    #traveling the corners
    print "here"
    print "player.location = " + str(player.location) + "prev_loc = " + str(last_loc) + " last_2_loc = " + str(last_2_loc)
    # at a corner, checking explicitly for the eight cases
    if (player.location[0] == last_loc[0][0] and player.location[0] > last_2_loc[0][0]
      and player.location[1] > last_loc[0][1] and player.location[1] > last_2_loc[0][1]):
      #upper right, going down
      image_key_list = construct_list(last_2_loc, last_loc, which + '_hd_dn', which + '_co_ur', which + '_tl_hor')
      last_loc[1] = 'cor'
    elif (player.location[0] < last_loc[0][0] and player.location[0] < last_2_loc[0][0]
      and player.location[1] == last_loc[0][1] and player.location[1] < last_2_loc[0][1]):
      #upper right, going left
      image_key_list = construct_list(last_2_loc, last_loc, which + '_hd_lf', which + '_co_ur',which + '_tl_ver' )
      last_loc[1] = 'cor'

    elif (player.location[0] > last_loc[0][0] and player.location[0] > last_2_loc[0][0]
      and player.location[1] == last_loc[0][1] and player.location[1] > last_2_loc[0][1]):
      # lower left, going right
      image_key_list = construct_list(last_2_loc, last_loc, which + '_hd_rt', which + '_co_ll',which + '_tl_ver' )
      last_loc[1] = 'cor'

    elif (player.location[0] == last_loc[0][0] and player.location[0] < last_2_loc[0][0]
      and player.location[1] < last_loc[0][1] and player.location[1] < last_2_loc[0][1]):
       # lower left, clockwise
      image_key_list = construct_list(last_2_loc, last_loc, which + '_hd_up', which + '_co_ll',which + '_tl_hor' )
      last_loc[1] = 'cor'
       
    elif (player.location[0] > last_loc[0][0] and player.location[0] > last_2_loc[0][0]
      and player.location[1] == last_loc[0][1] and player.location[1] < last_2_loc[0][1]):
      # upper left clockwise
      image_key_list = construct_list(last_2_loc, last_loc, which + '_hd_rt', which + '_co_ul',which + '_tl_ver' )
      last_loc[1] = 'cor'
       
    elif (player.location[0] == last_loc[0][0] and player.location[0] < last_2_loc[0][0]
      and player.location[1] > last_loc[0][1] and player.location[1] > last_2_loc[0][1]):
      # upper left counterclockwise
      image_key_list = construct_list(last_2_loc, last_loc, which + '_hd_dn', which + '_co_ul',which + '_tl_hor' )
      last_loc[1] = 'cor'
       
    elif (player.location[0] == last_loc[0][0] and player.location[0] > last_2_loc[0][0]
      and player.location[1] < last_loc[0][1] and player.location[1] < last_2_loc[0][1]):
      # lower right counterclockwise
      image_key_list = construct_list(last_2_loc, last_loc, which + '_hd_up', which + '_co_lr',which + '_tl_hor' )
      last_loc[1] = 'cor'
       
    elif (player.location[0] < last_loc[0][0] and player.location[0] < last_2_loc[0][0]
      and player.location[1] == last_loc[0][1] and player.location[1] > last_2_loc[0][1]):
      # lower right clockwise
      image_key_list = construct_list(last_2_loc, last_loc, which + '_hd_lf', which + '_co_lr',which + '_tl_ver' )
      last_loc[1] = 'cor'
  return image_key_list

  

grid = []
if __name__ == '__main__':
  pygame.init()
  location = []
  for x in range(0,FULL_GRID_SIZE[0] ):
    location.append([])
    for y in range(0,FULL_GRID_SIZE[1]):
      location[x].append(0) # 0 

  player1 = LightBike(PLAYER1_START, 'hor', [1,0], K_LEFT)
  player2 = LightBike(PLAYER2_START, 'hor', [-1,0], K_d)
  last_loc_1 = [[-1, FULL_GRID_SIZE[1]/2], 'off'] # initilize off screen, shouldn't affect anythin
  last_2_loc_1 = [[-2, FULL_GRID_SIZE[1]/2], 'off']
  last_loc_2 = [[ FULL_GRID_SIZE[0], FULL_GRID_SIZE[1]/2] , 'off'] # initilize off screen, shouldn't affect anythin
  last_2_loc_2 = [[FULL_GRID_SIZE[0]+1, FULL_GRID_SIZE[1]/2], 'off']
  
  window = pygame.display.set_mode((20,20))
  image_dict = load_images()
  sock_list = [[ [] for y in range(MONITOR_GRIDY)] for x in range(MONITOR_GRIDX)]
  ip_list = [('localhost', 20000), ('localhost', 20001)]#, ('localhost', 20001)]
  idx = 0
  for x in range(0, MONITOR_GRIDX):
    for y in range(0, MONITOR_GRIDY):
      sock_list[x][y] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock_list[x][y].connect(ip_list[idx])
      idx += 1
  while True:
    # control block This will be the master node
    # send_struct = {'player1move':'', 'player2move': '', new_loc:[0,0]} # clear it everytime
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          sys.exit()
      if event.type == KEYDOWN:
        # check if trying to go back on them selves
        if event.key == K_LEFT:
          if player1.last_key != K_RIGHT and player1.last_key != K_LEFT:
            player1.moveleft()
            player1.last_key = K_LEFT
        if event.key == K_RIGHT and player1.last_key != K_RIGHT:
          if player1.last_key != K_LEFT:
            player1.moveright()
            player1.last_key = K_RIGHT
        if event.key == K_UP and player1.last_key != K_UP:
          if player1.last_key != K_DOWN:
            player1.moveup()
            player1.last_key = K_UP
        if event.key == K_DOWN and player1.last_key != K_DOWN:
          if player1.last_key != K_UP:
            player1.movedown()
            player1.last_key = K_DOWN
        if event.key == K_a and player2.last_key != K_a:
          if player2.last_key != K_d:
            player2.moveleft()
            player2.last_key = K_d
        if event.key == K_d and player2.last_key != K_d:
          if player2.last_key != K_a:
            player2.moveright()
            player2.last_key = K_a
        if event.key == K_w and player2.last_key != K_w:
          if player2.last_key != K_s:
            player2.moveup()
            player2.last_key = K_w
        if event.key == K_s and player2.last_key != K_s:
          if player2.last_key != K_w:
            player2.movedown()
            player2.last_key = K_s

    last_2_loc_1 = last_loc_1[:]
    last_loc_1[0] = [player1.location[0], player1.location[1]]
    last_2_loc_2 = last_loc_2[:]
    last_loc_2[0] = [player2.location[0], player2.location[1]]
    print last_loc_1
    player1.update()
    player2.update()
    player1_image_dict = draw_logic(last_2_loc_1, last_loc_1, player1, 'c')
    print last_loc_1[1]
    player2_image_dict = draw_logic(last_2_loc_2, last_loc_2, player2, 'm')
    # if loc_collision(player1):
    #   close_sockets(sock_list)
    # if loc_collision(player2):
    #   close_sockets(sock_list)

    location[player1.location[0]][player1.location[1]] = 1
    location[player2.location[0]][player2.location[1]] = 1
    send_struct = {'player1_images': player1_image_dict,
                'player2_images':player2_image_dict,
                'player1_locs':[player1.location, last_loc_1[0], last_2_loc_1[0]],
                'player2_locs':[player2.location, last_loc_2[0], last_2_loc_2[0]],
                'kill_state': 0}
    print "printing send struct"
    pprint(send_struct)
    # print "printing the location varibles"
    # print "player 1 currrent" + str(player1.location) + "player"

    # make it so the render communicates the velocity vector and the of the position
    # of the players. Pass the players to other nodes. 
    data = cPickle.dumps(send_struct, cPickle.HIGHEST_PROTOCOL) + '*ET*'
    for x in range(0, len(sock_list)):
      for y in range(0, len(sock_list[x])):
        sock_list[x][y].sendall(data)
    state_list = []
    # for x in range(0, len(sock_list)):
    #   for y in range(0, len(sock_list[x])):
    #     state_list.append(get_whole_packet(sock_list[x][y]))

    # for idx, state in enumerate(state_list):
    #   print state
    time.sleep(1)

