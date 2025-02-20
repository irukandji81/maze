from graphics import Window
from maze import Maze

def main():
    num_rows = 18
    num_cols = 24
    margin = 50
    screen_x = 1900
    screen_y = 1080
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)

    # Disable the Solve button initially
    win.disable_solve_button()

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)

    # Set the solve callback
    win.set_solve_callback(maze.solve)

    # Set the clear path callback
    win.set_clear_callback(maze.clear_path)

    # Set the new maze callback
    win.set_new_maze_callback(maze.new_maze)

    # Disable the Clear Path button initially
    win.disable_clear_button()

    # Enable the Solve button after the maze is fully drawn
    win.enable_solve_button()

    win.wait_for_close()

main()