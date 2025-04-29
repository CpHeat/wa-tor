from tkinter import Canvas, Tk, NW, Button, StringVar, Entry, IntVar

from PIL import Image, ImageTk

from test import print_height
from settings import cell_size, grid_width, grid_height, simulation_parameters


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

    def create_controls(self):
        """
        grid_height
        grid_width
        fish_reproduction_time
        shark_reproduction_time
        fish_nb
        shark_nb
        shark_starvation_time
        shark_energy_gain
        shark_starting_energy
        simulation_length
        """

        grid_height_value = IntVar()
        grid_height_value.set(grid_height)
        grid_height_input = Entry(self.window, textvariable=grid_height_value, width=30)
        grid_height_input.grid(row=0, column=1)
        grid_height_button = Button(self.window, text="Save", command=self.set_grid_height)
        grid_height_button.grid(row=0, column=2)


        #button
        bouton=Button(self.window, text="Fermer", command=self.window.quit)
        bouton.grid(row=0, column=1)
        bouton = Button(self.window, text="Fermer", command=self.window.quit)
        bouton.grid(row=1, column=1)

    def set_grid_height(self):
        print("set grid height")
        simulation_parameters['grid_height'] = 12

        print_height()

    def draw_wa_tor(self, grid):
        canvas_width = grid_width * cell_size
        canvas_height = grid_height * cell_size
        canvas = Canvas(self.window, width=canvas_width, height=canvas_height, bg='#42b6f5')
        canvas.grid(row=0, column=0, rowspan=10)

        for x, row in enumerate(grid):
            for y, cell in enumerate(row):
                if cell == "fish":
                    canvas.create_image(x * cell_size, y * cell_size, anchor=NW, image=self.images['fish_image'])
                elif cell == "shark":
                    canvas.create_image(x * cell_size, y * cell_size, anchor=NW, image=self.images['shark_image'])