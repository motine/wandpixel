# thanks Dario for sponsoring this!
from lib.engine import PIXEL_WIDTH, PIXEL_HEIGHT
import numpy as np

# this script needs numpy:
# python3 -m pip install --upgrade numpy

FPS = 6

def update(cur):
    nxt = np.zeros((cur.shape[0], cur.shape[1]))
    for r, c in np.ndindex(cur.shape):
        num_alive = np.sum(cur[r-1:r+2, c-1:c+2]) - cur[r, c]
        if (cur[r, c] == 1 and 2 <= num_alive <= 3) or (cur[r, c] == 0 and num_alive == 3):
            nxt[r, c] = 1
    return nxt

def generate():
  global old_grid, new_grid
  old_grid = np.random.randint(0,2,(PIXEL_WIDTH,PIXEL_HEIGHT), dtype='int');
  new_grid = old_grid

def draw_grid(strip, grd):
    for iy, ix in np.ndindex(grd.shape):
        if grd[iy, ix] == 1:
            color = (255, 255, 255)
        else:
            color = (0, 0, 0)
        strip.set_pixel((iy, ix), color)

def restart():
    generate()

def draw(strip):
    global old_grid, new_grid
    strip.fill((0, 0, 0))
    new_grid = update(old_grid)
    draw_grid(strip, new_grid)
    if np.array_equal(old_grid, new_grid):
        restart()
    old_grid = new_grid
    strip.show()

generate()
