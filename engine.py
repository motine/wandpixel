#!/usr/bin/env python3

# python3 -m pip install -U pygame --user

import importlib
import sys
import pygame
from pygame.locals import *

PIXEL_WIDTH = 14
PIXEL_HEIGHT = 25
PIXEL_DISPLAY_SIZE = 30
PIXEL_DISPLAY_INSET = 1 # px on each side
PIXEL_DISPLAY_INNER_SIZE = PIXEL_DISPLAY_SIZE - 2*PIXEL_DISPLAY_INSET
FPS = 30

BACKGROUND_COLOR = (35, 35, 35)

class Strip:
  def __init__(self):
    self.pixel_colors = [ [(0, 0, 0)]*PIXEL_WIDTH for i in range(PIXEL_HEIGHT)]

  def setPixel(self, x, y, color):
    # this would use setPixelColor for the real pixel
    self.pixel_colors[y][x] = color

  def show(self):
    surface.fill(BACKGROUND_COLOR)
    for y in range(PIXEL_HEIGHT):
      for x in range(PIXEL_WIDTH):
        left, top = x*PIXEL_DISPLAY_SIZE, y*PIXEL_DISPLAY_SIZE
        surface.fill(self.pixel_colors[y][x], rect=(left+PIXEL_DISPLAY_INSET, top+PIXEL_DISPLAY_INSET, PIXEL_DISPLAY_INNER_SIZE, PIXEL_DISPLAY_INNER_SIZE))
    pygame.display.flip()

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print('please specify a script')
    sys.exit(1)
  draw_module = importlib.import_module(sys.argv[1])
  if hasattr(draw_module, 'FPS'):
    FPS = draw_module.FPS

  pygame.init() 
  fps_clock = pygame.time.Clock()
  surface = pygame.display.set_mode((PIXEL_WIDTH*PIXEL_DISPLAY_SIZE, PIXEL_HEIGHT*PIXEL_DISPLAY_SIZE))
  pygame.display.set_caption("Wandpixel")

  strip = Strip()

  gameLoop = True
  while gameLoop:
    for event in pygame.event.get():
      if (event.type == pygame.QUIT):
        gameLoop = False
    draw_module.draw(strip, PIXEL_WIDTH, PIXEL_HEIGHT)
    fps_clock.tick(FPS)
  pygame.quit()
