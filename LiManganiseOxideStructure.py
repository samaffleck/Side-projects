import numpy as np
import matplotlib.pyplot as plt

# This is the lattice parameter
lattice_scalar = 1

# Arrays are structured as [z][y][x]
# E.G. [1, 0, 0] represents the unit vector in the z-axis
basis = np.array([[1.0, 0.0, 0.0],
                  [0.0, 1.0, 0.0],
                  [0.0, 0.0, 1.0]])*lattice_scalar

# Relative positions of each Lithium atom in a unit cell
unit_cell = np.array([[0.0, 0.0, 0.0],  # 1. Origin
                      [0.5, 0.5, 0.0],  # 2. ZY-plane face centred point
                      [0.0, 0.5, 0.5],  # 3. XY-plane face centred point
                      [0.5, 0.0, 0.5],  # 4. XY-plane face centred point
                      [0.25, 0.25, 0.25],  # 5
                      [0.75, 0.75, 0.25],  # 6
                      [0.25, 0.75, 0.75],  # 7
                      [0.75, 0.25, 0.75]])*lattice_scalar  # 8

length_of_system = 5  # This is the length (s) of the side. So for a cube there are s^3 cells
# NOTE: Matplot lib strugles to plot the points when s > 5. 

grid = []
for z in range(length_of_system):
    for y in range(length_of_system):
        for x in range(length_of_system):
            base_position = np.array([z, y, x])  # Index of each unit cell
            cartesian_position = np.inner(basis.T, base_position)  # Origin of each unit cell
            grid.append(cartesian_position + unit_cell)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

colours = ['r', 'b', 'g']
i = -1
for cell in grid:
    if i < len(colours)-1:
        i += 1
    else:
        i = 0
    for atom in cell:
        colour = colours[i]
        ax.scatter(atom[2], atom[1], atom[0], c=colour)

plt.show()
