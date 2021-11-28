# NOTE
# to run this, you need:
# python3 -m pip install --upgrade Pillow

from lib.engine import PIXEL_WIDTH, PIXEL_HEIGHT
from PIL import Image
import random

FPS = 10
DIRECTION_RAND = 0.05
DIRECTION_MAX = 0.5
WINDOW_FACTOR = 20 # size of the window we crop out of the image before we size it down
WINDOW_WIDTH = PIXEL_WIDTH * WINDOW_FACTOR
WINDOW_HEIGHT = PIXEL_HEIGHT * WINDOW_FACTOR
image = None
offset = [0.0, 0.0]
direction = [1.0, 0.1]

def init(strip, args):
  if not args:
    raise f"please specify an image"

  global image
  image = Image.open(args[0])
  image = image.convert("RGB")


def draw(strip):
  global image, offset, direction
  
  current_image = image.copy()
  offset_x, offset_y = int(offset[0]), int(offset[1])
  current_image = current_image.crop((offset_x, offset_y, offset_x+WINDOW_WIDTH, offset_y+WINDOW_HEIGHT))
  current_image.thumbnail((PIXEL_WIDTH, PIXEL_HEIGHT))

  # draw
  strip.fill((0, 0, 0))
  for i, (r, g, b) in enumerate(current_image.getdata()):
    x, y = int(i % current_image.width), int(i / current_image.width)
    strip.set_pixel((x, y), (r, g, b))

  offset[0] = (offset[0] + direction[0]) % (image.width - WINDOW_WIDTH)
  offset[1] = (offset[1] + direction[1]) % (image.height - WINDOW_HEIGHT)

  direction[0] += random.uniform(-DIRECTION_RAND, DIRECTION_RAND) # randomize
  direction[1] += random.uniform(-DIRECTION_RAND, DIRECTION_RAND)
  direction[0] = max(-DIRECTION_MAX, min(DIRECTION_MAX, direction[0])) # cap
  direction[1] = max(-DIRECTION_MAX, min(DIRECTION_MAX, direction[1]))

  strip.show()
