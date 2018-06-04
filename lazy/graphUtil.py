#import matplotlib.pyplot as plt
#from mpl_interaction import PanAndZoom as Pan


class GraphUtil:

    @staticmethod
    def has_matplotlib():
        """ Imports matplotlib.
        :return: Returns True if succeed, prints message and returns false otherwise.
        :rtype: bool
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Please install matplotlib from www.matplotlib.org.")
            return False
        else:
            return True

    @staticmethod
    def has_mpl_interaction():
        """ Imports MplInteraction.
        :return: Returns True if succeed, prints message and returns false otherwise.
        :rtype: bool
        """
        try:
            from .mpl_interaction import PanAndZoom as Pan
        except ImportError:
            print("Please install MpiInteraction.")
            return False
        else:
            return True

    @staticmethod
    def bar(label, value, label_name=None, value_name=None, title=None):
        """Draws the bar diagram.
        No graph is drawn if matplotlib is not installed.
        The graph cannot be dragged and zoomed by mouse if MpiInteraction not installed.
        """
        if not GraphUtil.has_matplotlib():
            return
        fig, ax = plt.subplots()
        ax.bar(label, value)
        if not label_name is None:
            plt.xlabel(label_name)
        if not value_name is None:
            plt.ylabel(value_name)
        if not title is None:
            plt.suptitle(title)
        if not GraphUtil.has_mpl_interaction():
            pan_zoom = Pan(fig)
        plt.show()
