from lib.engine import PIXEL_WIDTH, PIXEL_HEIGHT
from PIL import Image

# to run this, you need:
# python3 -m pip install --upgrade Pillow

FPS = 5 # TODO use 0.2
IMAGE_PATH = 'images/mario.png'
IMAGE_PATH = 'images/mario.gif'
# IMAGE_PATH = 'images/fire.gif'

im = Image.open(IMAGE_PATH)

from PIL import ImageSequence

image_frames = []
for frame in ImageSequence.Iterator(im):
  frame = frame.copy()
  frame.thumbnail((PIXEL_WIDTH, PIXEL_HEIGHT), resample=Image.HAMMING) # modifies the Image object in place
  frame = frame.convert("RGB")
  image_frames.append(frame)

last_frame_index = 0

def draw(strip):
  global image_frames, last_frame_index
  
  # animation
  current_frame_index = (last_frame_index + 1) % len(image_frames)
  frame = image_frames[current_frame_index]

  # draw
  strip.fill((0, 0, 0))
  for i, (r, g, b) in enumerate(frame.getdata()):
    strip.set_pixel(i, (r, g, b))

  last_frame_index = current_frame_index
  strip.show()
