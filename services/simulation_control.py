from tkinter import NW

from PIL import Image, ImageTk

from classes.planet import Planet
from settings import simulation_parameters


class SimulationControl:
    _i = 1
    _simulation_status = "playing"
    _simulation_duration = simulation_parameters['simulation_duration']
    _planet = None

    def __init__(self):
        pass

    @classmethod
    def set_parameters(cls, grid_height_value, grid_width_value, simulation_length_value, fish_reproduction_time_value, shark_reproduction_time_value, shark_starvation_time_value, shark_starting_energy_value, shark_energy_gain_value, shark_starting_population_value, fish_starting_population_value, chronon_duration_value):
        simulation_parameters['grid_height'] = grid_height_value.get()
        simulation_parameters['grid_width'] = grid_width_value.get()
        simulation_parameters['simulation_length'] = simulation_length_value.get()
        simulation_parameters['fish_reproduction_time'] = fish_reproduction_time_value.get()
        simulation_parameters['shark_reproduction_time'] = shark_reproduction_time_value.get()
        simulation_parameters['shark_starvation_time'] = shark_starvation_time_value.get()
        simulation_parameters['shark_starting_energy'] = shark_starting_energy_value.get()
        simulation_parameters['shark_energy_gain'] = shark_energy_gain_value.get()
        simulation_parameters['shark_starting_population'] = shark_starting_population_value.get()
        simulation_parameters['fish_starting_population'] = fish_starting_population_value.get()
        simulation_parameters['chronon_duration'] = chronon_duration_value.get()

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

        cls.planet = Planet()
        cls._simulation_status = "playing"
        cls._i = 1
        cls.simulation_step(interface)

    @classmethod
    def simulation_step(cls, interface):
        if cls._simulation_status == "playing" and cls._i <= simulation_parameters['simulation_duration']:
            print("chronon", cls._i)
            grid = cls.planet.check_entities()
            interface.draw_wator(grid)
            cls._i += 1
            if cls._i < simulation_parameters['simulation_duration']-1:
                interface.window.after(simulation_parameters['chronon_duration'], lambda: cls.simulation_step(interface))


    @classmethod
    def pause_simulation(cls, interface):
        if cls._simulation_status == "playing":
            SimulationControl._simulation_status = "paused"
            interface.pause_button.config(text="Resume")
        elif cls._simulation_status == "paused":
            SimulationControl._simulation_status = "playing"
            interface.pause_button.config(text="Pause")
            cls.simulation_step(interface)


    @classmethod
    def stop_simulation(cls, interface):
        SimulationControl._simulation_status = "stopped"
        interface.reset_interface()