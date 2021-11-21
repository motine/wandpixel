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

class Strip(object):
  def __init__(self):
    pass

  def do_loop(self):
    strip.fill((0, 0, 0))
    strip.show()
    pass

  def quit(self):
    self.fill((0, 0, 0))
    self.show()
    pass

  def fill(self, color):
    for i in range(PIXEL_HEIGHT * PIXEL_WIDTH):
      self.set_pixel(i, color)

  def set_pixel(self, coordinate_or_index, color):
    pass

  def show(self):
    pass

class VirtualStrip(Strip):
  def __init__(self):
    super(VirtualStrip, self).__init__()
    pygame.init()
    pygame.display.set_caption("Wandpixel")
    self.surface = pygame.display.set_mode((PIXEL_WIDTH*PIXEL_DISPLAY_SIZE, PIXEL_HEIGHT*PIXEL_DISPLAY_SIZE))
    self.pixel_colors = [ [(0, 0, 0)]*PIXEL_WIDTH for _ in range(PIXEL_HEIGHT)]
    
  def do_loop(self):
    for event in pygame.event.get():
      if (event.type == pygame.QUIT):
        raise KeyboardInterrupt

  def quit(self):
    super()
    pygame.quit()

  def set_pixel(self, coordinate_or_index, color):
    if isinstance(coordinate_or_index, int):
      index = coordinate_or_index
      self.set_pixel((index % PIXEL_WIDTH, int(index/PIXEL_WIDTH)), color)
      return
    self.pixel_colors[coordinate_or_index[1]][coordinate_or_index[0]] = color

  def show(self):
    self.surface.fill(BACKGROUND_COLOR)
    for y in range(PIXEL_HEIGHT):
      for x in range(PIXEL_WIDTH):
        left, top = x*PIXEL_DISPLAY_SIZE, y*PIXEL_DISPLAY_SIZE
        self.surface.fill(self.pixel_colors[y][x], rect=(left+PIXEL_DISPLAY_INSET, top+PIXEL_DISPLAY_INSET, PIXEL_DISPLAY_INNER_SIZE, PIXEL_DISPLAY_INNER_SIZE))
    pygame.display.flip()

class LedStrip(Strip):
  def __init__(self):
    super(LedStrip, self).__init__()
    pass
    
  def set_pixel(self, coordinate_or_index, color):
    # this would use for the real pixel
    pass

  def show(self):
    pass

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print('please specify a script')
    sys.exit(1)

  draw_module = importlib.import_module(sys.argv[1])
  if hasattr(draw_module, 'FPS'):
    FPS = draw_module.FPS

  strip = VirtualStrip()
  fps_clock = pygame.time.Clock()

  try:
    while True:
      strip.do_loop()
      draw_module.draw(strip)
      fps_clock.tick(FPS)
  finally:
    strip.quit()
