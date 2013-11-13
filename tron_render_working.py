# tron render code
import pygame
import sys
import SocketServer, struct, threading
import network as n
import cPickle

FPS = pygame.time.Clock()
# self.player1 = LightBike([0,0], [1,0], (255,0,0))
# player2 = LightBike([40,40], [1,0], (0,255,0))


GRID_SIZEX = 100 # will probably need to be rectangular
GRID_SIZEY = 100
# game = Game()
# for x in range(0,GRID_SIZEX + 1):
#   loc.append([])
#   for y in range(0,GRID_SIZEY + 1):
#     loc[x].append(0) # 0 means not moved there yet

# # global vars for some stuff
# SCALE = 10
# WIDTH = len(loc) * SCALE
# HEIGHT = len(loc[0]) * SCALE
# SIZE = (WIDTH, HEIGHT) # width of screen
# player1 = LightBike([0,0], [1,0], (255,0,0))
# player2 = LightBike([40,40], [1,0], (0,255,0))


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


class Game(object):
  """holds everything for hte game"""
  def __init__(self):
    self.GRID_SIZEX = 100 # will probably need to be rectangular
    self.GRID_SIZEY = 100
    self.loc = []
    for x in range(0,GRID_SIZEX + 1):
      self.loc.append([])
      for y in range(0,GRID_SIZEY + 1):
        self.loc[x].append(0) # 0 means not moved there yet

    self.SCALE = 10
    self.WIDTH = len(self.loc) * self.SCALE
    self.HEIGHT = len(self.loc[0]) * self.SCALE
    self.SIZE = (self.WIDTH, self.HEIGHT) # widt
    self.player1 = LightBike([0,0], [1,0], (255,0,0))
    self.player2 = LightBike([40,40], [1,0], (0,255,0))
    pygame.init()
    self.window = pygame.display.set_mode(self.SIZE)
    # print 'here'


  def run(self):
    """starts the game and runs the server"""
    server=n.broadcastServer( ( '10.10.0.1', 20000 ), n.requestHandler )
    server.serve_forever()
    # print 'herel'

  def handle(self, pickled_data):
    # unique to each app, parse the data and call functions and such
    data = cPickle.loads(pickled_data)
    if data['player1move'] == 'left':
      self.player1.moveleft()
    elif data['player1move'] == 'right':
      self.player1.moveright()
    elif data['player1move'] == 'up':
      self.player1.moveup()
    elif data['player1move'] == 'down':
      self.player1.movedown()

    if data['player2move'] == 'left':
      self.player2.moveleft()
    elif data['player2move'] == 'right':
      self.player2.moveright()
    elif data['player2move'] == 'up':
      self.player2.moveup()
    elif data['player2move'] == 'down':
      self.player2.movedown()


    self.player1.update()
    self.player2.update()
    if loc_collision(self.loc, self.player1):
      # will have to send to master node that there is a winner!
      print 'PLAYER 2 WINS'
      sys.exit()
    if loc_collision(self.loc, self.player2):
      print 'PLAYER 1 WINS'
      sys.exit()

    self.loc[self.player1.location[0]][self.player1.location[1]] = 1
    self.loc[self.player2.location[0]][self.player2.location[1]] = 1

    pygame.draw.rect(self.window, self.player1.color, (self.player1.location[0]*self.SCALE, self.player1.location[1]*self.SCALE, self.SCALE, self.SCALE))
    pygame.draw.rect(self.window, self.player2.color, (self.player2.location[0]*self.SCALE, self.player2.location[1]*self.SCALE, self.SCALE, self.SCALE))
    pygame.display.flip()
    # FPS.tick(60)
    # print data

game = Game()

def process_request(pickled_data):
  global game
  game.handle(pickled_data)

def loc_collision(loc, bike):
  # check the location array to see if colided.
  if bike.location[0] < 0 or bike.location[0] > GRID_SIZEX:
    return True
  if bike.location[1] < 0 or bike.location[1] > GRID_SIZEY:
    return True
  if loc[bike.location[0]][bike.location[1]] == 1:
    # something was drawn there you hit!!
    return True
  else:
    return False


# change all of this to a game class
if __name__ == '__main__':
  global game
  # game = Game()
  game.run()

