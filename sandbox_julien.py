import pygame
import time
from collections import deque

pygame.init()
screen = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

# just some colored squares for our animation
def get_cache(colors):
    tmp=[]
    for c in colors:
        s = pygame.surface.Surface((50,50))
        s.fill(pygame.color.Color(c))
        tmp.append(s)
    return tmp

walk_left, walk_right = get_cache(('red', 'yellow', 'blue')), get_cache(('black', 'white', 'grey'))

rect = walk_left[0].get_rect(top=100, right=100)
cachedeque = deque(walk_left)
state = None
quit = False

# a simple variable to keep track of time
timer = 0

# a dict of {key: (animation, direction)}
moves = {pygame.K_LEFT:  (walk_left,  (-2, 0)),
         pygame.K_RIGHT: (walk_right, ( 2, 0))}

while not quit:
    quit = pygame.event.get(pygame.QUIT)
    pygame.event.poll()

    # state of the keys
    pygame.key.set_repeat()
    keys = pygame.key.get_pressed()
    # print(keys)
    # filter for the keys we're interessted in
    pressed = ((key, _) for (key, _) in moves.items() if keys[key])
    key, (cache, dir) = next(pressed, (None, (None, None)))

    # if a key of the 'moves' dict is pressed:
    if key:
        # if we change the direction, we need another animation
        print(key)
        if state != key:
            cachedeque = deque(cache)
            state = key
        # move the square
        rect.move_ip(dir)
        a = 0
    else:
        state = None

    screen.fill(pygame.color.Color('green'))

    # display first image in cachedeque
    screen.blit(cachedeque[0], rect)

    # rotate cachedeque to the left, so the second image becomes the first
    # do this three times a second:
    # if state and timer >= 1000./3:
    #     cachedeque.rotate(-1)
    #     timer = 0

    # call flip() and tick() only once per frame
    pygame.display.flip()

    # keep track of how long it took to draw this frame
    timer += clock.tick(60)