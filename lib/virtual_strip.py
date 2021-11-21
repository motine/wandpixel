import pygame
from .strip import Strip
from .engine import PIXEL_WIDTH, PIXEL_HEIGHT

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