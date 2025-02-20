from tkinter import Tk, BOTH, Canvas, Button

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

        # Add a Solve button
        self.__solve_button = Button(self.__root, text="Solve", command=self.solve)
        self.__solve_button.pack()

        # Add a Clear Path button
        self.__clear_button = Button(self.__root, text="Clear Path", command=self.clear_path, state="disabled")
        self.__clear_button.pack()

        # Add a New Maze button
        self.__new_maze_button = Button(self.__root, text="New Maze", command=self.new_maze)
        self.__new_maze_button.pack()

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def close(self):
        self.__running = False

    def solve(self):
        if self.solve_callback:
            self.solve_callback()
            self.enable_clear_button()  # Enable the Clear Path button after solving

    def clear_path(self):
        if self.clear_callback:
            self.clear_callback()

    def new_maze(self):
        if self.new_maze_callback:
            self.new_maze_callback()
            self.disable_clear_button()  # Disable the Clear Path button for the new maze

    def set_solve_callback(self, callback):
        self.solve_callback = callback

    def set_clear_callback(self, callback):
        self.clear_callback = callback

    def set_new_maze_callback(self, callback):
        self.new_maze_callback = callback

    def enable_clear_button(self):
        self.__clear_button.config(state="normal")

    def disable_clear_button(self):
        self.__clear_button.config(state="disabled")

    def clear_canvas(self):
        self.__canvas.delete("all")

    def disable_solve_button(self):
        self.__solve_button.config(state="disabled")

    def enable_solve_button(self):
        self.__solve_button.config(state="normal")

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)