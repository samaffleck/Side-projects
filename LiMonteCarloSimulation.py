import numpy as np
import random


class Atoms:
    """Atoms class contains the object of a primitive cell - 2 Li atoms offset by (0.25, 0.25, 0.25)"""

    def __init__(self, x_index, y_index, z_index):
        self.x_index = x_index
        self.y_index = y_index
        self.z_index = z_index

        self.c1 = 1  # The occupation number of sub lattice 1, c = 1 is a Lithium atom c = 0 is a vacant site.
        self.c2 = 1  # The occupation number of sub lattice 2
        self.vectors = np.array([[0.5, 0.5, 0.0], [0.5, 0.0, 0.5], [0.0, 0.5, 0.5]])
        self.offset_vector = np.array([0.25, 0.25, 0.25])
        self.temp_neighbours = []

    def get_position(self):
        """Gets the cartesian coordinates for the two Lithium atoms in the primitive cell"""
        if (self.z_index + self.y_index) % 2 != 0:
            x_offset = 0.5
        else:
            x_offset = 0

        self.position_1 = np.array([self.x_index + x_offset, self.y_index * 0.5, self.z_index * 0.5])
        self.position_2 = self.position_1 + self.offset_vector

        print(self.position_1, self.position_2, 'x_index: ', self.x_index, 'y_index: ', self.y_index, 'z_index: ', self.z_index)

    def get_nn(self, grid, sublattice_1):
        self.temp_neighbours = []

        # Neighbouring sub-lattices

        try:
            if sublattice_1:
                if self.x_index % 2 == 0:
                    self.temp_neighbours.append(grid[self.x_index-1][self.y_index][self.z_index-1])
                    self.temp_neighbours.append(grid[self.x_index][self.y_index-1][self.z_index-1])
                    self.temp_neighbours.append(grid[self.x_index-1][self.y_index-1][self.z_index])
                else:
                    self.temp_neighbours.append(grid[self.x_index][self.y_index][self.z_index-1])
                    self.temp_neighbours.append(grid[self.x_index-1][self.y_index-1][self.z_index])
                    self.temp_neighbours.append(grid[self.x_index][self.y_index-1][self.z_index-1])
            else:
                if self.x_index % 2 == 0:
                    self.temp_neighbours.append(grid[self.x_index][self.y_index][self.z_index + 1])
                    self.temp_neighbours.append(grid[self.x_index][self.y_index + 1][self.z_index])
                    self.temp_neighbours.append(grid[self.x_index][self.y_index + 1][self.z_index+1])
                else:
                    self.temp_neighbours.append(grid[self.x_index+1][self.y_index][self.z_index + 1])
                    self.temp_neighbours.append(grid[self.x_index][self.y_index + 1][self.z_index + 1])
                    self.temp_neighbours.append(grid[self.x_index+1][self.y_index + 1][self.z_index - 1])

        except Exception as e:
            print(e)

        self.neighbours = np.array(self.temp_neighbours)

    def get_nnn(self, grid):
        self.temp_neighbours = []

        try:
            if self.y_index % 2 == 0:
                self.temp_neighbours.append(grid[self.x_index-1][self.y_index-1][self.z_index])
                self.temp_neighbours.append(grid[self.x_index][self.y_index-1][self.z_index])
                self.temp_neighbours.append(grid[self.x_index][self.y_index+1][self.z_index])
                self.temp_neighbours.append(grid[self.x_index-1][self.y_index+1][self.z_index])

                self.temp_neighbours.append(grid[self.x_index][self.y_index-1][self.z_index+1])
                self.temp_neighbours.append(grid[self.x_index][self.y_index+1][self.z_index+1])
                self.temp_neighbours.append(grid[self.x_index+1][self.y_index][self.z_index+1])
                self.temp_neighbours.append(grid[self.x_index-1][self.y_index][self.z_index+1])

                self.temp_neighbours.append(grid[self.x_index][self.y_index - 1][self.z_index - 1])
                self.temp_neighbours.append(grid[self.x_index][self.y_index + 1][self.z_index - 1])
                self.temp_neighbours.append(grid[self.x_index + 1][self.y_index][self.z_index - 1])
                self.temp_neighbours.append(grid[self.x_index - 1][self.y_index][self.z_index - 1])
            else:
                self.temp_neighbours.append(grid[self.x_index][self.y_index - 1][self.z_index])
                self.temp_neighbours.append(grid[self.x_index][self.y_index + 1][self.z_index])
                self.temp_neighbours.append(grid[self.x_index+1][self.y_index - 1][self.z_index])
                self.temp_neighbours.append(grid[self.x_index + 1][self.y_index + 1][self.z_index])

                self.temp_neighbours.append(grid[self.x_index][self.y_index - 1][self.z_index + 1])
                self.temp_neighbours.append(grid[self.x_index][self.y_index + 1][self.z_index + 1])
                self.temp_neighbours.append(grid[self.x_index][self.y_index][self.z_index + 1])
                self.temp_neighbours.append(grid[self.x_index + 1][self.y_index][self.z_index + 1])

                self.temp_neighbours.append(grid[self.x_index][self.y_index - 1][self.z_index - 1])
                self.temp_neighbours.append(grid[self.x_index][self.y_index + 1][self.z_index - 1])
                self.temp_neighbours.append(grid[self.x_index + 1][self.y_index][self.z_index - 1])
                self.temp_neighbours.append(grid[self.x_index][self.y_index][self.z_index - 1])

        except Exception as e:
            print(e)

        self.nnn = np.array(self.temp_neighbours)


def monte_carlo(grid, grid_length):
    random_cell = grid[random.randint(0, (grid_length/2)-1)][random.randint(0, grid_length-1)][random.randint(0, grid_length-1)]  # Selects a random primitive cell
    random_lattice = random.choice([True, False])  # This swaps between the two atoms in the primitive cell

    print("The random atom is: ")
    random_cell.get_position()
    print("Is it in sub lattice 1? ", random_lattice)
    print()

    print("The neighbouring cells of which are:")
    random_cell.get_nn(grid, random_lattice)
    for neighbour in random_cell.neighbours:
        neighbour.get_position()


def get_grid(grid_length):
    """Get_grid() returns a 3 dimensional array of 'Atom' objects and is representative of the lattice structure."""
    grid = np.zeros((int(grid_length/2), grid_length, grid_length), dtype=Atoms)  # The 3 dimensional array that will store each primitive cell.

    for z in range(grid_length):
        for y in range(grid_length):
            for x in range(int(grid_length/2)):
                grid[x][y][z] = Atoms(x, y, z)

    return grid


if __name__ == '__main__':
    grid_length = 2  # This is the number of primitive unit cells containing 2 lithium atoms. MUST BE EVEN!
    grid = get_grid(grid_length)
    monte_carlo(grid, grid_length)
