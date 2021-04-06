# This simulation takes a qrid of length n by n and randomly initiates a temperature to each node.
# Over incremental time steps, each node will tend to the average value of the 4 nodes closest to it.
# The simulations stops once a global temperature difference is below a tolerance.


import random
import pygame
import time

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)


class Node:
    def __init__(self):
        self.temperature = random.randint(0, 255)  # [K]


def animation(matrix, n, time):
    # Initialise variables
    atom_size = 10  # Radius
    w = 600
    h = 600
    spacing = atom_size*4  # 1 Diameter spacing
    padding = (w - (n*atom_size*2 + (n-1)*(spacing-(2*atom_size))))/2

    highest_temp = 0
    lowest_temp = 255

    pygame.init()
    game_display = pygame.display.set_mode((w, h))
    game_display.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Draw nodes
    for y in range(n):
        for x in range(n):
            if matrix[0][y][x].temperature > 100:
                colour = (matrix[0][y][x].temperature, 0, 0)
            else:
                colour = (0, 0, 255-matrix[0][y][x].temperature)

            if matrix[0][y][x].temperature > highest_temp:
                highest_temp = matrix[0][y][x].temperature
            elif matrix[0][y][x].temperature < lowest_temp:
                lowest_temp = matrix[0][y][x].temperature

            pygame.draw.circle(game_display, colour, (padding + x*spacing, padding + y*spacing), atom_size)
            my_font = pygame.font.SysFont('arial', 12)
            temp_int = int(matrix[0][y][x].temperature)
            text_surface = my_font.render(str(temp_int), False, white)
            game_display.blit(text_surface, (padding + x*spacing - 8, padding + y*spacing - 8))

    # Print time
    my_font = pygame.font.SysFont('arial', 15)
    text_surface = my_font.render('Time: ' + str(time), False, white)
    game_display.blit(text_surface, (w/2, 10))

    if highest_temp - lowest_temp < 10:
        # We have reached thermal equilibrium and stop
        pygame.quit()
        quit()


def main():
    # Define an empty cube matrix of order n.
    # matrix[z][y][x].
    n = 5
    matrix = [[[Node() for x in range(n)] for x in range(n)] for x in range(n)]
    t = 0
    time_step = 1

    animation(matrix, n, t)

    # Running window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            animation(matrix, n, t)
            pygame.display.update()
            time.sleep(time_step)
            matrix = update_nodes(matrix, n)
            t += time_step

        pygame.display.update()


def update_nodes(matrix, n):
    # Create a copy of matrix which will store temperature at t = t + dt
    # Loop through every node in the matrix [z=0]
    # for each node calculate the average surrounding temperature and use that with the the current node temperature
    # to calculate the new note temperature at t = t + dt. Return the new matrix.

    matrix2 = [[[Node() for x in range(n)] for x in range(n)] for x in range(n)]

    for y in range(n):
        for x in range(n):
            cumulative_temp = 0
            nodes_checked = 0
            # Check for boundaries
            if x == 0:
                if y == 0:
                    cumulative_temp = matrix[0][y][x + 1].temperature + matrix[0][y + 1][x].temperature
                    nodes_checked = 2
                elif y == n - 1:
                    cumulative_temp = matrix[0][y][x + 1].temperature + matrix[0][y - 1][x].temperature
                    nodes_checked = 2
                else:
                    cumulative_temp = matrix[0][y][x + 1].temperature + matrix[0][y - 1][x].temperature + \
                                      matrix[0][y + 1][x].temperature
                    nodes_checked = 3
            elif x == n - 1:
                if y == 0:
                    cumulative_temp = matrix[0][y][x - 1].temperature + matrix[0][y + 1][x].temperature
                    nodes_checked = 2
                elif y == n - 1:
                    cumulative_temp = matrix[0][y][x - 1].temperature + matrix[0][y - 1][x].temperature
                    nodes_checked = 2
                else:
                    cumulative_temp = matrix[0][y][x - 1].temperature + matrix[0][y - 1][x].temperature + \
                                      matrix[0][y + 1][x].temperature
                    nodes_checked = 3
            elif y == 0:
                cumulative_temp = matrix[0][y][x - 1].temperature + matrix[0][y][x + 1].temperature + \
                                  matrix[0][y + 1][x].temperature
                nodes_checked = 3
            elif y == n - 1:
                cumulative_temp = matrix[0][y][x - 1].temperature + matrix[0][y][x + 1].temperature + \
                                  matrix[0][y - 1][x].temperature
                nodes_checked = 3
            else:
                # Node is central node
                cumulative_temp = matrix[0][y][x + 1].temperature + matrix[0][y][x - 1].temperature + \
                                    matrix[0][y + 1][x].temperature + matrix[0][y - 1][x].temperature
                nodes_checked = 4

            average_temperature = cumulative_temp/nodes_checked
            average_average_temperature = (average_temperature + matrix[0][y][x].temperature)/2

            matrix2[0][y][x].temperature = average_average_temperature

    return matrix2


if __name__ == '__main__':
    main()
