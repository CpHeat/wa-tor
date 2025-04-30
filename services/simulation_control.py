from settings import simulation_parameters


class SimulationControl:
    def __init__(self):
        self.simulation_duration = simulation_parameters['simulation_duration']
        self.simulation_status = "started"

    @classmethod
    def set_parameters(cls, grid_height_value, grid_width_value, simulation_length_value, fish_reproduction_time_value, shark_reproduction_time_value, shark_starvation_time_value, shark_starting_energy_value, shark_energy_gain_value, shark_starting_population_value, fish_starting_population_value, chronon_duration_value):
        simulation_parameters['grid_height_value'] = grid_height_value
        simulation_parameters['grid_width_value'] = grid_width_value
        simulation_parameters['simulation_length_value'] = simulation_length_value
        simulation_parameters['fish_reproduction_time_value'] = fish_reproduction_time_value
        simulation_parameters['shark_reproduction_time_value'] = shark_reproduction_time_value
        simulation_parameters['shark_starvation_time_value'] = shark_starvation_time_value
        simulation_parameters['shark_starting_energy_value'] = shark_starting_energy_value
        simulation_parameters['shark_energy_gain_value'] = shark_energy_gain_value
        simulation_parameters['shark_starting_population_value'] = shark_starting_population_value
        simulation_parameters['fish_starting_population_value'] = fish_starting_population_value
        simulation_parameters['chronon_duration_value'] = chronon_duration_value

    @classmethod
    def start_simulation(cls, grid_height_value, grid_width_value, simulation_length_value, fish_reproduction_time_value, shark_reproduction_time_value, shark_starvation_time_value, shark_starting_energy_value, shark_energy_gain_value, shark_starting_population_value, fish_starting_population_value, chronon_duration_value):
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
        planet = Planet()
        planet.check_entities()

    def pause_simulation(self):
        self.simulation_status = "paused"

    def stop_simulation(self):
        self.simulation_status = "stopped"