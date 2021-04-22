import pygame
import random
import math


W = 600
win = pygame.display.set_mode((W, W))
pygame.display.set_caption("Ising model")
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

        p = random.random()
        if p < 0.5:
            self.colour = WHITE
            self.s = 1
        else:
            self.colour = BLACK
            self.s = -1

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1:  # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0:  # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1:  # Right
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.row > 0:  # Left
            self.neighbours.append(grid[self.row][self.col - 1])

    def get_spot_energy(self):
        neighbour_energy = 0
        for n in self.neighbours:
            neighbour_energy += n.s

        self.spot_energy = -self.s * neighbour_energy


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw(win, grid):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    pygame.display.update()


def monte_carlo(grid, rows, steps):
    temp = 1.5

    for i in range(steps):
        rand_spot_x = random.randrange(rows)
        rand_spot_y = random.randrange(rows)
        grid[rand_spot_y][rand_spot_x].update_neighbours(grid)
        grid[rand_spot_y][rand_spot_x].get_spot_energy()

        if grid[rand_spot_y][rand_spot_x].spot_energy > 0:
            grid[rand_spot_y][rand_spot_x].s *= -1
        elif grid[rand_spot_y][rand_spot_x].spot_energy < 0:
            p = random.random()
            if p < math.e**(2*grid[rand_spot_y][rand_spot_x].spot_energy/temp):
                grid[rand_spot_y][rand_spot_x].s *= -1

        if grid[rand_spot_y][rand_spot_x].s == 1:
            grid[rand_spot_y][rand_spot_x].colour = WHITE
        else:
            grid[rand_spot_y][rand_spot_x].colour = BLACK

    return grid


def main(win, width):
    ROWS = 100
    grid = make_grid(ROWS, width)
    total_steps = 0
    steps = 5000

    # Initialise neighbours

    run = True
    while run:
        draw(win, grid)
        grid = monte_carlo(grid, ROWS, steps)
        total_steps += steps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


if __name__ == '__main__':
    main(win, W)
