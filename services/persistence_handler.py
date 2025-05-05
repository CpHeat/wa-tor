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
    def load_ddb(cls):

        conn = cls.connect_ddb()

        try:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM simulation")
            resultats = cursor.fetchall()

            print("Contenu de la base :")
            for ligne in resultats:
                print(ligne)

        except Exception as e:
            print(f"Erreur lors de la lecture : {e}")

        finally:
            cursor.close()
            conn.close()

    @classmethod
    def save_data(cls):
        """
        """

        data = {
            "simulation_id": 0,
            "date": datetime.now(),
            "duration": 50,
            "grid_height": 10,
            "grid_width": 10,
            "animal_count": 54,
            "fish_count": 12,
            "shark_count": 47,
            "life_expectancy": 2.87,
            "fish_life_expectancy": 5.87,
            "shark_life_expectancy": 6.51,
            "reproduction": 10,
            "fish_reproduction": 7,
            "shark_reproduction": 5,
            "fish_eaten": 45,
            "shark_starved": 23,
            "detail": [
                {
                    "chronon": 1,
                    "animal_count": 14,
                    "fish_count": 75,
                    "shark_count": 54,
                    "reproduction": 5,
                    "fish_reproduction": 4,
                    "shark_reproduction":3,
                    "fish_eaten": 14,
                    "shark_starved": 57,
                },
                {
                    "chronon": 2,
                    "animal_count": 58,
                    "fish_count": 45,
                    "shark_count": 1,
                    "reproduction": 7,
                    "fish_reproduction": 3,
                    "shark_reproduction": 8,
                    "fish_eaten": 145,
                    "shark_starved": 87,
                }
            ]
        }

        conn = cls.connect_ddb()

        try:
            cursor = conn.cursor()
            simulation_request = """
                INSERT INTO simulation (
                    simulation_id, date, duration, grid_height, grid_width,
                    animal_count, fish_count, shark_count, life_expectancy,
                    fish_life_expectancy, shark_life_expectancy, reproduction,
                    fish_reproduction, shark_reproduction, fish_eaten, shark_starved
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """

            values = (
                data["simulation_id"],
                data["date"],
                data["duration"],
                data["grid_height"],
                data["grid_width"],
                data["animal_count"],
                data["fish_count"],
                data["shark_count"],
                data["life_expectancy"],
                data["fish_life_expectancy"],
                data["shark_life_expectancy"],
                data["reproduction"],
                data["fish_reproduction"],
                data["shark_reproduction"],
                data["fish_eaten"],
                data["shark_starved"]
            )

            cursor.execute(simulation_request, values)

            for chronon_data in data['detail']:
                simulation_detail_request = """
                    INSERT INTO simulation_detail (
                        simulation_id, chronon, animal_count, fish_count, shark_count, reproduction,
                        fish_reproduction, shark_reproduction, fish_eaten, shark_starved
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """

                values = (
                    data["simulation_id"],
                    chronon_data["chronon"],
                    chronon_data["animal_count"],
                    chronon_data["fish_count"],
                    chronon_data["shark_count"],
                    chronon_data["reproduction"],
                    chronon_data["fish_reproduction"],
                    chronon_data["shark_reproduction"],
                    chronon_data["fish_eaten"],
                    chronon_data["shark_starved"]
                )

                cursor.execute(simulation_detail_request, values)

            conn.commit()

        except Exception as e:
            print(f"Database error: {e}")

        finally:
            cursor.close()
            conn.close()