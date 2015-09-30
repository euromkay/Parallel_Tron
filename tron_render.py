#!/usr/bin/env python
import pygame
import sys, os
import networking as n 
import tron
import socket

FPS = pygame.time.Clock()
# self.player1 = LightBike([0,0], [1,0], (255,0,0))
# player2 = LightBike([40,40], [1,0], (0,255,0))


# GRID_SIZEX = 100 # will probably need to be rectangular
# GRID_SIZEY = 100

# # change all of this to a game class
def display(ip, port, x, y, scale, coords = None):
  if coords != None:
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % coords
  # game = Game.Game() # initilize game and pygame
  # middleware = n.MiddleWare(game)
  # find which ip address to host on
  #if y == 2:
   # y = 0
  #elif y == 0:
   # y = 2
  game = tron.Game([x, y], scale)
  server = n.Server(game)
  server.open_connection(ip, port)
  while True:
    server.recev_connection()

