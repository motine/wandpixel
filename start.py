#!/usr/bin/env python3

import sys
import importlib
from pathlib import Path

USE_LED = Path("USE_LEDS").is_file()
DEFAULT_FPS = 30

import lib.engine
from lib.virtual_strip import VirtualStrip
if USE_LED:
  from lib.led_strip import LedStrip

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print('please specify a script')
    sys.exit(1)

  strip_class = LedStrip if USE_LED else VirtualStrip
  draw_module = importlib.import_module(sys.argv[1])
  fps = draw_module.FPS if hasattr(draw_module, 'FPS') else DEFAULT_FPS

  lib.engine.run(strip_class, draw_module.draw, fps)

