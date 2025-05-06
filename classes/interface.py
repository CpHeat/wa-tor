import copy
from tkinter import Tk, Label, IntVar, Entry, Button, Canvas, NW, Frame, PhotoImage, messagebox, TclError, Checkbutton, \
    BooleanVar, DoubleVar, ttk

from PIL import Image, ImageTk, ImageOps

from classes.planet import Fish, Shark
from services.persistence_handler import PersistenceHandler
from services.simulation_control import SimulationControl
from settings import simulation_parameters


class Interface:
    """
    Implements the visual interface for the simulation.

    Methods
    -------
    initialize_interface: Initializes all the interface modules.
    create_window: Creates the main window.
    draw_canvas: Creates the canvas for the simulation output.
    draw_counter: Creates the counter for entities and chronon.
    draw_controls: Creates the control frame for the simulation parameters.
    draw_alerts: Creates the alert space.
    create_assets: Creates the images and set their size to use in the canvas.
    set_cell_size: Sets the cell size to keep the window from overflowing.
    input_component: Creates an input component.
    open_history: Initializes, populates and opens the history window.
    draw_history: Draws the history window.
    update_canvas: Updates the canvas to match the new states of the simulation.
    reset_canvas: Resets the canvas.
    draw_wator: Draws a state of the simulation.
    check_parameters: Checks if all inputs are valid.
    check_parameter: Checks if a DoubleVar input is valid.
    """

    def __init__(self):

        self.window = None
        self.canvas = None
        self.frames = {}

        self.images = {}
        self.image_ids = []
        self.grids = []
        self.grid_lines = []

        self.cell_size = 50

        self.fish_nb_counter = None
        self.shark_nb_counter = None
        self.chronons_counter = None

        self.grid_height_value = None
        self.grid_width_value = None
        self.simulation_duration_value = None
        self.fish_reproduction_time_value = None
        self.shark_reproduction_time_value = None
        self.shark_starvation_time_value = None
        self.shark_energy_gain_value = None
        self.shark_starting_population_value = None
        self.fish_starting_population_value = None
        self.chronon_duration_value = None

        self.follow_entities_value = None
        self.shuffle_entities_value = None

        self.start_button = None
        self.pause_button = None
        self.stop_button = None
        self.previous_button = None
        self.next_button = None
        self.throwback_chronon_label = None

        self.alert_label = None

    def initialize_interface(self) -> None:
        """
        Initializes all the interface modules.
        """
        self.create_window()
        self.draw_canvas()
        self.draw_counter()
        self.draw_controls()
        self.draw_alerts()

    def create_window(self) -> None:
        """
        Creates the main window.
        """
        self.window = Tk()
        main_frame = Frame(self.window)
        main_frame.grid(row=0, column=0)

        counter_frame = Frame(main_frame)
        counter_frame.grid(row=0, column=0, columnspan=2)
        self.frames['counter_frame'] = counter_frame
        simulation_frame = Frame(main_frame)
        simulation_frame.grid(row=1, column=0)
        self.frames['simulation_frame'] = simulation_frame
        control_frame = Frame(main_frame)
        control_frame.grid(row=1, column=1)
        self.frames['control_frame'] = control_frame
        control_buttons_frame = Frame(control_frame)
        control_buttons_frame.grid(row=11, column=0, columnspan=3)
        self.frames['control_buttons_frame'] = control_buttons_frame

    def draw_canvas(self) -> None:
        """
        Creates the canvas for the simulation output.
        """
        self.set_cell_size()
        self.create_assets()

        canvas_width = simulation_parameters['grid_width'] * self.cell_size
        canvas_height = simulation_parameters['grid_height'] * self.cell_size
        canvas = Canvas(self.frames['simulation_frame'], width=canvas_width, height=canvas_height, bg='#42b6f5')
        canvas.grid(row=0, column=0)

        for i in range(simulation_parameters['grid_width'] + 1):
            x = i * self.cell_size
            line = canvas.create_line(x, 0, x, canvas_height, fill="black")
            self.grid_lines.append(line)

        for j in range(simulation_parameters['grid_height'] + 1):
            y = j * self.cell_size
            line = canvas.create_line(0, y, canvas_width, y, fill="black")
            self.grid_lines.append(line)

        self.canvas = canvas

    def draw_counter(self) -> None:
        """
        Creates the counter for entities and chronon.
        """
        fish_label = Label(self.frames['counter_frame'], text="Fishes:")
        fish_label.grid(row=0, column=0)
        self.fish_nb_counter = Label(self.frames['counter_frame'], text="0")
        self.fish_nb_counter.grid(row=0, column=1)

        shark_label = Label(self.frames['counter_frame'], text="Sharks:")
        shark_label.grid(row=0, column=2)
        self.shark_nb_counter = Label(self.frames['counter_frame'], text="0")
        self.shark_nb_counter.grid(row=0, column=3)

        chronons_label = Label(self.frames['counter_frame'], text="Chronons:")
        chronons_label.grid(row=0, column=4)
        self.chronons_counter = Label(self.frames['counter_frame'], text="0")
        self.chronons_counter.grid(row=0, column=5)

    def draw_controls(self) -> None:
        """
        Creates the control frame for the simulation parameters.
        """
        self.grid_height_value = self.input_component(self.frames['control_frame'], "Grid height:", simulation_parameters['grid_height'], 0)
        self.grid_width_value = self.input_component(self.frames['control_frame'], "Grid width:", simulation_parameters['grid_width'], 1)
        self.fish_starting_population_value = self.input_component(self.frames['control_frame'], "Fish starting population:", simulation_parameters['fish_starting_population'], 2)
        self.fish_reproduction_time_value = self.input_component(self.frames['control_frame'], "Fish reproduction time:", simulation_parameters['fish_reproduction_time'], 3)
        self.shark_starting_population_value = self.input_component(self.frames['control_frame'], "Shark starting population:", simulation_parameters['shark_starting_population'], 4)
        self.shark_reproduction_time_value = self.input_component(self.frames['control_frame'], "Shark reproduction time:", simulation_parameters['shark_reproduction_time'], 5)
        self.shark_energy_gain_value = self.input_component(self.frames['control_frame'], "Shark energy gain:", simulation_parameters['shark_energy_gain'], 6)
        self.shark_starvation_time_value = self.input_component(self.frames['control_frame'], "Shark starvation time:", simulation_parameters['shark_starvation_time'], 7)
        self.simulation_duration_value = self.input_component(self.frames['control_frame'], "Simulation duration:", simulation_parameters['simulation_duration'], 8)
        self.chronon_duration_value = self.input_component(self.frames['control_frame'], "Chronon duration (in ms):", simulation_parameters['chronon_duration'], 9)

        self.follow_entities_value = BooleanVar(value=False)
        follow_entities_checkbox = Checkbutton(self.frames['control_frame'], text='Follow entities',variable=self.follow_entities_value, onvalue=True, offvalue=False, command=lambda: setattr(self, 'follow_entities_value', self.follow_entities_value))
        follow_entities_checkbox.grid(row=10, column=0)

        self.shuffle_entities_value = BooleanVar(value=True)
        shuffle_entities_checkbox = Checkbutton(self.frames['control_frame'], text='shuffle entities',
                                               variable=self.shuffle_entities_value, onvalue=True, offvalue=False,
                                               command=lambda: setattr(self, 'shuffle_entities_value',
                                                                       self.shuffle_entities_value))
        shuffle_entities_checkbox.grid(row=10, column=1)

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

        history_button = Button(self.frames['control_buttons_frame'], text="History", command=self.open_history)
        history_button.grid(row=3, column=2)

        database_creation_button = Button(self.frames['control_buttons_frame'], text="Create database", command=PersistenceHandler.create_ddb)
        database_creation_button.grid(row=4, column=2)

    def draw_alerts(self) -> None:
        """
        Creates the alert space.
        """
        self.alert_label = Label(self.frames['control_frame'], text="")
        self.alert_label.grid(row=12, column=0, columnspan=3)

    def create_assets(self) -> None:
        """
        Creates the images and set their size to use in the canvas.
        """
        fish_image = Image.open("resources/fish.png")
        fish_image = fish_image.resize((self.cell_size-2, self.cell_size-2))
        fish_image = ImageTk.PhotoImage(fish_image)

        followed_fish_image = Image.open("resources/followed_fish.png")
        followed_fish_image = followed_fish_image.resize((self.cell_size-2, self.cell_size-2))
        followed_fish_image = ImageTk.PhotoImage(followed_fish_image)

        shark_image = Image.open("resources/shark.png")
        shark_image = shark_image.resize((self.cell_size-2, self.cell_size-2))
        shark_image = ImageTk.PhotoImage(shark_image)

        followed_shark_image = Image.open("resources/followed_shark.png")
        followed_shark_image = followed_shark_image.resize((self.cell_size-2, self.cell_size-2))
        followed_shark_image = ImageTk.PhotoImage(followed_shark_image)

        empty_image = Image.open("resources/empty.png")
        empty_image = empty_image.resize((self.cell_size-2, self.cell_size-2))
        empty_image = ImageTk.PhotoImage(empty_image)

        self.images = {
            'fish': fish_image,
            'followed_fish': followed_fish_image,
            'shark': shark_image,
            'followed_shark': followed_shark_image,
            'empty': empty_image
        }

    def set_cell_size(self) -> None:
        """
        Sets the cell size to keep the window from overflowing.
        """
        self.cell_size = 800 // max(simulation_parameters['grid_width'], simulation_parameters['grid_height'])
        if self.cell_size < 3:
            self.cell_size = 3

        # Recreate assets to match the new size of cells
        self.create_assets()

    @classmethod
    def input_component(cls, frame:Frame, text:str, default_value:int, row:int) -> DoubleVar:
        """
        Creates an input component.

        Parameters:
            frame (Frame): The frame that will contain the component.
            text (str): The text to be displayed in the component.
            default_value (int): The default value of the input..
            row (int): The row of the input component inside the frame.

        Returns:
            component_value (DoubleVar): A reference to the component value.
        """
        component_label = Label(frame, text=text)
        component_label.grid(row=row, column=0)
        component_value = DoubleVar()
        component_value.set(default_value)
        component_input = Entry(frame, textvariable=component_value, width=30)
        component_input.grid(row=row, column=1)

        return component_value

    def open_history(self) -> None:
        """
        Initializes, populates and opens the history window.
        """
        history_data = PersistenceHandler.load_data()

        history_window, history_frame = self.draw_history()

        for data in history_data:
            simulation_label = ttk.Label(history_frame, text=f"Simulation #{data[0]} ({data[1]}):")
            simulation_label.pack(anchor="w", padx=10)
            parameters_content = ttk.Label(history_frame, text=f"Parameters: duration {data[2]}, grid height {data[3]}, grid_width {data[4]}, fish starting population {data[5]}, shark starting population {data[6]}, fish reproduction time {data[7]}, shark reproduction time {data[8]}, shark starvation time {data[9]}, shark energy gain {data[10]}, shuffled {data[11]}")
            parameters_content.pack(anchor="w", padx=10)
            results_content = ttk.Label(history_frame, text=f"Results: fish count {data[13]}, shark count {data[14]}, fish reproduction {data[19]}, shark reproduction {data[20]}")
            results_content.pack(anchor="w", padx=10)

        history_window.mainloop()

    @classmethod
    def draw_history(cls) -> list[Tk|Frame]:
        """
        Draws the history window.

        Returns: [history_window, scrollable_frame]
            history_window: the history window
            scrollable_frame: the frame that will contain the history data
        """
        history_window = Tk()
        history_window.title("Simulation history")

        canvas = Canvas(history_window, borderwidth=0, width=1500, height=1000)
        scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        label = ttk.Label(scrollable_frame, text="Simulations history:", font=("Arial", 14))
        label.pack(pady=10)

        return history_window, scrollable_frame

    def update_canvas(self) -> None:
        """
        Updates the canvas to match the new states of the simulation.
        """
        self.set_cell_size()

        canvas_width, canvas_height = self.get_canvas_size()

        self.canvas.config(width=canvas_width, height=canvas_height)

        self.draw_grid(canvas_width, canvas_height)

        self.canvas.update_idletasks()

    def get_canvas_size(self):
        canvas_width = simulation_parameters['grid_width'] * self.cell_size
        canvas_height = simulation_parameters['grid_height'] * self.cell_size

        return canvas_width, canvas_height

    def draw_grid(self, canvas_width, canvas_height):
        for i in range(simulation_parameters['grid_width'] + 1):
            x = i * self.cell_size
            line = self.canvas.create_line(x, 0, x, canvas_height, fill="black")
            self.grid_lines.append(line)

        for j in range(simulation_parameters['grid_height'] + 1):
            y = j * self.cell_size
            line = self.canvas.create_line(0, y, canvas_width, y, fill="black")
            self.grid_lines.append(line)

    def reset_canvas(self) -> None:
        """
        Resets the canvas.
        """
        # Empty the grid history
        self.grids = []

        # Empty the image list
        if self.image_ids:
            for row in self.image_ids:
                for cell in row:
                    img = self.images.get(cell, self.images["empty"])
                    self.canvas.itemconfig(cell, image=img)
                    self.pause_button.config(text="Pause")

        # Erase the grid
        for line in self.grid_lines:
            self.canvas.delete(line)
        self.grid_lines.clear()

    def draw_wator(self, grid:list, throwback:str|None = None) -> None:
        """
        Draws a state of the simulation.

        Parameters:
            grid (list): A grid to be drawn.
            throwback (str|None): Tells if the state to draw is previous, next or current.
        """
        # If the state to draw is the current state
        if not throwback:
            self.grids.append(copy.deepcopy(grid))
        else:
            # If the state to draw is the previous state
            if throwback == "previous":
                if SimulationControl.throwback_chronon > 0:
                    SimulationControl.throwback_chronon -= 1
                grid = self.grids[SimulationControl.throwback_chronon]
            # If the state to draw is the next state
            elif throwback == "next" and SimulationControl.throwback_chronon < SimulationControl.current_chronon:
                if SimulationControl.throwback_chronon < SimulationControl.current_chronon:
                    SimulationControl.throwback_chronon += 1
                grid = self.grids[SimulationControl.throwback_chronon]
            self.throwback_chronon_label['text'] = SimulationControl.throwback_chronon

        # If it is the initial drawing
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
                        y * self.cell_size + 1, x * self.cell_size + 1, anchor=NW, image=img
                    )
                    row_ids.append(img_id)
                self.image_ids.append(row_ids)
        # If it is an update, we need to change the content of images
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
                    if len(self.image_ids) > x and len(self.image_ids[x]) > y:
                        self.canvas.itemconfig(self.image_ids[x][y], image=img)

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
        valid = self.check_parameter(self.shark_energy_gain_value, "shark energy gain value", 1, valid)
        valid = self.check_parameter(self.shark_starvation_time_value, "shark starvation time value",0, valid)
        valid = self.check_parameter(self.simulation_duration_value, "simulation duration value", 1, valid)
        valid = self.check_parameter(self.chronon_duration_value, "chronon duration value", 0, valid)

        try:
            if self.fish_starting_population_value.get() + self.shark_starting_population_value.get() > self.grid_height_value.get() * self.grid_width_value.get():
                valid = False
                self.alert_label['text'] += "\nToo many fishes for grid size"
        except TclError:
            valid = False

        if valid:
            SimulationControl.start_simulation(self)

    def check_parameter(self, parameter: DoubleVar, parameter_name: str, min_value: int, valid: bool) -> bool:
        """
        Checks if a DoubleVar input is valid.

        Args:
            parameter (DoubleVar): The input to check.
            parameter_name (str): The name to show in alerts.
            min_value (int): The minimum value of the input to check.
            valid (bool): The previous state of valid.

        Returns:
            valid (boolean): The validity of the input (and those tested before).
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