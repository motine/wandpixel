# NOTE
# to run this, you need:
# python3 -m pip install --upgrade Pillow

from lib.engine import PIXEL_WIDTH, PIXEL_HEIGHT
from PIL import Image, ImageSequence

FPS = 5
image_frames = []
last_frame_index = 0

def init(strip, args):
  if not args:
    raise f"please specify an image"
  im = Image.open(args[0])

  for frame in ImageSequence.Iterator(im):
    frame = frame.copy()
    frame.thumbnail((PIXEL_WIDTH, PIXEL_HEIGHT), resample=Image.HAMMING) # modifies the Image object in place
    frame = frame.convert("RGB")
    image_frames.append(frame)

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
