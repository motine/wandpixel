from .engine import PIXEL_WIDTH, PIXEL_HEIGHT

class Strip(object):
  def __init__(self, brightness):
    pass

  def do_loop(self):
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
  # if an int is given, it is considered from left to right, from top to bottom
  def set_pixel(self, coordinate_or_index, color):
    pass

  def show(self):
    pass
