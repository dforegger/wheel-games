# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/

import pygame
import numpy as np
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the width and height of each grid location
width = 20
height = 20

# This sets the margin between each cell
margin = 5


class Game(object):
    """ This class represents an instance of the game.
    The overhead is minimal enough that if we need to reset just create a new instance of this class"""

    #--- Class attributes
    # TODO


    def __init__(self, rows, columns):
        self.ROWS, self.COLUMNS = rows, columns
        # Create a 2 dimensional array. A two dimensional
        # array is simply a list of lists.
        self.grid = np.zeros((rows, columns))

        # Set row 1, cell 5 to one.
        # Current position
        self.x_coord = random.randrange(columns)
        self.y_coord = random.randrange(rows)
        self.grid[self.y_coord][self.x_coord] = 1

        self.game_over = False
        pass

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()
            elif event.type == pygame.KEYUP:
                self.grid[self.y_coord][self.x_coord] = 0

                # Figure out if it was an arrow key. If so
                # adjust speed.
                if event.key == pygame.K_LEFT:
                    self.x_coord = (self.x_coord - 1) % self.COLUMNS
                elif event.key == pygame.K_RIGHT:
                    self.x_coord = (self.x_coord + 1) % self.COLUMNS
                elif event.key == pygame.K_UP:
                    self.y_coord = (self.y_coord - 1) % self.ROWS
                elif event.key == pygame.K_DOWN:
                    self.y_coord = (self.y_coord + 1) % self.ROWS

                self.grid[self.y_coord][self.x_coord] = 1

        return False

    def run_logic(self):
        """
        This method is run each time through the frame.
        """
        pass

    def display_frame(self, screen):
        """ Render the game """


        if self.game_over:
            screen.fill(WHITE)
            pass
        else:
            screen.fill(BLACK)

            # Draw the grid
            for row in range(self.ROWS):
                for column in range(self.COLUMNS):
                    pygame.draw.rect(screen,
                                     GREEN if self.grid[row][column] == 1 else WHITE,
                                     [(margin + width) * column + margin,
                                      (margin + height) * row + margin,
                                      width,
                                      height])

        pygame.display.flip()

def main():
    # Setup
    pygame.init()

    ROWS = 7
    COLUMNS = 13

    # Set the width and height of the screen [width,height]
    size = [COLUMNS * (width + margin) + margin, ROWS * (height + margin) + margin]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Pygame Scratch")
    pygame.mouse.set_visible(False)

    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game(rows=ROWS, columns=COLUMNS)

    # Main game loop
    while not done:
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        # Update object positions, check for collisions
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(60)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()

if __name__ == "__main__":
    main()