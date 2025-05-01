from tkinter import Tk, Label, IntVar, Entry, Button, Canvas, NW, Frame, PhotoImage, messagebox, TclError

from PIL import Image, ImageTk

from classes.planet import Fish, Shark
from services.simulation_control import SimulationControl
from settings import CELL_SIZE, simulation_parameters


class Interface:

    def __init__(self):

        self.window = None
        self.canvas = None
        self.frames = {}

        self.images = {}
        self.image_ids = []

        self.grid_height_value = None
        self.grid_width_value = None
        self.simulation_length_value = None
        self.fish_reproduction_time_value = None
        self.shark_reproduction_time_value = None
        self.shark_starvation_time_value = None
        self.shark_starting_energy_value = None
        self.shark_starting_population_value = None
        self.fish_starting_population_value = None
        self.chronon_duration_value = None

        self.start_button = None
        self.pause_button = None
        self.stop_button = None

        self.alert_label = None

    def initialize_interface(self):

        self.create_window()
        self.create_assets()
        self.draw_canvas()
        self.draw_counter()
        self.draw_controls()
        self.draw_alerts()

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
        control_buttons_frame = Frame(control_frame, bg="black")
        control_buttons_frame.grid(row=10, column=0, columnspan=3)
        self.frames['control_buttons_frame'] = control_buttons_frame
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

    @classmethod
    def input_component(cls, frame, text, default_value, row):

        component_label = Label(frame, text=text)
        component_label.grid(row=row, column=0)
        component_value = IntVar()
        component_value.set(default_value)
        component_input = Entry(frame, textvariable=component_value, width=30)
        component_input.grid(row=row, column=1)

        return component_value

    def draw_controls(self):

        self.grid_height_value = self.input_component(self.frames['control_frame'], "Grid height:", simulation_parameters['grid_height'], 0)
        self.grid_width_value = self.input_component(self.frames['control_frame'], "Grid width:", simulation_parameters['grid_width'], 1)
        self.fish_starting_population_value = self.input_component(self.frames['control_frame'], "Fish starting population:", simulation_parameters['fish_starting_population'], 2)
        self.fish_reproduction_time_value = self.input_component(self.frames['control_frame'], "Fish reproduction time:", simulation_parameters['fish_reproduction_time'], 3)
        self.shark_starting_population_value = self.input_component(self.frames['control_frame'], "Shark starting population:", simulation_parameters['shark_starting_population'], 4)
        self.shark_reproduction_time_value = self.input_component(self.frames['control_frame'], "Shark reproduction time:", simulation_parameters['shark_reproduction_time'], 5)
        self.shark_starting_energy_value = self.input_component(self.frames['control_frame'], "Shark starting energy:", simulation_parameters['shark_starting_energy'], 6)
        self.shark_starvation_time_value = self.input_component(self.frames['control_frame'], "Shark starvation time:", simulation_parameters['shark_starvation_time'], 7)
        self.simulation_length_value = self.input_component(self.frames['control_frame'], "Simulation duration:", simulation_parameters['simulation_duration'], 8)
        self.chronon_duration_value = self.input_component(self.frames['control_frame'], "Chronon duration (in ms):", simulation_parameters['chronon_duration'], 9)

        self.start_button = Button(self.frames['control_buttons_frame'], text="Start", command=lambda:self.check_parameters())
        self.start_button.grid(row=0, column=0)

        self.pause_button = Button(self.frames['control_buttons_frame'], text="Pause", command=lambda:SimulationControl.pause_simulation(self))
        self.pause_button.grid(row=0, column=1)

        self.stop_button = Button(self.frames['control_buttons_frame'], text="Stop", command=lambda:SimulationControl.stop_simulation(self))
        self.stop_button.grid(row=0, column=2)

    def update_canvas(self):
        canvas_width = simulation_parameters['grid_width'] * CELL_SIZE
        canvas_height = simulation_parameters['grid_height'] * CELL_SIZE

        self.canvas.config(width=canvas_width, height=canvas_height)
        self.canvas.update_idletasks()

    def draw_canvas(self):
        canvas_width = simulation_parameters['grid_width'] * CELL_SIZE
        canvas_height = simulation_parameters['grid_height'] * CELL_SIZE
        canvas = Canvas(self.frames['simulation_frame'], width=canvas_width, height=canvas_height, bg='#42b6f5')
        canvas.grid(row=0, column=0)

        self.canvas = canvas

    def draw_alerts(self):
        self.alert_label = Label(self.frames['control_frame'], text="", bg="pink")
        self.alert_label.grid(row=12, column=0, columnspan=3)

    def draw_wator(self, grid):

        if not self.image_ids:
            self.image_ids = []

            for x, row in enumerate(grid):
                row_ids = []
                for y, cell in enumerate(row):
                    if isinstance(cell, Fish):
                        img = self.images.get(cell, self.images["fish"])
                    elif isinstance(cell, Shark):
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
                    if isinstance(cell, Fish):
                        img = self.images.get(cell, self.images["fish"])
                    elif isinstance(cell, Shark):
                        img = self.images.get(cell, self.images["shark"])
                    else:
                        img = self.images.get(cell, self.images["empty"])
                    self.canvas.itemconfig(self.image_ids[x][y], image=img)

    def reset_interface(self):
        if self.image_ids:
            for row in self.image_ids:
                for cell in row:
                    img = self.images.get(cell, self.images["empty"])
                    self.canvas.itemconfig(cell, image=img)
                    self.pause_button.config(text="Pause")

    def check_parameters(self):

        valid = True
        self.alert_label['text'] = ""

        try:
            if self.grid_height_value.get() == 0:
                valid = False
                self.alert_label['text']+="\nEntrez une grid height valide"
        except TclError:
            valid = False
            self.alert_label['text']+="\nEntrez une grid height valide"

        try:
            if self.grid_width_value.get() == 0:
                valid = False
                self.alert_label['text']+="\nEntrez une grid width valide"
        except TclError:
            valid = False
            self.alert_label['text']+="\nEntrez une grid width valide"

        try:
            if self.fish_starting_population_value.get() == 0:
                valid = False
                self.alert_label['text']+="\nEntrez une fish_starting_population_value valide"
        except TclError:
            valid = False
            self.alert_label['text']+="\nEntrez une fish_starting_population_value valide"

        try:
            if self.fish_reproduction_time_value.get() == 0:
                valid = False
                self.alert_label['text']+="\nEntrez une fish_reproduction_time_value valide"
        except TclError:
            valid = False
            self.alert_label['text']+="\nEntrez une fish_reproduction_time_value valide"

        try:
            if self.shark_starting_population_value.get() == 0:
                valid = False
                self.alert_label['text']+="\nEntrez une shark_starting_population_value valide"
        except TclError:
            valid = False
            self.alert_label['text']+="\nEntrez une shark_starting_population_value valide"

        try:
            if self.shark_reproduction_time_value.get() == 0:
                valid = False
                self.alert_label['text']+="\nEntrez une shark_reproduction_time_value valide"
        except TclError:
            valid = False
            self.alert_label['text']+="\nEntrez une shark_reproduction_time_value valide"

        try:
            if self.shark_starting_energy_value.get() == 0:
                valid = False
                self.alert_label['text']+="\nEntrez une shark_starting_energy_value valide"
        except TclError:
            valid = False
            self.alert_label['text']+="\nEntrez une shark_starting_energy_value valide"

        try:
            if self.shark_starvation_time_value.get() == 0:
                valid = False
                self.alert_label['text']+="\nEntrez une shark_starvation_time_value valide"
        except TclError:
            valid = False
            self.alert_label['text']+="\nEntrez une shark_starvation_time_value valide"

        try:
            if self.simulation_length_value.get() == 0:
                valid = False
                self.alert_label['text']+="\nEntrez une simulation_length_value valide"
        except TclError:
            valid = False
            self.alert_label['text']+="\nEntrez une simulation_length_value valide"

        try:
            if self.chronon_duration_value.get() == 0:
                valid = False
                self.alert_label['text']+="\nEntrez une chronon_duration_value valide"
        except TclError:
            valid = False
            self.alert_label['text']+="\nEntrez une chronon_duration_value valide"

        try:
            if self.fish_starting_population_value.get() + self.shark_starting_population_value.get() > self.grid_height_value.get() * self.grid_width_value.get():
                valid = False
                self.alert_label['text'] += "\nToo many fishes for grid size"
        except TclError:
            valid = False

        if valid:
            SimulationControl.start_simulation(self)