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
        self.user_position = (0, 0)

    def move_user(self, direction):
        i, j = self.user_position
        if direction == "up" and j > 0 and not self._cells[i][j].has_top_wall:
            self._move_to(i, j - 1)
        elif direction == "down" and j < self._num_rows - 1 and not self._cells[i][j].has_bottom_wall:
            self._move_to(i, j + 1)
        elif direction == "left" and i > 0 and not self._cells[i][j].has_left_wall:
            self._move_to(i - 1, j)
        elif direction == "right" and i < self._num_cols - 1 and not self._cells[i][j].has_right_wall:
            self._move_to(i + 1, j)

    def _move_to(self, new_i, new_j):
        old_i, old_j = self.user_position
        self._cells[old_i][old_j].draw_move(self._cells[new_i][new_j])
        self.user_position = (new_i, new_j)
        self._animate()
        self._check_victory(new_i, new_j)

    def _check_victory(self, i, j):
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            self._win.show_victory_message()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j, with_delay=False)

    def _draw_cell(self, i, j, with_delay=True, fill_color=None, text=None):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2, fill_color, text)
        self._animate(with_delay=with_delay)

    def _animate(self, with_delay=True):
        if self._win is None:
            return
        self._win.redraw()
        if with_delay:
            time.sleep(0.015)

    def _break_entrance_and_exit(self):
        self._draw_cell(0, 0, fill_color="green", text="S")
        self._draw_cell(self._num_cols - 1, self._num_rows - 1, fill_color="red", text="E")

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            elif next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            elif next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            elif next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        self._win.disable_solve_button()
        
        self.solution_path = []
        solved = self._solve_r(0, 0)
        if solved:
            self._win.enable_clear_button()
        else:
            self._win.enable_solve_button()
        return solved

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        self.solution_path.append((i, j))

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

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
        self._win.clear_canvas()

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j, with_delay=False)

        for k in range(len(self.solution_path) - 1):
            i, j = self.solution_path[k]
            ni, nj = self.solution_path[k + 1]
            self._cells[i][j].draw_move(self._cells[ni][nj])

        self._draw_cell(0, 0, fill_color="green", text="S")
        self._draw_cell(self._num_cols - 1, self._num_rows - 1, fill_color="red", text="E")

        self._win.redraw()

        self._win.disable_clear_button()
        
    def new_maze(self):
        self._win.clear_canvas()
        self._cells = []
        self.solution_path = []
        self._win.set_move_callback(None)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self.user_position = (0, 0)
        self._win.disable_clear_button()
        self._win.redraw()
        self._win.enable_solve_button()
        self._win.set_move_callback(self.move_user)