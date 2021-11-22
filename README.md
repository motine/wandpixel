# Wandpixel

The fun may begin. Let's write some nice animations for the wandpixel.

**Please open pull requests and add new draw scripts**

## Get started

```bash
# install the python3
# install pygame package
python3 -m pip install -U pygame --user

# now run the engine with the demo script
./start.py snowflake

# to start your own script:
cp snowflake.py yourscript.py
vim yourscript.py
# use strip's method set_pixel([x, y], color_triple) to set the color of a pixel
# make sure to call strip.show() at the end of the draw method
# the init(strip, args) method is optional
# if you want to override the number of frames per second, specify a constant called FPS in your script
./start.py yourscript
```

If you have the actual LED matrix as seen at Tom's house, please also run the following on the raspberry pi:

```bash
sudo apt install libsdl2-dev
sudo python3 -m pip install rpi_ws281x
touch USE_LEDS # if this file is present, we will not spin up a window, but rather use the actual matrix
sudo ./start.py snowflake
```


## Notes on Assembly

- [wiring as seen here](https://core-electronics.com.au/tutorials/ws2812-addressable-leds-raspberry-pi-quickstart-guide.html)
- [my raspberry pinout](https://www.etechnophiles.com/raspberry-pi-zero-gpio-pinout-specifications-programming-language/)
- [my logic converter](https://www.reichelt.de/de/de/entwicklerboards-ttl-logic-level-converter-3-3v-5v-debo-llc-3-3-5-p282702.html?PROVID=2788&gclid=CjwKCAiAp8iMBhAqEiwAJb94zyk37X1ipjVY39zC6SMttjr7QZZH0hxFD9Wy-gSgvogEei4ow7t56BoCSeQQAvD_BwE&&r=1) and its [data sheet](https://cdn-reichelt.de/documents/datenblatt/A300/ST1167.pdf)
- install as seen [here](https://core-electronics.com.au/tutorials/ws2812-addressable-leds-raspberry-pi-quickstart-guide.html)
- then install python package [rpi3-ws2812b](https://raw.githubusercontent.com/coreelectronics/scripts/master/rpi3-ws2812b) (maybe uninstall package and reinstall)
- follow instructions for PMW: https://github.com/jgarff/rpi_ws281x

