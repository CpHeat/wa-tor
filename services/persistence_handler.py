import os
from abc import ABC
from datetime import datetime

import psycopg2
from dotenv import load_dotenv


class PersistenceHandler(ABC):

    load_dotenv()

    @classmethod
    def connect_ddb(cls):
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
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
            print(f"Erreur lors de la lecture : {e}")

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
