from tkinter import Canvas, Tk, NW

from PIL import Image, ImageTk

from settings import cell_size, grid_width, grid_height


class Interface:
    def __init__(self):
        self.window = None
        self.images = {}

    def create_window(self):
        self.window = Tk()
        return self.window

    def create_assets(self):
        fish_image = Image.open("resources/fish.png")
        fish_image = fish_image.resize((cell_size, cell_size))
        fish_image = ImageTk.PhotoImage(fish_image)

        shark_image = Image.open("resources/shark.png")
        shark_image = shark_image.resize((cell_size, cell_size))
        shark_image = ImageTk.PhotoImage(shark_image)

        self.images['fish_image'] = fish_image
        self.images['shark_image'] = shark_image

    def draw_wa_tor(self, grid):
        canvas_width = grid_width * cell_size
        canvas_height = grid_height * cell_size
        canvas = Canvas(self.window, width=canvas_width, height=canvas_height, bg='#42b6f5')
        canvas.grid(row=20, column=20)

        for x, row in enumerate(grid):
            for y, cell in enumerate(row):
                if cell == "fish":
                    canvas.create_image(x * cell_size, y * cell_size, anchor=NW, image=self.images['fish_image'])
                elif cell == "shark":
                    canvas.create_image(x * cell_size, y * cell_size, anchor=NW, image=self.images['shark_image'])