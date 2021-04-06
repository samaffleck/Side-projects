import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np

GREY = (0.78, 0.78, 0.78)  # uninfected
RED = (0.96, 0.15, 0.15)  # infected
GREEN = (0, 0.86, 0.03)  # recovered
BLACK = (0, 0, 0)  # dead


class Culture():

    def __init__(self):
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(111, projection="polar")
        self.axes.grid(False)
        self.axes.set_xticklabels([])
        self.axes.set_yticklabels([])
        self.axes.set_ylim(0, 1)

        '''Lable the figure'''
        self.cells_text = self.axes.annotate(
            "Number of cells: 0", xy=[np.pi / 2, 1], ha="center", va="bottom")
        self.time_text = self.axes.annotate(
            "Time: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=RED)

        '''Init variables'''
        self.curr_no_cells = 0
        self.max_no_cells = 1000
        self.time = 0
        self.active_thetas = []
        self.active_rs = []

        self.cell_density = 0.01  # 1 cell = 0.01 g/L

        self.substrate_concentration = 5  # g/L
        self.cell_concentration = 0.01  # g/L: 1 cell at the start
        self.mu_max = 0.1
        self.ks = 0.5

        self.initial_population()

    def initial_population(self):
        population = self.max_no_cells
        self.curr_no_cells = 1
        indices = np.arange(0, population) + 0.5
        self.thetas = np.pi * (1 + 5**0.5) * indices
        self.rs = np.sqrt(indices / population)
        self.plot = self.axes.scatter(self.thetas, self.rs, s=5, color=GREY)

        #first cells
        for i in range(self.curr_no_cells):
            self.axes.scatter(self.thetas[i], self.rs[i], s=5, color=RED)

    def spread(self, i):
        self.growth_rate = (self.mu_max*self.cell_concentration*self.substrate_concentration)/\
                           (self.ks + self.substrate_concentration)

        # In each time period of 1, cell concentration += rate and substrate concentration -= rate
        self.cell_concentration += self.growth_rate
        self.substrate_concentration -= self.growth_rate

        self.curr_no_cells = round(self.cell_concentration/self.cell_density)

        print(self.curr_no_cells, self.cell_concentration, self.substrate_concentration, self.growth_rate, self.time)

        self.time += 1
        self.active_thetas = []
        self.active_rs = []

        for i in range(self.curr_no_cells):
            self.active_thetas.append(self.thetas[i])
            self.active_rs.append(self.rs[i])

        self.update_text()
        self.update_status()

    def update_status(self):
        self.axes.scatter(self.active_thetas, self.active_rs, s=5, color=RED)

    def update_text(self):
        self.time_text.set_text("Time: {}".format(self.time))
        self.cells_text.set_text("Number of Cells: {}".format(self.curr_no_cells))

    def gen(self):
        while self.curr_no_cells < self.max_no_cells:
            yield

    def animate(self):
        self.anim = ani.FuncAnimation(
            self.fig,
            self.spread,
            frames=self.gen,
            repeat=True)

def main():
    test1 = Culture()
    test1.animate()
    plt.show()


if __name__ == '__main__':
    main()

