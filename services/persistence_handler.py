import psycopg2
import settings

class Persistence_handler():
    def __init__(self):
        self.dbname = settings.DB_NAME
        self.user = settings.DB_USER
        self.password = settings.DB_PASSWORD
        self.host = settings.DB_HOST
        self.port = settings.DB_PORT

    def connect_db():
        try:
            conn = psycopg2.connect(
            dbname="nom_de_ta_bdd",
            user="ton_utilisateur",
            password="ton_mot_de_passe",
            host="localhost",
            port="5432"
            )
        except Exception as e:
            print()
