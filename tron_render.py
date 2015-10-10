#!/usr/bin/env python
import pygame
import sys, os
import networking 
import tron
import socket

FPS = pygame.time.Clock()
# self.player1 = LightBike([0,0], [1,0], (255,0,0))
# player2 = LightBike([40,40], [1,0], (0,255,0))


# GRID_SIZEX = 100 # will probably need to be rectangular
# GRID_SIZEY = 100

# # change all of this to a game class
def display(ip, port, x, y, scale, coords = None):
  game = tron.Game([x, y], scale)

  mode = 0
  if coords != None:
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((game.WIDTH+10)*x, (game.HEIGHT+60)*y)
    mode = pygame.NOFRAME
  else:
    mode = pygame.FULLSCREEN

  game = tron.Game([x, y], scale, mode)
  # game = Game.Game() # initilize game and pygame
  # middleware = n.MiddleWare(game)
  # find which ip address to host on
  #if y == 2:
   # y = 0
  #elif y == 0:
   # y = 2
  server = networking.Server(game)
  server.open_connection(ip, port)
  while True:
    server.recev_connection()

