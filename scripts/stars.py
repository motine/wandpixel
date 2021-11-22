from random import randrange
from math import floor
from lib.engine import PIXEL_WIDTH, PIXEL_HEIGHT
from PIL import Image

# to run this, you need:
# python3 -m pip install --upgrade Pillow

FPS = 5
RESET_AFTER_ITERATIONS = 10000

im = Image.open('images/star-bg.png')
im = im.convert("RGB")

class Star(object):
  def __init__(self, x, y, luminosity):
    self.x, self.y, self.luminosity = x, y, luminosity
    self.luminosity_add = 0

  def twinkle(self):
    max_range = int(floor(self.luminosity * 0.2))
    step_range = int(floor(max_range * 0.2))
    add = self.luminosity_add
    add += randrange(-step_range, step_range)
    add = min(add, max_range)
    add = max(add, -max_range)
    self.luminosity_add = add

  def draw(self, strip):
    current_luminosity = min(self.luminosity + self.luminosity_add, 255)
    strip.set_pixel((self.x, self.y), [current_luminosity] * 3)

stars = []
iteration = 0

def reset_stars():
  global stars  
  stars = [ Star(randrange(PIXEL_WIDTH), randrange(PIXEL_HEIGHT-5), randrange(50, 256)) for _ in range(10) ]

reset_stars()

def draw(strip):
  global iteration
  if iteration == 0:
    reset_stars()
  iteration = (iteration + 1) % RESET_AFTER_ITERATIONS

  global im
  for i, (r, g, b) in enumerate(im.getdata()):
    strip.set_pixel(i, (r, g, b))

  global stars
  for star in stars:
    star.draw(strip)
    star.twinkle()
  
  strip.show()
