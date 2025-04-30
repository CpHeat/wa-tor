from tkinter import NW

from PIL import Image, ImageTk

from settings import simulation_parameters


class SimulationControl:
    _simulation_status = "playing"
    _simulation_duration = simulation_parameters['simulation_duration']

    def __init__(self):
        pass

    @classmethod
    def set_parameters(cls, grid_height_value, grid_width_value, simulation_length_value, fish_reproduction_time_value, shark_reproduction_time_value, shark_starvation_time_value, shark_starting_energy_value, shark_energy_gain_value, shark_starting_population_value, fish_starting_population_value, chronon_duration_value):
        simulation_parameters['grid_height_value'] = grid_height_value.get()
        simulation_parameters['grid_width_value'] = grid_width_value.get()
        simulation_parameters['simulation_length_value'] = simulation_length_value.get()
        simulation_parameters['fish_reproduction_time_value'] = fish_reproduction_time_value.get()
        simulation_parameters['shark_reproduction_time_value'] = shark_reproduction_time_value.get()
        simulation_parameters['shark_starvation_time_value'] = shark_starvation_time_value.get()
        simulation_parameters['shark_starting_energy_value'] = shark_starting_energy_value.get()
        simulation_parameters['shark_energy_gain_value'] = shark_energy_gain_value.get()
        simulation_parameters['shark_starting_population_value'] = shark_starting_population_value.get()
        simulation_parameters['fish_starting_population_value'] = fish_starting_population_value.get()
        simulation_parameters['chronon_duration_value'] = chronon_duration_value.get()

    @classmethod
    def start_simulation(cls, interface, grid_height_value, grid_width_value, simulation_length_value, fish_reproduction_time_value, shark_reproduction_time_value, shark_starvation_time_value, shark_starting_energy_value, shark_energy_gain_value, shark_starting_population_value, fish_starting_population_value, chronon_duration_value):

        cls.set_parameters(
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
        )


        while SimulationControl._simulation_status != "stopped":

            i = 0

            while i < simulation_parameters['simulation_duration']:
                planet.check_entities()
                i += 1


        # planet = Planet()
        # planet.check_entities()
        grid = [
            ["shark", None, None, None, None, "shark", None, None, "fish", "fish"],
            [None, None, "fish", None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, "shark", None],
            [None, "shark", None, None, None, "fish", None, None, None, None],
            [None, None, None, None, "fish", None, None, None, None, None],
            [None, None, None, None, None, None, None, None, "fish", None],
            [None, "fish", None, None, "shark", None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, "shark", None, None, "fish", None, "shark", None, None],
            ["fish", None, None, None, None, None, None, None, None, "fish"],
        ]

        interface.draw_wator(grid)

    def pause_simulation(self):
        self.simulation_status = "paused"

    def stop_simulation(self):
        self.simulation_status = "stopped"