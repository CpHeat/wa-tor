from classes.interface import Interface
from services.persistence_handler import PersistenceHandler

interface = Interface()

if __name__ == "__main__":

    # PersistenceHandler.save_data()
    interface.initialize_interface()
    interface.window.mainloop()