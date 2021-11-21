import rpi_ws281x
import csv
from .strip import Strip
from .engine import PIXEL_WIDTH, PIXEL_HEIGHT

class LedStrip(Strip):
  LED_COUNT      = 350     #  Number of LED pixels.
  LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
  LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
  LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
  LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
  LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
  LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

  def __init__(self):
    super(LedStrip, self).__init__()
    self.read_pixel_mapping()
    self.neopixel = rpi_ws281x.Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
    self.neopixel.begin()

  def read_pixel_mapping(self):
    self.pixel_mapping = {}
    with open('helper/pixel-arrangement.csv', newline='') as f:
      reader = csv.reader(f, delimiter=';')
      for y, row in enumerate(reader):
        for x, cell in enumerate(row):
          if (cell):
            self.pixel_mapping[y*PIXEL_WIDTH + x] = int(cell)

  def set_pixel(self, coordinate_or_index, color):
    if (isinstance(coordinate_or_index, tuple) or isinstance(coordinate_or_index, list)):
      self.set_pixel(coordinate_or_index[1]*PIXEL_WIDTH + coordinate_or_index[0], color)
      return
    if (isinstance(coordinate_or_index, int)):
      index = coordinate_or_index
      if not index in self.pixel_mapping:
        return # this is a dead pixel, so we ignore it (e.g. one in the top-right corner)
      real_index = self.pixel_mapping[index]
      self.neopixel.setPixelColor(real_index, rpi_ws281x.Color(*color))
      return

    raise TypeError # no idea what to do with coordinate_or_index

  def show(self):
    self.neopixel.show()
