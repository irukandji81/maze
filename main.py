from graphics import Window
from maze import Maze

def main():
    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)

    # Set the solve callback
    win.set_solve_callback(maze.solve)

    # Set the clear path callback
    win.set_clear_callback(maze.clear_path)

    # Set the new maze callback
    win.set_new_maze_callback(maze.new_maze)

    # Disable the Clear Path button initially
    win.disable_clear_button()

    win.wait_for_close()

main()