from classes.interface import Interface
from services.persistence_handler import PersistenceHandler

interface = Interface()

if __name__ == "__main__":

    PersistenceHandler.get_next_simulation_id()
    # interface.initialize_interface()
    # interface.window.mainloop()