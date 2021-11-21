from lib.engine import PIXEL_WIDTH, PIXEL_HEIGHT
import random

FPS = 10

BG_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 0, 255)
FRUIT_COLOR = (255, 0, 0)
FRUIT_COUNT = 20

DIRECTION_CHOICES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

snake = [] # coordinates starting in the front of the snake, to the end
fruits = []
direction = (-1, 0)

def restart():
  global snake, fruits, direction
  snake = [(5,10), (6,10), (7,10)] # coordinates starting in the front of the snake, to the end
  fruits = []
  direction = (-1, 0)

def fade_color(original, factor):
  return (
    int(original[0] * factor),
    int(original[1] * factor),
    int(original[2] * factor)
  )

restart()

def draw(strip):
  global snake, fruits, direction

  # fill background
  strip.fill(BG_COLOR)
  # draw snake
  for i, (x, y) in enumerate(snake):
    color = fade_color(SNAKE_COLOR, 0.5 + (float(len(snake) - i)/(len(snake))) * 0.5 )
    strip.set_pixel((x, y), color)
  # draw fruits
  for x, y in fruits:
    strip.set_pixel((x, y), FRUIT_COLOR)

  # move snake
  head = snake[0]
  removed_snake_end = snake[-1]
  next_coord = ( (head[0] + direction[0]) % PIXEL_WIDTH, (head[1] + direction[1]) % PIXEL_HEIGHT )
  snake = [next_coord, *snake[:-1]] # insert next position and drop the last

  # change direction every once in a while
  if random.randrange(10) == 0:
    choices = set(DIRECTION_CHOICES) - set([direction, (-direction[0], -direction[1])]) # we must remove going back
    direction = random.choice(list(choices))

  # eat fruit
  head = snake[0]
  if head in fruits:
    fruits.remove(head)
    snake.append(removed_snake_end) # extend snake

  # collision detection
  head = snake[0]
  if head in snake[1:]:
    restart()

  # (re-)populate fruits
  while len(fruits) < FRUIT_COUNT:
    fruit_coord = (random.randrange(PIXEL_WIDTH), random.randrange(PIXEL_HEIGHT))
    if not fruit_coord in snake and not fruit_coord in fruits:
      fruits.append(fruit_coord)

  strip.show()
