from tkinter import Tk, Label, IntVar, Entry, Button, Canvas, NW

from PIL import Image, ImageTk

from settings import CELL_SIZE, simulation_parameters


class Interface:
    def __init__(self):
        self.window = None
        self.images = {}

    def create_window(self):
        self.window = Tk()
        return self.window

    def create_assets(self):
        fish_image = Image.open("resources/fish.png")
        fish_image = fish_image.resize((CELL_SIZE, CELL_SIZE))
        fish_image = ImageTk.PhotoImage(fish_image)

        shark_image = Image.open("resources/shark.png")
        shark_image = shark_image.resize((CELL_SIZE, CELL_SIZE))
        shark_image = ImageTk.PhotoImage(shark_image)

        self.images['fish_image'] = fish_image
        self.images['shark_image'] = shark_image

    def create_controls(self):
        grid_height_label = Label(self.window, text="Grid height:")
        grid_height_label.grid(row=0, column=1)
        grid_height_value = IntVar()
        grid_height_value.set(simulation_parameters['grid_height'])
        grid_height_input = Entry(self.window, textvariable=grid_height_value, width=30)
        grid_height_input.grid(row=0, column=2)

        grid_width_label = Label(self.window, text="Grid width:")
        grid_width_label.grid(row=1, column=1)
        grid_width_value = IntVar()
        grid_width_value.set(simulation_parameters['grid_width'])
        grid_width_input = Entry(self.window, textvariable=grid_width_value, width=30)
        grid_width_input.grid(row=1, column=2)

        simulation_length_label = Label(self.window, text="Simulation length:")
        simulation_length_label.grid(row=2, column=1)
        simulation_length_value = IntVar()
        simulation_length_value.set(simulation_parameters['simulation_length'])
        simulation_length_input = Entry(self.window, textvariable=simulation_length_value, width=30)
        simulation_length_input.grid(row=2, column=2)

        fish_reproduction_time_label = Label(self.window, text="Fish reproduction time:")
        fish_reproduction_time_label.grid(row=3, column=1)
        fish_reproduction_time_value = IntVar()
        fish_reproduction_time_value.set(simulation_parameters['fish_reproduction_time'])
        fish_reproduction_time_input = Entry(self.window, textvariable=fish_reproduction_time_value, width=30)
        fish_reproduction_time_input.grid(row=3, column=2)

        shark_reproduction_time_label = Label(self.window, text="Shark reproduction time:")
        shark_reproduction_time_label.grid(row=4, column=1)
        shark_reproduction_time_value = IntVar()
        shark_reproduction_time_value.set(simulation_parameters['shark_reproduction_time'])
        shark_reproduction_time_input = Entry(self.window, textvariable=shark_reproduction_time_value, width=30)
        shark_reproduction_time_input.grid(row=4, column=2)

        shark_starvation_time_label = Label(self.window, text="Shark starvation time:")
        shark_starvation_time_label.grid(row=5, column=1)
        shark_starvation_time_value = IntVar()
        shark_starvation_time_value.set(simulation_parameters['shark_starvation_time'])
        shark_starvation_time_input = Entry(self.window, textvariable=shark_starvation_time_value, width=30)
        shark_starvation_time_input.grid(row=5, column=2)

        shark_starting_energy_label = Label(self.window, text="Shark starting energy:")
        shark_starting_energy_label.grid(row=6, column=1)
        shark_starting_energy_value = IntVar()
        shark_starting_energy_value.set(simulation_parameters['shark_starting_energy'])
        shark_starting_energy_input = Entry(self.window, textvariable=shark_starting_energy_value, width=30)
        shark_starting_energy_input.grid(row=6, column=2)

        shark_energy_gain_label = Label(self.window, text="Shark energy gain:")
        shark_energy_gain_label.grid(row=7, column=1)
        shark_energy_gain_value = IntVar()
        shark_energy_gain_value.set(simulation_parameters['shark_energy_gain'])
        shark_energy_gain_input = Entry(self.window, textvariable=shark_energy_gain_value, width=30)
        shark_energy_gain_input.grid(row=7, column=2)

        shark_population_label = Label(self.window, text="Shark population:")
        shark_population_label.grid(row=8, column=1)
        shark_population_value = IntVar()
        shark_population_value.set(simulation_parameters['shark_population'])
        shark_population_input = Entry(self.window, textvariable=shark_population_value, width=30)
        shark_population_input.grid(row=8, column=2)

        fish_population_label = Label(self.window, text="Fish population:")
        fish_population_label.grid(row=9, column=1)
        fish_population_value = IntVar()
        fish_population_value.set(simulation_parameters['fish_population'])
        fish_population_input = Entry(self.window, textvariable=fish_population_value, width=30)
        fish_population_input.grid(row=9, column=2)

        chronon_duration_label = Label(self.window, text="Chronon duration (in ms):")
        chronon_duration_label.grid(row=10, column=1)
        chronon_duration_value = IntVar()
        chronon_duration_value.set(simulation_parameters['chronon_duration'])
        chronon_duration_input = Entry(self.window, textvariable=chronon_duration_value, width=30)
        chronon_duration_input.grid(row=10, column=2)

        start_button = Button(self.window, text="Start", command='save')
        start_button.grid(row=11, column=1, columnspan=2)

    def draw_wator(self, grid):
        canvas_width = simulation_parameters['grid_width'] * CELL_SIZE
        canvas_height = simulation_parameters['grid_height'] * CELL_SIZE
        canvas = Canvas(self.window, width=canvas_width, height=canvas_height, bg='#42b6f5')
        canvas.grid(row=0, column=0, rowspan=12)

        for x, row in enumerate(grid):
            for y, cell in enumerate(row):
                if cell == "fish":
                    canvas.create_image(x * CELL_SIZE, y * CELL_SIZE, anchor=NW, image=self.images['fish_image'])
                elif cell == "shark":
                    canvas.create_image(x * CELL_SIZE, y * CELL_SIZE, anchor=NW, image=self.images['shark_image'])