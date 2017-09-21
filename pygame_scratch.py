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

ROWS = 7
COLUMNS = 13

# This sets the width and height of each grid location
width  = 20
height = 20

# This sets the margin between each cell
margin = 5

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = np.zeros((ROWS, COLUMNS))

# Set row 1, cell 5 to one.
# Current position
x_coord = random.randrange(COLUMNS)
y_coord = random.randrange(ROWS)
grid[y_coord][x_coord] = 1
print grid


# Set the width and height of the screen [width,height]
size = [COLUMNS*(width+margin)+margin, ROWS*(height+margin)+margin]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Pygame Scratch")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(0)

# -------- Main Program Loop -----------
while not done:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            # User pressed down on a key

        elif event.type == pygame.KEYUP:
            grid[y_coord][x_coord] = 0

            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                x_coord = (x_coord - 1) % COLUMNS
            elif event.key == pygame.K_RIGHT:
                x_coord = (x_coord + 1) % COLUMNS
            elif event.key == pygame.K_UP:
                y_coord = (y_coord - 1) % ROWS
            elif event.key == pygame.K_DOWN:
                y_coord = (y_coord + 1) % ROWS

            grid[y_coord][x_coord]=1

    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT


    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT

    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)

    # Draw the grid
    for row in range(ROWS):
        for column in range(COLUMNS):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(margin+width)*column+margin,
                              (margin+height)*row+margin,
                              width,
                              height])

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(60)

def main():
    # Setup
    pygame.init()

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()

if __name__ == "__main__":
    main()