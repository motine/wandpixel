from engine import PIXEL_WIDTH, PIXEL_HEIGHT
flakes = [(1, 8.0), (5, 0.0)] # column, top

def draw(strip):
  global flakes
  # move flakes
  flakes = [(col, (top+0.1) % PIXEL_HEIGHT) for col, top in flakes]

  # fill background
  for y in range(PIXEL_HEIGHT):
    for x in range(PIXEL_WIDTH):
      strip.setPixel(x, y, (30, 0, 0))
  # draw flakes
  for col, top in flakes:
    top_int = int(top)
    decimals = top - top_int
    color_value_upper = int(decimals * 255)
    color_value_lower = int((1-decimals) * 255)
    strip.setPixel(col, top_int, (color_value_lower, color_value_lower, color_value_lower))
    if top_int+1 < PIXEL_HEIGHT:
      strip.setPixel(col, top_int+1, (color_value_upper, color_value_upper, color_value_upper))

  strip.show()
