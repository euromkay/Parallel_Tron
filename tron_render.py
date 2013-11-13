# tron render code
import pygame
import sys
import network as n
import Game

FPS = pygame.time.Clock()
# self.player1 = LightBike([0,0], [1,0], (255,0,0))
# player2 = LightBike([40,40], [1,0], (0,255,0))


# GRID_SIZEX = 100 # will probably need to be rectangular
# GRID_SIZEY = 100

# # change all of this to a game class
if __name__ == '__main__':
  # game = Game.Game() # initilize game and pygame
  # middleware = n.MiddleWare(game)
  # find which ip address to host on
  myhostname = socket.gethostname()
  (_,xindx,yindx) = myhostname.split('-')
  xindx = int(xindx)
  yindx = int(yindx)
  print yindx
  print xindx
  game = tron.Game([xindx, yindx])
  for line in open('/etc/hosts').readlines():
    if line.find(myhostname) > -1:
      if first_hit:
        my_ip_address = line.split()[0]
      else:
        first_hit = True
        
  print my_ip_address
  server = n.server(my_ip_address, 20000, game )
  server.open_connection()
  while True:
    server.recev_connection()
    FPS.tick(5)

