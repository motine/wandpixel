#!/usr/bin/env python3

# python3 -m pip install -U pygame --user

import importlib
import sys
import csv
from pathlib import Path
import pygame

PIXEL_WIDTH = 14
PIXEL_HEIGHT = 25
FPS = 30

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

  # coordinate_or_index can either be a tuple or a single int
  # if a tuple is given, we use the format (x, y)
  # if an int is given, it is up to the derriving Strip class how to layout the pixels (the only guarantee is that 0..width*height-1 is valid)
  def set_pixel(self, coordinate_or_index, color):
    pass

  def show(self):
    pass


class VirtualStrip(Strip):
  PIXEL_DISPLAY_SIZE = 30
  PIXEL_DISPLAY_INSET = 1 # px on each side
  PIXEL_DISPLAY_INNER_SIZE = PIXEL_DISPLAY_SIZE - 2*PIXEL_DISPLAY_INSET
  BACKGROUND_COLOR = (35, 35, 35)

  def __init__(self):
    super(VirtualStrip, self).__init__()
    pygame.init()
    pygame.display.set_caption("Wandpixel")
    self.surface = pygame.display.set_mode((PIXEL_WIDTH*self.PIXEL_DISPLAY_SIZE, PIXEL_HEIGHT*self.PIXEL_DISPLAY_SIZE))
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
    self.surface.fill(self.BACKGROUND_COLOR)
    for y in range(PIXEL_HEIGHT):
      for x in range(PIXEL_WIDTH):
        left, top = x*self.PIXEL_DISPLAY_SIZE, y*self.PIXEL_DISPLAY_SIZE
        self.surface.fill(self.pixel_colors[y][x], rect=(left+self.PIXEL_DISPLAY_INSET, top+self.PIXEL_DISPLAY_INSET, self.PIXEL_DISPLAY_INNER_SIZE, self.PIXEL_DISPLAY_INNER_SIZE))
    pygame.display.flip()

class LedStrip(Strip):
  LED_COUNT      = 350     #  Number of LED pixels.
  LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
  LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
  LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
  LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
  LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
  LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

  PIXEL_MAPPING = {
    0: 0,
    1: 1,
    2: 2,
    3: 4
  }

  def __init__(self):
    super(LedStrip, self).__init__()
    import rpi_ws281x
    self.read_pixel_mapping()
    self.neopixel = rpi_ws281x.Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
    self.neopixel.begin()

  def read_pixel_mapping(self):
    self.pixel_mapping = {}
    with open('helper/pixel-arrangement.csv', newline='') as f:
      reader = csv.reader(f, delimiter=';')
      for y, row in enumerate(reader):
        for x, cell in enumerate(row):
          if (cell):
            self.pixel_mapping[y*PIXEL_WIDTH + x] = cell

  def set_pixel(self, coordinate_or_index, color):
    if (isinstance(coordinate_or_index, tuple) or isinstance(coordinate_or_index, list)):
      self.set_pixel(coordinate_or_index[1]*PIXEL_WIDTH + coordinate_or_index[0])
      return
    if (isinstance(coordinate_or_index, int)):
      index = coordinate_or_index
      if not index in self.pixel_mapping:
        return # this is a dead pixel, so we ignore it (e.g. one in the top-right corner)
      real_index = self.pixel_mapping[index]
      self.neopixel.setPixelColor(real_index, color)

    raise TypeError # no idea what to do with coordinate_or_index

  def show(self):
    self.neopixel.show()

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print('please specify a script')
    sys.exit(1)

  draw_module = importlib.import_module(sys.argv[1])
  if hasattr(draw_module, 'FPS'):
    FPS = draw_module.FPS

  if Path("USE_LEDS").is_file():
    strip = LedStrip()
  else:
    strip = VirtualStrip()
  fps_clock = pygame.time.Clock()

  try:
    while True:
      strip.do_loop()
      draw_module.draw(strip)
      fps_clock.tick(FPS)
  except KeyboardInterrupt:
    pass
  finally:
    strip.quit()
