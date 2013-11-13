# tron master node
import pygame
from pygame.locals import *
import socket, struct, threading, sys
import cPickle, time
# import RPi.GPIO as GPIO
loc = [] 
# FPS = pygame.time.Clock()

# bigger since it's the whole playfield!!
GRID_SIZEX = 200 # will probably need to be rectangular
GRID_SIZEY = 200

class LightBike():
  def __init__(self, startloc, startvel, color):
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
    self.location[0] += self.velocity[0]
    self.location[1] += self.velocity[1]

if __name__ == '__main__':
  # intial game set up. 
  # loc will be local to each node
  loc = []
  for x in range(0,GRID_SIZEX + 1):
    loc.append([])
    for y in range(0,GRID_SIZEY + 1):
      loc[x].append(0) # 0 means not moved there yet

  SCALE = 10
  WIDTH = len(loc) * SCALE
  HEIGHT = len(loc[0]) * SCALE
  SIZE = (WIDTH, HEIGHT) # width of screen
  SPEED = 1 # amount to move in location grid ie
  velocity = [1,0] # start moving right
  current_loc = [0,0]

  player1 = LightBike([0,0], [1,0], (255,0,0))
  player2 = LightBike([40,40], [1,0], (0,255,0))
  send_struct = {'player1move':'right', 'player2move': 'left'}
  x = cPickle.dumps(send_struct, cPickle.HIGHEST_PROTOCOL) + '*ET*'
  amount_of_data = sys.getsizeof(x)
  print sys.getsizeof(x)
  # will only need to send coordinates though

  pygame.init()
  window = pygame.display.set_mode((20,20))
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect(('10.10.0.1', 20000))
  # count = 0
  # while count < 10:
  #   sock.sendall(x)
  #   y = sock.recv(16)
  #   print y
  while True:
    # control block This will be the master node
    send_struct = {'player1move':'', 'player2move': ''} # clear it everytime
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          sys.exit()
      if event.type == KEYDOWN:
          if event.key == K_LEFT:
            send_struct['player1move'] = 'left'
          if event.key == K_RIGHT:
            send_struct['player1move'] = 'right'
          if event.key == K_UP:
            send_struct['player1move'] = 'up'
          if event.key == K_DOWN:
            send_struct['player1move'] = 'down'
          if event.key == K_a:
            send_struct['player2move'] = 'left'
          if  event.key == K_d:
            send_struct['player2move'] = 'right'
          if event.key == K_w:
            send_struct['player2move'] = 'up'
          if event.key == K_s:
            send_struct['player2move'] = 'down'

    x = cPickle.dumps(send_struct, cPickle.HIGHEST_PROTOCOL) + '*ET*'
    sock.sendall(x)
    y = sock.recv(16)
    # print y




# if __name__ == '__mai__':
#   # intial game set up. 
#   # loc will be local to each node
#   for x in range(0,GRID_SIZEX + 1):
#     loc.append([])
#     for y in range(0,GRID_SIZEY + 1):
#       loc[x].append(0) # 0 means not moved there yet

#   SCALE = 10
#   WIDTH = len(loc) * SCALE
#   HEIGHT = len(loc[0]) * SCALE
#   SIZE = (WIDTH, HEIGHT) # width of screen
#   SPEED = 1 # amount to move in location grid ie
#   velocity = [1,0] # start moving right
#   current_loc = [0,0]

#   player1 = LightBike([0,0], [1,0], (255,0,0))
#   player2 = LightBike([40,40], [1,0], (0,255,0))

#   # Display stuff Should be segmented later
#   pygame.init() 
#   window = pygame.display.set_mode(SIZE)

#   # start with just a square


#   # MAKE THIS OO!!!! 
#   while True:

#     # control block This will be the master node
#     for event in pygame.event.get():
#           if event.type == pygame.QUIT:
#               sys.exit()
#           if event.type == KEYDOWN:
#               if event.key == K_LEFT:
#                 player1.moveleft()
#               if event.key == K_RIGHT:
#                 player1.moveright()
#               if event.key == K_UP:
#                 player1.moveup()
#               if event.key == K_DOWN:
#                 player1.movedown()
#               if event.key == K_a:
#                 player2.moveleft()
#               if  event.key == K_d:
#                 player2.moveright()
#               if event.key == K_w:
#                 player2.moveup()
#               if event.key == K_s:
#                 player2.movedown()

    
#     FPS.tick(60)


