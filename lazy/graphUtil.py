class GraphUtil:

    # Imports matplotlib.
    # Returns True if succeed, prints message and returns false otherwise.
    @staticmethod
    def has_matplotlib():
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Please install matplotlib from www.matplotlib.org.")
            return False
        else:
            return True

    @staticmethod
    def has_mpi_interaction():
        try:
            import MpiInteraction as Mpi
        except ImportError:
            print("Please install MpiInteraction.")
            return False
        else:
            return True
