from math import sqrt
import colorsys
from lib.engine import PIXEL_WIDTH, PIXEL_HEIGHT

FPS = 4
TICK_ADD = 0.005
# DISTANCE_DIVISOR = sqrt(PIXEL_WIDTH**2 + PIXEL_HEIGHT**2)
DISTANCE_DIVISOR = 100 # defines how much the colors are streched out
# DISTANCE_DIVISOR = 50 # defines how much the colors are streched out

tick = 0.0 # adds TICK_ADD per frame

def draw(strip):
  global tick

  strip.fill((0,0,0))
  for y in range(0, PIXEL_HEIGHT):
    for x in range(0, PIXEL_WIDTH):
      distance = sqrt(x**2 + y**2) / DISTANCE_DIVISOR
      pulse = (distance - tick) % 1.0

      # gray scale pulse
      # intensity = int(pulse * 255)
      # strip.set_pixel((x, y), (intensity, intensity, intensity))

      # color pulse
      rgb_floats = colorsys.hsv_to_rgb(pulse, 1.0, 1.0)
      rgb = [int(component * 255) for component in rgb_floats]
      strip.set_pixel((x, y), rgb)

  tick += TICK_ADD

  strip.show()
