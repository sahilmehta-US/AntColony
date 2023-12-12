import numpy as np

x = 0
y = 1

def create_locations(grid_size):
    n_rows = grid_size[0]
    n_cols = grid_size[1]
    locations = np.zeros((n_rows * n_cols, 2))
    count = 0
    for r in range(n_rows):
        for c in range(n_cols):
            locations[count] = np.array([r, c])
            count += 1
    return locations


def create_adjacency_mat(locations):
    adjacency_mat = np.zeros((locations.shape[0], locations.shape[0]))
    for i in range(locations.shape[0]):
        adjacency_mat[i] = get_adjacent(locations[i], locations)
    return adjacency_mat


def get_adjacent(position, all_locations):
    adjacent = np.ones(all_locations.shape[0])
    for j in range(all_locations.shape[0]):
        position_compare = all_locations[j]
        if position[0] == position_compare[0] and position[1] == position_compare[1]:  # one can't go to the position one is at
            adjacent[j] = 0
        if ((abs(position[x] - position_compare[x]) >= 2) or (
                abs(position[y] - position_compare[y]) >= 2)):
            # can't go to coordinate which with ones current location
            # coordinates' difference is equal to or greater than 2
            adjacent[j] = 0
    return adjacent


#locations = np.load('data/location10x10_maze1.npy')
#adjacency_mat = create_adjacency_mat(locations)

# np.save('data/adjacency_mat10x10_maze1.npy', adjacency_mat)