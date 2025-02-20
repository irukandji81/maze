from cell import Cell
import random
import time

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j, with_delay=True):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate(with_delay=with_delay)  # Apply delay based on the parameter

    def _animate(self, with_delay=True):
        if self._win is None:
            return
        self._win.redraw()
        if with_delay:
            time.sleep(0.025)  # Apply delay only if with_delay is True

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            # if there is nowhere to go from here
            # just break out
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            elif next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            elif next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            elif next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        self.solution_path = []
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        self.solution_path.append((i, j))

        # If we are at the end cell, return True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # Try each direction
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self._num_cols and 0 <= nj < self._num_rows:
                if not self._cells[ni][nj].visited:
                    if (di == -1 and not self._cells[i][j].has_left_wall) or \
                       (di == 1 and not self._cells[i][j].has_right_wall) or \
                       (dj == -1 and not self._cells[i][j].has_top_wall) or \
                       (dj == 1 and not self._cells[i][j].has_bottom_wall):
                        self._cells[i][j].draw_move(self._cells[ni][nj])
                        if self._solve_r(ni, nj):
                            return True
                        self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)
                        self.solution_path.pop()

        return False
        
    def clear_path(self):
        # Clear the canvas
        self._win.clear_canvas()

        # Redraw the maze without the grey lines
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j, with_delay=False)  # Redraw instantly

        # Redraw the successful path
        for k in range(len(self.solution_path) - 1):
            i, j = self.solution_path[k]
            ni, nj = self.solution_path[k + 1]
            self._cells[i][j].draw_move(self._cells[ni][nj])

        self._win.redraw()  # Ensure the redraw happens immediately
    
    def new_maze(self):
        # Clear the canvas
        self._win.clear_canvas()

        # Reset the cells and solution path
        self._cells = []
        self.solution_path = []

        # Create a new maze
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self._win.redraw()