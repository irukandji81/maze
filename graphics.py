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
        self.__clear_button = Button(self.__root, text="Clear Path", command=self.clear_path)
        self.__clear_button.pack()

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

    def clear_path(self):
        if self.clear_callback:
            self.clear_callback()

    def set_solve_callback(self, callback):
        self.solve_callback = callback

    def set_clear_callback(self, callback):
        self.clear_callback = callback
    
    def clear_canvas(self):
        self.__canvas.delete("all")

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