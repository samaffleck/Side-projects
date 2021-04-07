# This simulation uses the bragg-williams model to calculate the entropy and partial derivative of molar enthalpy w/ respect to the volume fraction of Li ions (gold).

import random
import pygame
import math
import time
import matplotlib.pyplot as plt

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
gold = (255, 215, 0)


class Node:
    def __init__(self, z_pos, y_pos, x_pos, p):
        self.temperature = 298  # [K]
        self.pressure = 101  # [kPa]
        self.enthalpy = 0  # [J]
        self.entropy = 0  # [J/K]
        self.neighbours = []
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos

        rand_probability = random.random()
        if rand_probability < p:
            self.colour = gold  # Gold is Li ion
        else:
            self.colour = blue  # Blue is C atom

    def get_nearest_neighbours(self, matrix, n):
        self.neighbours = []
        if self.x_pos < n - 1:
            self.neighbours.append(matrix[self.z_pos][self.y_pos][self.x_pos + 1])  # Check Right

        if self.x_pos > 0:
            self.neighbours.append(matrix[self.z_pos][self.y_pos][self.x_pos - 1])  # Check Left

        if self.y_pos < n - 1:
            self.neighbours.append(matrix[self.z_pos][self.y_pos + 1][self.x_pos])  # Check Down

        if self.y_pos > 0:
            self.neighbours.append(matrix[self.z_pos][self.y_pos - 1][self.x_pos])  # Check Up

        if self.z_pos < n - 1:
            self.neighbours.append(matrix[self.z_pos + 1][self.y_pos][self.x_pos])  # Check Forwards

        if self.z_pos > 0:
            self.neighbours.append(matrix[self.z_pos - 1][self.y_pos][self.x_pos])  # Check Backwards


def get_volume_fraction(matrix, n):
    n0 = n ** 3  # Total number of nodes
    n1 = 0  # Li (gold) is 1 and C (blue) is 2
    n2 = 0
    for z in range(n):
        for y in range(n):
            for x in range(n):
                if matrix[z][y][x].colour == gold:
                    n1 += 1
                else:
                    n2 += 1

    vol_fraction_li = n1 / n0
    vol_fraction_c = n2 / n0

    return vol_fraction_li, vol_fraction_c, n0, n1, n2


def animation(matrix, n, entropy_list):
    # Initialise variables
    li_size = 6  # Radius
    o_size = 3
    w = 600
    h = 600
    spacing = li_size * 4  # 1 Diameter spacing
    padding = (w - (n * li_size * 2 + (n - 1) * (spacing - (2 * li_size)))) / 2
    z = 0  # This is the layer we are looking at on the z-axis

    pygame.init()
    game_display = pygame.display.set_mode((w, h))
    game_display.fill(black)

    # Draw nodes
    for y in range(n):
        for x in range(n):
            pygame.draw.circle(game_display, matrix[z][y][x].colour, (padding + x * spacing, padding + y * spacing),
                               li_size)

    # Return entropy parameters
    vol_fraction_li, vol_fraction_c, n0, n1, n2 = get_volume_fraction(matrix, n)
    kb = 1.38  # Boltzmann constant
    try:
        total_entropy = kb * (-n1 * math.log(vol_fraction_li, math.e) - n2 * math.log(vol_fraction_c, math.e))
        entropy_list.append((vol_fraction_li, total_entropy))
    except Exception as e:
        print("Total Entropy could not be calculated due to:", e)

    return entropy_list


def main():
    # Define an empty cube matrix of order n.
    # matrix[z][y][x].
    n = 20
    p = 0.0  # Start probability of a Li ion
    t = 0
    dt = 0.05
    dp = 0.02
    entropy_list = []

    matrix = [[[Node(z, y, x, p) for z in range(n)] for y in range(n)] for x in range(n)]

    animation(matrix, n, entropy_list)

    running = True
    # Running window
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if p >= 1:
            running = False

        p += dp
        t += dt
        matrix = [[[Node(z, y, x, p) for z in range(n)] for y in range(n)] for x in range(n)]
        entropy_list = animation(matrix, n, entropy_list)
        pygame.display.update()
        time.sleep(dt)

    i = 0
    gradients = []
    for x, s in entropy_list:
        if i == 0:
            x_old = x
            s_old = s
        else:
            m = (s-s_old)/(x-x_old)
            gradients.append((x, m))
            x_old = x
            s_old = s
        i += 1

    fig, axs = plt.subplots(2)
    axs[0].scatter(*zip(*gradients))
    axs[0].set_title('Voltage profile')
    axs[1].scatter(*zip(*entropy_list))
    axs[1].set_title('Entropy plot')
    plt.show()


if __name__ == '__main__':
    main()
