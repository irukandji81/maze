from tkinter import Tk, BOTH, Canvas, Button, Frame, LEFT, TOP, X, font

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        # Create a frame to hold the buttons
        self.__button_frame = Frame(self.__root, bg="lightgray")
        self.__button_frame.pack(side=TOP, fill=X)

        # Define a custom font
        custom_font = font.Font(family="Helvetica", size=12, weight="bold")

        # Add a New Maze button
        self.__new_maze_button = Button(self.__button_frame, text="New Maze", command=self.new_maze, width=20, height=2, bg="blue", fg="white", font=custom_font, padx=10, pady=5, bd=3, relief="raised")
        self.__new_maze_button.pack(side=LEFT, fill=X, expand=1, padx=5, pady=5)

        # Add a Solve button
        self.__solve_button = Button(self.__button_frame, text="Solve", command=self.solve, width=20, height=2, bg="green", fg="white", font=custom_font, padx=10, pady=5, bd=3, relief="raised")
        self.__solve_button.pack(side=LEFT, fill=X, expand=1, padx=5, pady=5)

        # Add a Clear Path button
        self.__clear_button = Button(self.__button_frame, text="Clear Path", command=self.clear_path, state="disabled", width=20, height=2, bg="#4B0082", fg="white", font=custom_font, padx=10, pady=5, bd=3, relief="raised")
        self.__clear_button.pack(side=LEFT, fill=X, expand=1, padx=5, pady=5)

        self.__canvas = Canvas(self.__root, bg="#1E1E1E", height=height, width=width)  # Set canvas background to dark grey
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

        self.__root.bind("<Up>", self.move_up)
        self.__root.bind("<Down>", self.move_down)
        self.__root.bind("<Left>", self.move_left)
        self.__root.bind("<Right>", self.move_right)

        self.__victory_label = None

    def show_victory_message(self):
        if self.__victory_label is None:
            self.__victory_label = self.__canvas.create_text(
                self.__canvas.winfo_width() // 2,
                self.__canvas.winfo_height() // 2,
                text="Congratulations! You solved the maze!",
                fill="yellow",
                font=("Helvetica", 24, "bold")
            )
        self.redraw()
    
    def move_up(self, event):
        if self.move_callback:
            self.move_callback("up")

    def move_down(self, event):
        if self.move_callback:
            self.move_callback("down")

    def move_left(self, event):
        if self.move_callback:
            self.move_callback("left")

    def move_right(self, event):
        if self.move_callback:
            self.move_callback("right")

    def set_move_callback(self, callback):
        self.move_callback = callback

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def draw_line(self, line, fill_color="white"):  # Default line color to white
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