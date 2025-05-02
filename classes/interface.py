import copy
from tkinter import Tk, Label, IntVar, Entry, Button, Canvas, NW, Frame, PhotoImage, messagebox, TclError, Checkbutton, \
    BooleanVar, DoubleVar

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
        self.grids = []

        self.fish_nb_counter = None
        self.shark_nb_counter = None
        self.chronons_counter = None

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

        self.follow_entities = False

        self.start_button = None
        self.pause_button = None
        self.stop_button = None
        self.previous_button = None
        self.next_button = None
        self.throwback_chronon_label = None

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
        control_buttons_frame.grid(row=11, column=0, columnspan=3)
        self.frames['control_buttons_frame'] = control_buttons_frame
        history_frame = Frame(main_frame, bg="red")
        history_frame.grid(row=2, column=0, columnspan=2)
        self.frames['history_frame'] = history_frame

        return self.window

    def create_assets(self):

        fish_image = Image.open("resources/fish.png")
        fish_image = fish_image.resize((CELL_SIZE, CELL_SIZE))
        fish_image = ImageTk.PhotoImage(fish_image)

        followed_fish_image = Image.open("resources/followed_fish.png")
        followed_fish_image = followed_fish_image.resize((CELL_SIZE, CELL_SIZE))
        followed_fish_image = ImageTk.PhotoImage(followed_fish_image)

        shark_image = Image.open("resources/shark.png")
        shark_image = shark_image.resize((CELL_SIZE, CELL_SIZE))
        shark_image = ImageTk.PhotoImage(shark_image)

        followed_shark_image = Image.open("resources/followed_shark.png")
        followed_shark_image = followed_shark_image.resize((CELL_SIZE, CELL_SIZE))
        followed_shark_image = ImageTk.PhotoImage(followed_shark_image)

        empty_image = Image.open("resources/empty.png")
        empty_image = empty_image.resize((CELL_SIZE, CELL_SIZE))
        empty_image = ImageTk.PhotoImage(empty_image)

        self.images = {
            'fish': fish_image,
            'followed_fish': followed_fish_image,
            'shark': shark_image,
            'followed_shark': followed_shark_image,
            'empty': empty_image
        }

    def draw_counter(self):

        fish_label = Label(self.frames['counter_frame'], text="Fishes:", bg="yellow")
        fish_label.grid(row=0, column=0)
        self.fish_nb_counter = Label(self.frames['counter_frame'], text="0", bg="yellow")
        self.fish_nb_counter.grid(row=0, column=1)

        shark_label = Label(self.frames['counter_frame'], text="Sharks:", bg="yellow")
        shark_label.grid(row=0, column=2)
        self.shark_nb_counter = Label(self.frames['counter_frame'], text="0", bg="yellow")
        self.shark_nb_counter.grid(row=0, column=3)

        chronons_label = Label(self.frames['counter_frame'], text="Chronons:", bg="yellow")
        chronons_label.grid(row=0, column=4)
        self.chronons_counter = Label(self.frames['counter_frame'], text="0", bg="yellow")
        self.chronons_counter.grid(row=0, column=5)

    @classmethod
    def input_component(cls, frame, text, default_value, row):

        component_label = Label(frame, text=text)
        component_label.grid(row=row, column=0)
        component_value = DoubleVar()
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

        check_value = BooleanVar(value=False)
        follow_entities_checkbox = Checkbutton(self.frames['control_frame'], text='Follow entities',variable=check_value, onvalue=True, offvalue=False, command=lambda: setattr(self, 'follow_entities', check_value.get()))
        follow_entities_checkbox.grid(row=10, column=0)

        self.start_button = Button(self.frames['control_buttons_frame'], text="Start", command=lambda:self.check_parameters())
        self.start_button.grid(row=0, column=0)
        self.pause_button = Button(self.frames['control_buttons_frame'], text="Pause", command=lambda:SimulationControl.pause_simulation(self))
        self.pause_button.grid(row=0, column=2)
        self.stop_button = Button(self.frames['control_buttons_frame'], text="Stop", command=lambda:SimulationControl.stop_simulation(self))
        self.stop_button.grid(row=0, column=4)


        self.previous_button = Button(self.frames['control_buttons_frame'], text="Previous", command=lambda:self.draw_wator(self.grids[SimulationControl.throwback_chronon], throwback="previous"))
        self.previous_button.grid(row=1, column=0)
        self.throwback_chronon_label = Label(self.frames['control_buttons_frame'], text=SimulationControl.throwback_chronon)
        self.throwback_chronon_label.grid(row=1, column=2)
        self.next_button = Button(self.frames['control_buttons_frame'], text="Next", command=lambda:self.draw_wator(self.grids[SimulationControl.throwback_chronon], throwback="next"))
        self.next_button.grid(row=1, column=4)

        self.start_button.grid(row=0, column=0)

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

    def draw_wator(self, grid, throwback = None):

        if not throwback:
            self.grids.append(copy.deepcopy(grid))
        else:
            if throwback == "previous":
                if SimulationControl.throwback_chronon > 0:
                    SimulationControl.throwback_chronon -= 1
                grid = self.grids[SimulationControl.throwback_chronon]
            elif throwback == "next" and SimulationControl.throwback_chronon < SimulationControl.current_chronon:
                if SimulationControl.throwback_chronon < SimulationControl.current_chronon:
                    SimulationControl.throwback_chronon += 1
                grid = self.grids[SimulationControl.throwback_chronon]
            self.throwback_chronon_label['text'] = SimulationControl.throwback_chronon

        if not self.image_ids:
            self.image_ids = []

            for x, row in enumerate(grid):
                row_ids = []
                for y, cell in enumerate(row):
                    if isinstance(cell, Fish):
                        if cell.followed:
                            img = self.images.get(cell, self.images["followed_fish"])
                        else:
                            img = self.images.get(cell, self.images["fish"])
                    elif isinstance(cell, Shark):
                        if cell.followed:
                            img = self.images.get(cell, self.images["followed_shark"])
                        else:
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
                        if cell.followed:
                            img = self.images.get(cell, self.images["followed_fish"])
                        else:
                            img = self.images.get(cell, self.images["fish"])
                    elif isinstance(cell, Shark):
                        if cell.followed:
                            img = self.images.get(cell, self.images["followed_shark"])
                        else:
                            img = self.images.get(cell, self.images["shark"])
                    else:
                        img = self.images.get(cell, self.images["empty"])
                    self.canvas.itemconfig(self.image_ids[x][y], image=img)

    def reset_canvas(self):
        """
        Resets the canvas.
        """
        self.grids = []
        if self.image_ids:
            for row in self.image_ids:
                for cell in row:
                    img = self.images.get(cell, self.images["empty"])
                    self.canvas.itemconfig(cell, image=img)
                    self.pause_button.config(text="Pause")

    def check_parameters(self) -> None:
        """
        Checks if all inputs are valid.
        """

        valid = True
        self.alert_label['text'] = ""

        valid = self.check_parameter(self.grid_height_value, "grid height", 2, valid)
        valid = self.check_parameter(self.grid_width_value, "grid width", 2, valid)
        valid = self.check_parameter(self.fish_starting_population_value, "fish starting population value", 1, valid)
        valid = self.check_parameter(self.fish_reproduction_time_value, "fish reproduction time value", 1, valid)
        valid = self.check_parameter(self.shark_starting_population_value, "shark starting population value", 0, valid)
        valid = self.check_parameter(self.shark_reproduction_time_value, "shark reproduction time value", 0, valid)
        valid = self.check_parameter(self.shark_starting_energy_value, "shark starting energy value", 1, valid)
        valid = self.check_parameter(self.shark_starvation_time_value, "shark starvation time value",0, valid)
        valid = self.check_parameter(self.simulation_length_value, "simulation length value", 1, valid)
        valid = self.check_parameter(self.chronon_duration_value, "chronon duration value", 0, valid)

        try:
            if self.fish_starting_population_value.get() + self.shark_starting_population_value.get() > self.grid_height_value.get() * self.grid_width_value.get():
                valid = False
                self.alert_label['text'] += "\nToo many fishes for grid size"
        except TclError:
            valid = False

        if valid:
            SimulationControl.start_simulation(self)

    def check_parameter(self, parameter: DoubleVar, parameter_name: str, min_value, valid: bool) -> bool:
        """
        Checks if a DoubleVar input is valid.

        Args:
            parameter (DoubleVar): The input to check.
            parameter_name (str): The name to show in alerts.
            valid (bool): The previous state of valid.

        Returns:
            valid (boolean): The validity of the input.
        """
        try:
            value = int(parameter.get() // 1)
            if value < min_value :
                valid = False
                self.alert_label['text']+=f"\nEnter a valid {parameter_name} (> {min_value})"
            else:
                parameter.set(value)
        except TclError:
            valid = False
            self.alert_label['text']+=f"\nEnter a valid {parameter_name} (> {min_value})"

        return valid