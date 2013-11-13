# tron render code
import pygame
import sys
import networking as n
import tron

FPS = pygame.time.Clock()
# self.player1 = LightBike([0,0], [1,0], (255,0,0))
# player2 = LightBike([40,40], [1,0], (0,255,0))


# GRID_SIZEX = 100 # will probably need to be rectangular
# GRID_SIZEY = 100

# # change all of this to a game class
if __name__ == '__main__':
  game = tron.Game([1,0]) # initilize game and pygame
  # middleware = n.MiddleWare(game)
  server = n.Server('localhost', 20001, game )
  server.open_connection()
  while True:
    server.recev_connection()
    FPS.tick(1)

