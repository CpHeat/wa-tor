# Default parameters
simulation_parameters = {
    # Grid size (width/height)
    'grid_width': 10,
    'grid_height': 10,
    # Sharks/Fishes number
    'shark_starting_population': 10,
    'fish_starting_population': 10,
    # Reproduction cycle duration
    'fish_reproduction_time': 5,
    'shark_reproduction_time': 5,
    # Sharks starvation time
    'shark_starvation_time': 3,
    # Starting energy of sharks
    'shark_starting_energy': 5,
    # Simulation duration (in chronons)
    'simulation_duration': 20,
    # Chronon duration (in ms)
    'chronon_duration': 500
}

# Cell size (in px)
CELL_SIZE = 50

DB_NAME = ""
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = "5432"