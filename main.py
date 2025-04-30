from classes.interface import Interface

interface = None

if __name__ == "__main__":

    interface = Interface()
    interface.initialize_interface()

    interface.window.mainloop()