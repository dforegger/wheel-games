import numpy as np
import random
import time

from collections import namedtuple, deque

import Tkinter as tk
from threading import Thread
import traceback


"""
total_spokes=4  #
spoke_length=2

spokes = [[(0,0,0)]*spoke_length]*total_spokes
print spokes

spoke
"""

Point = namedtuple("Point", ["x","y"]) # Eventually will become spoke/out or something like that
CENTER_POINT = Point(-1, -1)  # Special point

def keyboard_thread(app):
    keep_running = True
    wasd_keys = {
        'a' : SnekApp.LEFT,
        's' : SnekApp.DOWN,
        'd' : SnekApp.RIGHT,
        'w' : SnekApp.UP
    }
    while keep_running:
        try:
            key = raw_input("Send a keyboard command: ")
            if not key:
                continue
            elif ("quit" == key):
                # TODO: We should really use atexit for all this. This is
                # a short-term fix to not take down the simulator with us
                print "Received shutdown command. Exiting now"
                keep_running = False
                app.quit()
            elif key in wasd_keys:
                app.direction = wasd_keys[key]
        except:
            traceback.print_exc()

        time.sleep(.1)


def launch():
    root = tk.Tk()
    app = SnekApp(master=root)

    key_thread = Thread(target=keyboard_thread, args=(app,), name="KeyboardListeningThread")
    key_thread.setDaemon(True)
    key_thread.start()

    app.mainloop()
    root.destroy()


class SnekApp(tk.Frame):
    UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3

    def __init__(self, master=None, grid_width=20, grid_height=20):
        tk.Frame.__init__(self, master)
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid = np.zeros((grid_height,grid_width), dtype=np.ubyte)
        self.direction = None
        self.queue = deque()

        self.text = tk.StringVar()
        self.text.set(str(self.grid))
        self.grid_label = tk.Label(textvariable=self.text)
        self.grid_label.pack()
        self.playing = False

        self.reset()

    def reset(self):
        self.grid[:] = 0
        self.direction = SnekApp.RIGHT
        queue = deque()

        tail = Point(x=random.randrange(self.grid_width), y=random.randrange(self.grid_height))
        queue.append(tail)
        for _ in range(2):
            tail = self.get_next(tail, self.direction)
            queue.append(tail)
        self.queue = queue
        self.update_grid()

    def mainloop(self):
        frame_thread = Thread(target=self.play_game, args=(), name="FrameTimer")
        frame_thread.setDaemon(True)
        frame_thread.start()

        print "Calling main loop now"
        tk.Frame.mainloop(self)


    def play_game(self):
        self.reset()
        self.playing = True
        while self.playing:
            self.next_frame()
            #TODO: sleep logic
            time.sleep(.25) #  4 FPS, for now

    def next_frame(self):
        next_point = self.get_next(self.queue[-1], self.direction)
        assert next_point.y < self.grid_height, "Moved off the top. Ya loseah"
        last_point = self.queue.popleft() # Pop now so we can chase ourselves
        assert not next_point in self.queue, "Moved into yo'self."

        self.queue.append(next_point)
        self.update_grid(last_point=last_point)
        self.draw_grid()

    def update_grid(self, last_point=None):
        if last_point:  # Incremental
            self.grid[last_point.y,last_point.x] = 0
            self.grid[self.queue[-2].y, self.queue[-2].x] = 1
            self.grid[self.queue[-1].y,self.queue[-1].x] = 2  # TODO: Optimize
        else:  # Not incremental
            zipped = zip(*self.queue)
            self.grid[zipped[1], zipped[0]] = 1 #  TODO: Remove from earlier
            self.grid[self.queue[-1].y, self.queue[-1].x] = 2

    def draw_grid(self):
        self.text.set(str(self.grid))

    def get_next(self, head, direction):
        #TODO: Centerpoint Wraparound with disabled movement

        if direction == SnekApp.UP:
            # TODO error if y is too big now
            return Point(head.x, (head.y+1) % self.grid_height)
        elif direction == SnekApp.RIGHT:
            return Point((head.x+1)%self.grid_width, head.y)
        elif direction == SnekApp.LEFT:
            return Point((head.x-1)%self.grid_width, head.y)
        elif direction == SnekApp.DOWN:
            if head.y == 0:
                return CENTER_POINT
            else:
                return Point(head.x, head.y-1)

if __name__ == '__main__':
    launch()