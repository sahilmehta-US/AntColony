from AntColony import AntColony
import numpy as np
from matplotlib import pyplot as plt
import seaborn


def get_files(filename_tail):
    locations = np.load(
        'data/location' + filename_tail + '.npy')  # np.load: returns arrays stored in this file
    adjacency_mat = np.load('data/adjacency_mat' + filename_tail + '.npy')
    return locations, adjacency_mat


def run_simulation(locations, adjacency_mat):
    colony = AntColony(locations, adjacency_mat, 0, locations.shape[0] - 1,
                       timesteps=1000, decay=0.001, n_ants=200)
    colony.run()
    print(colony.best_path)
    print(colony.best_path_dist)

    return colony


def plot(colony, all_paths=False):
    plt.title("THE Best Path")

    if all_paths:
        for path in colony.all_finished_paths:
            plt.plot(colony.locations[:, 0][path],
                     colony.locations[:, 1][path])
            plt.scatter(colony.locations[:, 0][path],
                        colony.locations[:, 1][path])
        plt.title("All Paths")

    plt.plot(colony.locations[:, 0][colony.best_path],
             colony.locations[:, 1][colony.best_path])
    plt.scatter(colony.locations[:, 0][colony.best_path],
                colony.locations[:, 1][colony.best_path])
    plt.gca().invert_yaxis()
    plt.show()


def plot_pheromones(colony):
    p = np.copy(colony.pheromones)
    p[0][0] = 0
    p_norm = (p - np.min(p)) / (np.max(p) - np.min(p))
    seaborn.heatmap(p_norm)
    plt.show()


def plot_pheromones_on_graph(colony, grid_size):
    p = np.copy(colony.pheromones)
    for i in range(p.shape[0]):
        p[i][i] = 0
    pheromones = np.zeros(colony.locations.shape)
    for i in range(colony.locations.shape[0]):
        pheromones[i] = np.sum(p[i])
    p_grid = np.zeros(grid_size)
    for l in range(pheromones.shape[0]):
        loc = colony.locations[l]
        p_grid[int(loc[0])][int(loc[1])] = pheromones[l][0]
    seaborn.heatmap(p_grid)
    plt.title("Pheromone matrix")
    plt.show()


filename_tail = '10x10_maze1'
locations, adj_mat = get_files(filename_tail)
colony = run_simulation(locations, adj_mat)
plot(colony, all_paths=False)
plot_pheromones_on_graph(colony, (10, 10))
