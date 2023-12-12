from tkinter import *
import numpy as np
import create_adj_m
import time
from AntColony import AntColony
from run_simulation import run_simulation
# careful when importing - make sure there aren't any lines of code that will run


class Cell:
    FILLED_COLOR_BG = "white"  # locations that can go to
    EMPTY_COLOR_BG = "black"  # walls
    FILLED_COLOR_BORDER = "black"
    EMPTY_COLOR_BORDER = "black"

    START_COLOR_BG = 'green'
    END_COLOR_BG = 'red'
    SOL_COLOR_BG = "green"
    SOL_COLOR_BORDER = "black"

    def __init__(self, master, x, y, size, start, end):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.fill = True
        self.start = start
        self.end = end

    def switch(self):
        """ Switch if the cell is filled or not. """
        self.fill = not self.fill

    def fill_solution(self):
        fill = Cell.SOL_COLOR_BG
        outline = Cell.SOL_COLOR_BORDER

        if self.abs == self.end[0] and self.ord == self.end[1]:
            fill = Cell.END_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER
        xmin = self.abs * self.size
        xmax = xmin + self.size
        ymin = self.ord * self.size
        ymax = ymin + self.size

        self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=fill,
                                     outline=outline)

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master is not None:
            fill = Cell.FILLED_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER
            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER
            if self.abs == self.start[0] and self.ord == self.start[1]:
                fill = Cell.START_COLOR_BG
                outline = Cell.FILLED_COLOR_BORDER
                self.fill = True
            elif self.abs == self.end[0] and self.ord == self.end[1]:
                fill = Cell.END_COLOR_BG
                outline = Cell.FILLED_COLOR_BORDER
                self.fill = True

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=fill,
                                         outline=outline)

        # print("xmin: " + str(xmin) + " ymin: " + str(ymin) + " xmax: " + str(xmax) + " ymax: " + str(ymax))


class CellGrid(Canvas):
    def __init__(self, master, rowNumber, columnNumber, cellSize, *args,
                 **kwargs):
        Canvas.__init__(self, master, width=cellSize * columnNumber,
                        height=cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize

        self.start = (0, 0)
        self.end = (rowNumber - 1, columnNumber - 1)

        self.grid = []
        for row in range(rowNumber):
            line = []
            for column in range(columnNumber):
                line.append(
                    Cell(self, column, row, cellSize, self.start, self.end))

            self.grid.append(line)

        self.best_path_arr = []

        # memorize the cells that have been modified to avoid many switching
        # of state during mouse motion.
        self.switched = []

        # bind click action
        self.bind("<Button-1>", self.handleMouseClick)
        # bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        # bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

        run_button = Button(self, text="Run Optimization",
                            command=self.run_sim, anchor=W)
        run_button.configure(width=10, activebackground="#33B5E5", relief=FLAT)
        self.create_window(10, 10, anchor=NW, window=run_button)

        self.draw()

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        cell.switch()
        cell.draw()
        # add the cell to the list of cell switched during the click
        self.switched.append(cell)

    def handleMouseMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            cell.switch()
            cell.draw()
            self.switched.append(cell)

    def run_sim_by_step(self, n_timesteps=100):
        locations = self.create_locations()
        adjacency_mat = create_adj_m.create_adjacency_mat(locations)
        colony = AntColony(locations, adjacency_mat, 0, locations.shape[0] - 1,
                           decay=0.1, n_ants=100)
        for t in range(n_timesteps):
            colony.run_time_step(t)
            if len(colony.best_path) > 0:
                self.draw()
                #  for loc in self.best_path_arr:
                #     self.grid[loc[0]][loc[1]].draw()
                #   self.best_path_arr = []
                for idx in colony.best_path:
                    loc = locations[idx]
                    self.grid[loc[0]][loc[1]].fill_solution()
                #  self.best_path_arr.append(loc)
            self.update()
       #     time.sleep(0.001)
        print(colony.best_path)
        print(colony.best_path_dist)
        print("finished")

    def create_locations(self):
        locations = []
        for i in range(len(grid.grid)):
            for j in range(len(grid.grid[i])):
                if grid.grid[i][j].fill:
                    locations.append([i, j])
        locations = np.array(locations)
        return locations

    def run_sim(self):
        self.draw()
        locations = self.create_locations()
        adj_mat = create_adj_m.create_adjacency_mat(locations)
        # need to pass in locations and adj matrix
        colony = run_simulation(locations, adj_mat)
        for idx in colony.best_path:
            loc = locations[idx]
            self.grid[loc[0]][loc[1]].fill_solution()
            self.best_path_arr.append(loc)



app = Tk()

nx = 10
ny = 10
cell_size = 50

grid = CellGrid(app, nx, ny, cell_size)
grid.pack()

app.mainloop()
