import os
from abc import ABC
from datetime import datetime

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class PersistenceHandler(ABC):

    load_dotenv()

    @classmethod
    def create_ddb(cls):
        try:
            conn = psycopg2.connect(dbname='postgres', user=os.getenv("POSTGRES_USER"), password=os.getenv("POSTGRES_PASSWORD"), host=os.getenv("POSTGRES_HOST"), port=os.getenv("POSTGRES_PORT"), client_encoding="UTF-8")
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # important pour CREATE DATABASE

            cursor = conn.cursor()
            cursor.execute(f'CREATE DATABASE "{os.getenv("POSTGRES_DB")}" ENCODING "UTF8"')
            print(f"Database '{os.getenv("POSTGRES_DB")}' created.")

            cursor.close()
            conn.close()

            conn = psycopg2.connect(dbname=os.getenv("POSTGRES_DB"), user=os.getenv("POSTGRES_USER"), password=os.getenv("POSTGRES_PASSWORD"), host=os.getenv("POSTGRES_HOST"), port=os.getenv("POSTGRES_PORT"), client_encoding="UTF-8")
            cursor = conn.cursor()

            simulation_table_creation_request = """CREATE TABLE simulation(
   simulation_id SMALLINT,
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
   global_life_expectancy NUMERIC(8,2)  ,
   fish_life_expectancy NUMERIC(8,2)  ,
   shark_life_expectancy NUMERIC(8,2)  ,
   total_reproduction SMALLINT,
   fish_reproduction SMALLINT,
   shark_reproduction SMALLINT,
   fishes_eaten SMALLINT,
   sharks_starved SMALLINT,
   total_deaths SMALLINT,
   PRIMARY KEY(simulation_id)
);"""
            cursor.execute(simulation_table_creation_request)
            conn.commit()

            simulation_detail_table_creation_request = """CREATE TABLE simulation_detail(
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
            cursor.execute(simulation_detail_table_creation_request)
            conn.commit()

            simulation_entities_table_creation_request = """CREATE TABLE simulation_entities(
   simulation_id SMALLINT,
   entity_id SMALLINT,
   is_alive BOOLEAN,
   age SMALLINT,
   species VARCHAR(50) ,
   children SMALLINT,
   fishes_eaten SMALLINT,
   PRIMARY KEY(simulation_id, entity_id)
);"""
            cursor.execute(simulation_entities_table_creation_request)
            conn.commit()

            cursor.close()
            conn.close()


        except psycopg2.errors.DuplicateDatabase:
            print(f"Database '{os.getenv("POSTGRES_DB")}' already exists.")
        except Exception as e:
            print(f"Error while creating database : {e}")

    @classmethod
    def connect_ddb(cls):
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            client_encoding = "UTF-8"
        )

        return conn

    @classmethod
    def load_data(cls):
        conn = cls.connect_ddb()

        try:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM simulation")
            return cursor.fetchall()

        except Exception as e:
            print(f"Error while reading database : {e}")

        finally:
            cursor.close()
            conn.close()

    @classmethod
    def save_data(cls, data):

        conn = cls.connect_ddb()

        try:
            cursor = conn.cursor()
            simulation_request = """
                INSERT INTO simulation (
                    simulation_id, simulation_date, duration, grid_height, grid_width,
                    fish_starting_population, shark_starting_population, fish_reproduction_time,
                    shark_reproduction_time, shark_starvation_time, shark_energy_gain, shuffled_entities,
                    animal_count, fish_count, shark_count, global_life_expectancy,
                    fish_life_expectancy, shark_life_expectancy, total_reproduction,
                    fish_reproduction, shark_reproduction, fishes_eaten, sharks_starved, total_deaths
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """

            values = (
                data["simulation_id"],
                data["date"],
                data["duration"],
                data["grid_height"],
                data["grid_width"],
                data["fish_starting_population"],
                data["shark_starting_population"],
                data["fish_reproduction_time"],
                data["shark_reproduction_time"],
                data["shark_starvation_time"],
                data["shark_energy_gain"],
                data["shuffle_entities"],
                data["animal_count"],
                data["fish_count"],
                data["shark_count"],
                data["life_expectancy"],
                data["fish_life_expectancy"],
                data["shark_life_expectancy"],
                data["total_reproduction"],
                data["fish_reproduction"],
                data["shark_reproduction"],
                data["fishes_eaten"],
                data["sharks_starved"],
                data['total_deaths']
            )

            cursor.execute(simulation_request, values)

            for chronon_data in data['detail']:
                simulation_detail_request = """
                    INSERT INTO simulation_detail (
                        simulation_id, chronon, animal_count, fish_count, shark_count, total_reproduction,
                        fish_reproduction, shark_reproduction, fishes_eaten, sharks_starved, total_deaths
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """

                values = (
                    data["simulation_id"],
                    chronon_data["chronon"],
                    chronon_data["animal_count"],
                    chronon_data["fish_count"],
                    chronon_data["shark_count"],
                    chronon_data["total_reproduction"],
                    chronon_data["fish_reproduction"],
                    chronon_data["shark_reproduction"],
                    chronon_data["fishes_eaten"],
                    chronon_data["sharks_starved"],
                    chronon_data['total_deaths']
                )

                cursor.execute(simulation_detail_request, values)

            for entity in data['entities']:
                simulation_entities_request = """
                    INSERT INTO simulation_entities (simulation_id, entity_id, is_alive, age, species, children, fishes_eaten)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """

                values = (
                    data["simulation_id"],
                    entity["entity_id"],
                    entity["is_alive"],
                    entity["age"],
                    entity["species"],
                    entity["children"],
                    entity["fishes_eaten"]
                )

                cursor.execute(simulation_entities_request, values)

            conn.commit()

        except Exception as e:
            print(f"Database error: {e}")

        finally:
            cursor.close()
            conn.close()

    @classmethod
    def get_next_simulation_id(cls):
        conn = PersistenceHandler.connect_ddb()

        try:
            cursor = conn.cursor()
            simulation_ids_request = "SELECT simulation_id FROM simulation ORDER BY simulation_id DESC LIMIT 1"
            cursor.execute(simulation_ids_request)
            results = cursor.fetchall()

            if not results:
                return 0
            else:
                return int(results[0][0]) + 1

        except Exception as e:
            print(f"Database error: {e}")

        finally:
            cursor.close()
            conn.close()
