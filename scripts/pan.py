# NOTE
# to run this, you need to install the following:
#   python3 -m pip install --upgrade Pillow
#   apt install libopenjp2-7
#
# you can call this script with multiple paths and the image will then swap after a while

from lib.engine import PIXEL_WIDTH, PIXEL_HEIGHT
from PIL import Image
import random
import time

FPS = 10
DIRECTION_RAND = 0.05
DIRECTION_MAX = 0.5
WINDOW_FACTOR = 20 # size of the window we crop out of the image before we size it down
WINDOW_WIDTH = PIXEL_WIDTH * WINDOW_FACTOR
WINDOW_HEIGHT = PIXEL_HEIGHT * WINDOW_FACTOR
NEXT_IMAGE_AFTER_SEC = 30*60

page_paths = None
# see load_next_image for the initialization of the following variables
image = None
offset = None
direction = None
last_image_change_time = None

def load_next_image():
  global image, offset, direction, last_image_change_time
  offset = [0.0, 0.0]
  direction = [1.0, 0.1]
  image = Image.open(random.choice(image_paths))
  image = image.convert("RGB")
  last_image_change_time = time.time()

def init(strip, args):
  if not args:
    raise f"please specify an image"

  global image_paths
  image_paths = args
  load_next_image()

def draw(strip):
  global image, offset, direction, last_image_change_time
  
  if (time.time() - last_image_change_time) > NEXT_IMAGE_AFTER_SEC:
    load_next_image()

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
