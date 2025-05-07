from classes.interface import Interface
from services.persistence_handler import PersistenceHandler



"""this is main module where we call all the functions to do
"""
interface = Interface()

if __name__ == "__main__":

    interface.initialize_interface()
    interface.window.mainloop()