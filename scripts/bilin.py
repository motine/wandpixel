from lib.engine import PIXEL_WIDTH, PIXEL_HEIGHT
import random
import math

FPS = 10

t = 0.0

def draw(strip):
  global t

  t += 0.015
  phase1 = abs(math.sin(t))
  phase2 = 0.8 * abs(math.sin(t*1.2))
  phase3 = 0.5 * abs(math.sin(t*1.4))
  color_00 = (phase1, phase2, phase3)
  color_01 = (phase2, phase1, phase2)
  color_10 = (phase3, phase2, phase1)
  color_11 = (phase1, phase3, phase2)

  # strip.fill((0, 0, 0))
  # https://en.wikipedia.org/wiki/Bilinear_interpolation#On_the_unit_square
  for py in range(0, PIXEL_HEIGHT): # pixel x
    for px in range(0, PIXEL_WIDTH):
      color = [0,0,0]
      x = float(px) / PIXEL_WIDTH # x (0..1)
      y = float(py) / PIXEL_HEIGHT
      for ci in (0, 1, 2): # component index (0: red, 1: green, 2: blue)
        color[ci] = color_00[ci]*(1-x)*(1-y) + color_10[ci]*x*(1-y) + color_01[ci]*(1-x)*y + color_11[ci]*x*y
        color[ci] = int(255 * color[ci])
      strip.set_pixel((px, py), color)
  strip.show()
