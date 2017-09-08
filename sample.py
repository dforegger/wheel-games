import numpy as np
import random
import time

from collections import namedtuple, deque

import curses
import sys

"""
total_spokes=4  #
spoke_length=2

spokes = [[(0,0,0)]*spoke_length]*total_spokes
print spokes

spoke
"""

W,H = 10,5
grid = np.zeros((H,W), dtype=np.ubyte)

Point = namedtuple("Point", ["x","y"]) # Eventually will become spoke/out or something like that
CENTER_POINT = Point(-1, -1)  # Special point

def play_game():
    try:
        # TODO - use curses.wrapper
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)

        window = curses.newwin
        game = Snek(stdscr)
        while True:
            game.next_frame()
            time.sleep(1.0/15)

    finally:
        curses.nocbreak(); stdscr.keypad(0); curses.echo()
        curses.endwin()

class Snek(object):
    UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3

    def __init__(self, screen=None, width=10, height=5):
        self.screen = screen
        self.width = width
        self.height = height
        self.grid = np.zeros((H,W), dtype=np.ubyte)
        self.direction = None
        self.queue = deque()

        self.reset()

    def reset(self):
        self.grid[:] = 0
        self.direction = Snek.RIGHT
        queue = deque()

        tail = Point(x=random.randrange(self.width), y=random.randrange(self.height))
        queue.append(tail)
        for _ in range(2):
            tail = self.get_next(tail, self.direction)
            queue.append(tail)
        self.queue = queue
        self.update_grid()

    def next_frame(self):
        next_point = self.get_next(self.queue[-1], self.direction)
        assert next_point.y < self.height, "Moved off the top. Ya loseah"
        last_point = self.queue.popleft() # Pop now so we can chase ourselves
        assert not next_point in self.queue, "Moved into yo'self."

        self.queue.append(next_point)
        self.update_grid(last_point=last_point)
        self.draw_grid()

    def update_grid(self, last_point=None):
        if last_point:  # Incremental
            self.grid[last_point.y,last_point.x] = 0
            self.grid[self.queue[-1].y,self.queue[-1].x] = 1  # TODO: Optimize
        else:  # Not incremental
            zipped = zip(*self.queue)
            self.grid[zipped[1], zipped[0]] = 1

    def draw_grid(self):
        self.screen.addstr(str(self.grid))
        self.screen.refresh()


    @staticmethod
    def get_next(head, direction):
        #TODO: Centerpoint Wraparound with disabled movement

        if direction == Snek.UP:
            # TODO error if y is too big now
            return Point(head.x, head.y+1)
        elif direction == Snek.RIGHT:
            return Point((head.x+1)%W, head.y)
        elif direction == Snek.LEFT:
            return Point((head.x-1)%W, head.y)
        elif direction == Snek.DOWN:
            if head.y == 0:
                return CENTER_POINT
            else:
                return Point(head.x, head.y-1)

if __name__ == '__main__':
    play_game()