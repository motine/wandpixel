#!/usr/bin/env python3

import importlib
import argparse
from pathlib import Path

USE_LED = Path("USE_LEDS").is_file()
DEFAULT_FPS = 30

# import the correct class (we do this a little awkwardly to avoid requiring dependencies if we are not using the actual LEDs)
import lib.engine
from lib.virtual_strip import VirtualStrip
if USE_LED:
  from lib.led_strip import LedStrip

parser = argparse.ArgumentParser()
parser.add_argument('script', type=str)
parser.add_argument('script_args', nargs='*')
parser.add_argument('--brightness', type=int, default=255)
args = parser.parse_args()

# SCRIPT_ARGS = args.script_args

if __name__ == "__main__":
  strip_class = LedStrip if USE_LED else VirtualStrip
  draw_module = importlib.import_module(f"scripts.{args.script}")
  fps = draw_module.FPS if hasattr(draw_module, 'FPS') else DEFAULT_FPS

  lib.engine.run(strip_class, draw_module.draw, fps, args.brightness)

