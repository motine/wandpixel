import re
import urllib.request
from datetime import datetime
from lib.engine import PIXEL_WIDTH, PIXEL_HEIGHT

FPS = 10
REFRESH_WEATHER_EVERY_SEC = 60*60

DIGITS = (
  ( (1,1,1), # 0
    (1,0,1),
    (1,0,1),
    (1,0,1),
    (1,1,1)),
  ( (0,1,1), # 1
    (0,0,1),
    (0,0,1),
    (0,0,1),
    (0,0,1)),
  ( (1,1,1), # 2
    (0,0,1),
    (1,1,1),
    (1,0,0),
    (1,1,1)),
  ( (1,1,1), # 3
    (0,0,1),
    (0,1,1),
    (0,0,1),
    (1,1,1)),
  ( (1,0,0), # 4
    (1,0,0),
    (1,1,1),
    (0,1,0),
    (0,1,0)),
  ( (1,1,1), # 5
    (1,0,0),
    (1,1,1),
    (0,0,1),
    (1,1,1)),
  ( (1,0,0), # 6
    (1,0,0),
    (1,1,1),
    (1,0,1),
    (1,1,1)),
  ( (1,1,1), # 7
    (0,0,1),
    (0,1,1),
    (0,1,0),
    (0,1,0)),
  ( (1,1,1), # 8
    (1,0,1),
    (1,1,1),
    (1,0,1),
    (1,1,1)),
  ( (1,1,1), # 9
    (1,0,1),
    (1,1,1),
    (0,0,1),
    (0,0,1)
  )
)

DEGREE = (
  (1,),
  (0,),
  (0,),
  (0,),
  (0,))

MINUS = (
  (0,0),
  (0,0),
  (1,1),
  (0,0),
  (0,0))

def draw_bitmap(bitmap, strip, position, color):
  for y, row in enumerate(bitmap):
    for x, cell in enumerate(row):
      if cell:
        strip.set_pixel((position[0]+x, position[1]+y), color)

def draw_digit(digit_value, strip, position, color):
  draw_bitmap(DIGITS[digit_value], strip, position, color)

# right aligned numbers
# degree sign is not right aligned, but added to the right
def draw_number(number, strip, top_right, color, add_degree=False, add_minus=False):
  if number >= 100:
    raise TypeError("we only support up to two digits")
  if number < 0:
    draw_number(-number, strip, top_right, color, add_degree=add_degree, add_minus=True)
    return

  left = None
  if number >= 10:
    width = len(DIGITS[0][0]) * 2 + 1 # 2 digits + 1 space
    draw_digit(int(number / 10), strip, (top_right[0] - 7, top_right[1]), color)
    draw_digit(number % 10, strip, (top_right[0] - 3, top_right[1]), color)
    left = top_right[0] - 7
  if number < 10:
    draw_digit(number, strip, (top_right[0] - 3, top_right[1]), color)
    left = top_right[0] - 3

  if add_degree:
    draw_bitmap(DEGREE, strip, (top_right[0] + 1, top_right[1]), color)
  if add_minus:
    draw_bitmap(MINUS, strip, (left - 3, top_right[1]), color)

temperature = 0
last_temperature_fetch = datetime(2000, 1, 1)

def fetch_temperature():
  global temperature, last_temperature_fetch
  with urllib.request.urlopen("http://wttr.in/Berlin?format=\"%t\"") as f:
    conditions_string = f.read().decode('utf-8')
    temperature = -int(re.sub('[^\d\-]', '', conditions_string))
    last_temperature_fetch = datetime.now()

fetch_temperature()

def draw(strip):
  global temperature, last_temperature_fetch
  temperature_age = datetime.now() - last_temperature_fetch
  if temperature_age.total_seconds() > REFRESH_WEATHER_EVERY_SEC:
    print('refreshing weather...')
    fetch_temperature()
  strip.fill((0, 0, 0))
  draw_number(temperature, strip, (PIXEL_WIDTH - 3, PIXEL_HEIGHT - 6), (255, 255, 255), add_degree=True)

  # global number
  # draw_number(-number, strip, (PIXEL_WIDTH - 3, PIXEL_HEIGHT - 6), (255, 255, 255), add_degree=True)
  # number = (number + 1) % 50
  
  strip.show()
