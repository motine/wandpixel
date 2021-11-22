import pygame # we use pygame drawing in a window _and_ running with the right FPS

PIXEL_WIDTH = 14
PIXEL_HEIGHT = 25

def run(strip_class, draw_method, init_method, fps, brightness, script_args):
  strip = strip_class(brightness)
  fps_clock = pygame.time.Clock()

  if init_method:
    init_method(strip, script_args)

  try:
    while True:
      strip.do_loop()
      draw_method(strip)
      fps_clock.tick(fps)
  except KeyboardInterrupt:
    pass
  finally:
    strip.quit()
