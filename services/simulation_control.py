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
    def set_parameters(cls, interface):
        simulation_parameters['grid_height'] = int(interface.grid_height_value.get())
        simulation_parameters['grid_width'] = int(interface.grid_width_value.get())
        simulation_parameters['simulation_length'] = int(interface.simulation_length_value.get())
        simulation_parameters['fish_reproduction_time'] = int(interface.fish_reproduction_time_value.get())
        simulation_parameters['shark_reproduction_time'] = int(interface.shark_reproduction_time_value.get())
        simulation_parameters['shark_starvation_time'] = int(interface.shark_starvation_time_value.get())
        simulation_parameters['shark_starting_energy'] = int(interface.shark_starting_energy_value.get())
        simulation_parameters['shark_starting_population'] = int(interface.shark_starting_population_value.get())
        simulation_parameters['fish_starting_population'] = int(interface.fish_starting_population_value.get())
        simulation_parameters['chronon_duration'] = int(interface.chronon_duration_value.get())

    @classmethod
    def start_simulation(cls, interface):
        cls.set_parameters(interface)

        interface.update_canvas()
        cls.planet = Planet(interface.follow_entities)
        cls._simulation_status = "playing"
        cls._i = 1
        cls.simulation_step(interface)

    @classmethod
    def simulation_step(cls, interface):
        if cls._simulation_status == "playing" and cls._i <= simulation_parameters['simulation_duration']:

            # wator_status = cls.planet.check_entities()
            # grid = wator_status['grid']
            interface.chronons_counter.config(text=cls._i)
            # interface.fish_nb_counter.config(text=wator_status['nb_fish'])
            # interface.shark_nb_counter.config(text=wator_status['nb_sharks'])
            #
            # interface.draw_wator(grid)
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
        interface.reset_canvas()