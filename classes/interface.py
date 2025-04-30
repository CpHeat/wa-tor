from tkinter import Tk, Label, IntVar, Entry, Button, Canvas, NW, Frame, PhotoImage

from PIL import Image, ImageTk

from services.simulation_control import SimulationControl
from settings import CELL_SIZE, simulation_parameters


class Interface:
    def __init__(self):
        self.window = None
        self.canvas = None
        self.frames = {}
        self.images = {}
        self.image_ids = []

    def initialize_interface(self):
        self.create_window()
        self.create_assets()
        self.draw_canvas()
        self.draw_counter()
        self.draw_controls()

    def create_window(self):
        self.window = Tk()
        main_frame = Frame(self.window)
        main_frame.grid(row=0, column=0)

        counter_frame = Frame(main_frame, bg="green")
        counter_frame.grid(row=0, column=0, columnspan=2)
        self.frames['counter_frame'] = counter_frame
        simulation_frame = Frame(main_frame, bg="yellow")
        simulation_frame.grid(row=1, column=0)
        self.frames['simulation_frame'] = simulation_frame
        control_frame = Frame(main_frame, bg="purple")
        control_frame.grid(row=1, column=1)
        self.frames['control_frame'] = control_frame
        history_frame = Frame(main_frame, bg="red")
        history_frame.grid(row=2, column=0, columnspan=2)
        self.frames['history_frame'] = history_frame

        return self.window

    def create_assets(self):
        fish_image = Image.open("resources/fish.png")
        fish_image = fish_image.resize((CELL_SIZE, CELL_SIZE))
        fish_image = ImageTk.PhotoImage(fish_image)

        shark_image = Image.open("resources/shark.png")
        shark_image = shark_image.resize((CELL_SIZE, CELL_SIZE))
        shark_image = ImageTk.PhotoImage(shark_image)

        empty_image = Image.open("resources/empty.png")
        empty_image = empty_image.resize((CELL_SIZE, CELL_SIZE))
        empty_image = ImageTk.PhotoImage(empty_image)

        self.images = {
            'fish': fish_image,
            'shark': shark_image,
            'empty': empty_image
        }

    def draw_counter(self):
        fish_label = Label(self.frames['counter_frame'], text="Fishes:", bg="yellow")
        fish_label.grid(row=0, column=0)
        fish_nb = Label(self.frames['counter_frame'], text="12", bg="yellow")
        fish_nb.grid(row=0, column=1)

        shark_label = Label(self.frames['counter_frame'], text="Sharks:", bg="yellow")
        shark_label.grid(row=0, column=2)
        shark_nb = Label(self.frames['counter_frame'], text="15", bg="yellow")
        shark_nb.grid(row=0, column=3)

        chronons_label = Label(self.frames['counter_frame'], text="Chronons:", bg="yellow")
        chronons_label.grid(row=0, column=4)
        chronons_nb = Label(self.frames['counter_frame'], text="8", bg="yellow")
        chronons_nb.grid(row=0, column=5)

    def draw_controls(self):
        grid_height_label = Label(self.frames['control_frame'], text="Grid height:")
        grid_height_label.grid(row=0, column=0)
        grid_height_value = IntVar()
        grid_height_value.set(simulation_parameters['grid_height'])
        grid_height_input = Entry(self.frames['control_frame'], textvariable=grid_height_value, width=30)
        grid_height_input.grid(row=0, column=1)

        grid_width_label = Label(self.frames['control_frame'], text="Grid width:")
        grid_width_label.grid(row=1, column=0)
        grid_width_value = IntVar()
        grid_width_value.set(simulation_parameters['grid_width'])
        grid_width_input = Entry(self.frames['control_frame'], textvariable=grid_width_value, width=30)
        grid_width_input.grid(row=1, column=1)

        simulation_length_label = Label(self.frames['control_frame'], text="Simulation length:")
        simulation_length_label.grid(row=2, column=0)
        simulation_length_value = IntVar()
        simulation_length_value.set(simulation_parameters['simulation_duration'])
        simulation_length_input = Entry(self.frames['control_frame'], textvariable=simulation_length_value, width=30)
        simulation_length_input.grid(row=2, column=1)

        fish_reproduction_time_label = Label(self.frames['control_frame'], text="Fish reproduction time:")
        fish_reproduction_time_label.grid(row=3, column=0)
        fish_reproduction_time_value = IntVar()
        fish_reproduction_time_value.set(simulation_parameters['fish_reproduction_time'])
        fish_reproduction_time_input = Entry(self.frames['control_frame'], textvariable=fish_reproduction_time_value, width=30)
        fish_reproduction_time_input.grid(row=3, column=1)

        shark_reproduction_time_label = Label(self.frames['control_frame'], text="Shark reproduction time:")
        shark_reproduction_time_label.grid(row=4, column=0)
        shark_reproduction_time_value = IntVar()
        shark_reproduction_time_value.set(simulation_parameters['shark_reproduction_time'])
        shark_reproduction_time_input = Entry(self.frames['control_frame'], textvariable=shark_reproduction_time_value, width=30)
        shark_reproduction_time_input.grid(row=4, column=1)

        shark_starvation_time_label = Label(self.frames['control_frame'], text="Shark starvation time:")
        shark_starvation_time_label.grid(row=5, column=0)
        shark_starvation_time_value = IntVar()
        shark_starvation_time_value.set(simulation_parameters['shark_starvation_time'])
        shark_starvation_time_input = Entry(self.frames['control_frame'], textvariable=shark_starvation_time_value, width=30)
        shark_starvation_time_input.grid(row=5, column=1)

        shark_starting_energy_label = Label(self.frames['control_frame'], text="Shark starting energy:")
        shark_starting_energy_label.grid(row=6, column=0)
        shark_starting_energy_value = IntVar()
        shark_starting_energy_value.set(simulation_parameters['shark_starting_energy'])
        shark_starting_energy_input = Entry(self.frames['control_frame'], textvariable=shark_starting_energy_value, width=30)
        shark_starting_energy_input.grid(row=6, column=1)

        shark_energy_gain_label = Label(self.frames['control_frame'], text="Shark energy gain:")
        shark_energy_gain_label.grid(row=7, column=0)
        shark_energy_gain_value = IntVar()
        shark_energy_gain_value.set(simulation_parameters['shark_energy_gain'])
        shark_energy_gain_input = Entry(self.frames['control_frame'], textvariable=shark_energy_gain_value, width=30)
        shark_energy_gain_input.grid(row=7, column=1)

        shark_starting_population_label = Label(self.frames['control_frame'], text="Shark starting population:")
        shark_starting_population_label.grid(row=8, column=0)
        shark_starting_population_value = IntVar()
        shark_starting_population_value.set(simulation_parameters['shark_starting_population'])
        shark_starting_population_input = Entry(self.frames['control_frame'], textvariable=shark_starting_population_value, width=30)
        shark_starting_population_input.grid(row=8, column=1)

        fish_starting_population_label = Label(self.frames['control_frame'], text="Fish starting population:")
        fish_starting_population_label.grid(row=9, column=0)
        fish_starting_population_value = IntVar()
        fish_starting_population_value.set(simulation_parameters['fish_starting_population'])
        fish_starting_population_input = Entry(self.frames['control_frame'], textvariable=fish_starting_population_value, width=30)
        fish_starting_population_input.grid(row=9, column=1)

        chronon_duration_label = Label(self.frames['control_frame'], text="Chronon duration (in ms):")
        chronon_duration_label.grid(row=10, column=0)
        chronon_duration_value = IntVar()
        chronon_duration_value.set(simulation_parameters['chronon_duration'])
        chronon_duration_input = Entry(self.frames['control_frame'], textvariable=chronon_duration_value, width=30)
        chronon_duration_input.grid(row=10, column=1)

        start_button = Button(self.frames['control_frame'], text="Start", command=lambda:SimulationControl.start_simulation(
            self,
            grid_height_value,
            grid_width_value,
            simulation_length_value,
            fish_reproduction_time_value,
            shark_reproduction_time_value,
            shark_starvation_time_value,
            shark_starting_energy_value,
            shark_energy_gain_value,
            shark_starting_population_value,
            fish_starting_population_value,
            chronon_duration_value
        ))
        start_button.grid(row=11, column=0, columnspan=2)

    def draw_canvas(self):
        canvas_width = simulation_parameters['grid_width'] * CELL_SIZE
        canvas_height = simulation_parameters['grid_height'] * CELL_SIZE
        canvas = Canvas(self.frames['simulation_frame'], width=canvas_width, height=canvas_height, bg='#42b6f5')
        canvas.grid(row=0, column=0)

        self.canvas = canvas

    def draw_wator(self, grid):

        if not self.image_ids:
            self.image_ids = []

            for x, row in enumerate(grid):
                row_ids = []
                for y, cell in enumerate(row):
                    if cell == "fish":
                        img = self.images.get(cell, self.images["fish"])
                    elif cell == "shark":
                        img = self.images.get(cell, self.images["shark"])
                    else:
                        img = self.images.get(cell, self.images["empty"])

                    img_id = self.canvas.create_image(
                        y * CELL_SIZE, x * CELL_SIZE, anchor=NW, image=img
                    )
                    row_ids.append(img_id)
                self.image_ids.append(row_ids)
        else:
            for x, row in enumerate(grid):
                for y, cell in enumerate(row):
                    print(cell)
                    if cell == "fish":
                        print("really fish")
                        img = self.images.get(cell, self.images["fish"])
                    elif cell == "shark":
                        img = self.images.get(cell, self.images["shark"])
                    else:
                        img = self.images.get(cell, self.images["empty"])
                    self.canvas.itemconfig(self.image_ids[x][y], image=img)
                    print(f"x={x}, y={y}, cell={cell}, image={img}")