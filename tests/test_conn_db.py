import psycopg2
from psycopg2 import sql, errors

# Database connection parameters
host = "localhost"
port = "5432"
user = "postgres"
password = "user"
new_db_name = "watorgame"

# Step 1: Connect to 'postgres' to create database
try:
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname="postgres"
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Try to create database
    try:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(new_db_name)
        ))
        print(f"Database '{new_db_name}' created successfully!")
    except errors.DuplicateDatabase:
        print(f"Database '{new_db_name}' already exists.")

    cur.close()
    conn.close()

except Exception as e:
    print(f"Error creating database: {e}")
    exit(1)

# Step 2: Connect to 'watorgame' database to create tables
try:
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=new_db_name
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Create tables
    simulation_table_creation_request = """CREATE TABLE IF NOT EXISTS simulation(
       simulation_id SMALLINT PRIMARY KEY,
       simulation_date TIMESTAMP,
       duration SMALLINT,
       grid_height SMALLINT,
       grid_width SMALLINT,
       fish_starting_population SMALLINT,
       shark_starting_population SMALLINT,
       fish_reproduction_time SMALLINT,
       shark_reproduction_time SMALLINT,
       shark_starvation_time SMALLINT,
       shark_energy_gain SMALLINT,
       shuffled_entities BOOLEAN,
       animal_count SMALLINT,
       fish_count SMALLINT,
       shark_count SMALLINT,
       global_life_expectancy NUMERIC(8,2),
       fish_life_expectancy NUMERIC(8,2),
       shark_life_expectancy NUMERIC(8,2),
       total_reproduction SMALLINT,
       fish_reproduction SMALLINT,
       shark_reproduction SMALLINT,
       fishes_eaten SMALLINT,
       sharks_starved SMALLINT,
       total_deaths SMALLINT
    );"""
    cur.execute(simulation_table_creation_request)
    print(" Table 'simulation' created or already exists.")

    simulation_detail_table_creation_request = """CREATE TABLE IF NOT EXISTS simulation_detail(
       simulation_id SMALLINT,
       chronon SMALLINT,
       animal_count SMALLINT,
       fish_count SMALLINT,
       shark_count SMALLINT,
       total_reproduction SMALLINT,
       fish_reproduction SMALLINT,
       shark_reproduction SMALLINT,
       fishes_eaten SMALLINT,
       sharks_starved SMALLINT,
       total_deaths SMALLINT,
       PRIMARY KEY(simulation_id, chronon)
    );"""
    cur.execute(simulation_detail_table_creation_request)
    print("Table 'simulation_detail' created or already exists.")

    simulation_entities_table_creation_request = """CREATE TABLE IF NOT EXISTS simulation_entities(
       simulation_id SMALLINT,
       entity_id SMALLINT,
       is_alive BOOLEAN,
       age SMALLINT,
       species VARCHAR(50),
       children SMALLINT,
       fishes_eaten SMALLINT,
       PRIMARY KEY(simulation_id, entity_id)
    );"""
    cur.execute(simulation_entities_table_creation_request)
    print(" Table 'simulation_entities' created or already exists.")

    cur.close()
    conn.close()

except Exception as e:
    print(f" Error creating tables: {e}")
