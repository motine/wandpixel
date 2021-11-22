from lib.engine import PIXEL_WIDTH, PIXEL_HEIGHT
import random

FPS = 20

x, y = (0, 0)

def draw(strip):
  global x, y

  strip.fill((0,0,0))
  strip.set_pixel((x, y), (255, 255, 255))

  if (x == PIXEL_WIDTH-1):
    y = (y + 1) % PIXEL_HEIGHT
    x = 0
  else:
    x = x + 1
  
  strip.show()
