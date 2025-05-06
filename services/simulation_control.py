from classes.planet import Planet
from services.data_handler import DataHandler
from settings import simulation_parameters


class SimulationControl:
    """
    Controls the simulation and bridges the interface, the logic and the persistence system.

    Methods
    -------
    set_parameters: Sets the parameters of the simulation from the input values.
    start_simulation: Starts the simulation.
    simulation_step: Advances the simulation one step further.
    pause_simulation: Pauses the simulation.
    stop_simulation: Stops and resets the simulation.
    """
    current_chronon = 0
    throwback_chronon = 0
    _simulation_status = "playing"
    simulation_duration = simulation_parameters['simulation_duration']
    _planet = None

    @classmethod
    def set_parameters(cls, interface:'Interface') -> None:
        """
        Sets the parameters of the simulation from the input values.

        Parameters:
            interface (Interface): Interface class instance.
        """
        simulation_parameters['grid_height'] = int(interface.grid_height_value.get())
        simulation_parameters['grid_width'] = int(interface.grid_width_value.get())
        simulation_parameters['simulation_duration'] = int(interface.simulation_duration_value.get())
        simulation_parameters['fish_reproduction_time'] = int(interface.fish_reproduction_time_value.get())
        simulation_parameters['shark_reproduction_time'] = int(interface.shark_reproduction_time_value.get())
        simulation_parameters['shark_starvation_time'] = int(interface.shark_starvation_time_value.get())
        simulation_parameters['shark_energy_gain'] = int(interface.shark_energy_gain_value.get())
        simulation_parameters['shark_starting_population'] = int(interface.shark_starting_population_value.get())
        simulation_parameters['fish_starting_population'] = int(interface.fish_starting_population_value.get())
        simulation_parameters['chronon_duration'] = int(interface.chronon_duration_value.get())

        simulation_parameters['follow_entities'] = interface.follow_entities_value.get()
        simulation_parameters['shuffle_entities'] = interface.shuffle_entities_value.get()

    @classmethod
    def start_simulation(cls, interface:'Interface') -> None:
        """
        Starts the simulation.

        Parameters:
            interface (Interface): Interface class instance.
        """
        cls.set_parameters(interface)

        interface.reset_canvas()
        interface.update_canvas()
        DataHandler.reset_data()

        cls.planet = Planet()
        initial_data = {
            'entities': cls.planet.entities,
            'dead_fishes': cls.planet.dead_fishes,
            'dead_sharks': cls.planet.dead_sharks,
            'nb_fish': cls.planet.count_fish,
            'nb_shark': cls.planet.count_shark,
            'nb_reproduction_shark': cls.planet.count_reproduced_shark,
            'nb_reproduction_fish': cls.planet.count_reproduced_fish,
        }

        DataHandler.chronon_data_handling(0, initial_data)

        cls._simulation_status = "playing"
        cls.current_chronon = cls.throwback_chronon = 0
        interface.fish_nb_counter['text'] = cls.planet.count_fish
        interface.shark_nb_counter['text'] = cls.planet.count_shark

        interface.draw_wator(cls.planet.grid)
        interface.window.after(simulation_parameters['chronon_duration'], lambda: cls.simulation_step(interface))

    @classmethod
    def simulation_step(cls, interface:'Interface') -> None:
        """
        Advances the simulation one step further.

        Parameters:
            interface (Interface): Interface class instance.
        """
        if cls._simulation_status == "playing" and cls.current_chronon <= simulation_parameters['simulation_duration']:

            cls.current_chronon += 1
            cls.throwback_chronon = cls.current_chronon

            wator_status = cls.planet.check_entities()
            DataHandler.chronon_data_handling(cls.current_chronon, wator_status)
            grid = wator_status['grid']

            interface.chronons_counter['text'] = cls.current_chronon
            interface.fish_nb_counter['text'] = cls.planet.count_fish
            interface.shark_nb_counter['text'] = cls.planet.count_shark
            interface.throwback_chronon_label['text'] = cls.throwback_chronon

            interface.draw_wator(grid)

            if cls.current_chronon < simulation_parameters['simulation_duration']:
                interface.window.after(simulation_parameters['chronon_duration'], lambda: cls.simulation_step(interface))
            else:
                DataHandler.final_data_handling(wator_status)

    @classmethod
    def pause_simulation(cls, interface:'Interface') -> None:
        """
        Pauses the simulation.

        Parameters:
            interface (Interface): Interface class instance.
        """
        if cls._simulation_status == "playing":
            SimulationControl._simulation_status = "paused"
            interface.pause_button.config(text="Resume")
        elif cls._simulation_status == "paused":
            SimulationControl._simulation_status = "playing"
            interface.pause_button.config(text="Pause")
            cls.simulation_step(interface)

    @classmethod
    def stop_simulation(cls, interface:'Interface') -> None:
        """
        Stops and resets the simulation.

        Parameters:
            interface (Interface): Interface class instance.
        """
        cls._simulation_status = "stopped"
        cls.throwback_chronon = 0
        cls.current_chronon = 0
        DataHandler.reset_data()
        interface.chronons_counter['text'] = 0
        interface.fish_nb_counter['text'] = 0
        interface.shark_nb_counter['text'] = 0
        interface.throwback_chronon_label['text'] = 0
        interface.reset_canvas()