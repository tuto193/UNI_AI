import numpy as np
import matplotlib
matplotlib.use('Qt5Agg') # for PyCharm
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# global variables for the plot to conserve memory
fig = None
ax = None
texts = []
implot = None

class Board(object):
    def __init__(self, width=4, inputs=None):
        """
        Constructs a board object with the given width.
        :param width: width of the square board
        :param inputs: optional input values to intitialize the board. if None, the board is initialized with a random configuration
        """
        self.width = width
        if inputs is not None and len(inputs) != width**2:
            raise ValueError("number of input values must match a whole field")
        self.state = None
        self.__create_board(width, inputs)

        self.history = []

    def __eq__(self, other):
        """
        Comparison operator for equality. Will use the state attribute to compare the objects
        :param other: instance to compare this object to
        :return:
        """
        if isinstance(other, Board) and np.all(other.state == self.state):
            return True
        return False

    def __hash__(self):
        """
        Hash operator to store this object in a set()
        :return: a hash value
        """
        return hash(self.state.tostring())

    def plot_state(self, interactive=True):
        """
        plots the current board state using matplotlib
        :param interactive: if True the function will reuse the plot from a previous call. If false a new plot will be generated for each call
        """
        global fig
        global ax
        global texts
        global implot

        if interactive:
            plt.ion()

        # if this is the first time this function is called
        if not interactive or fig is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            colors = [(0.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0)]
            cmap = LinearSegmentedColormap.from_list('Custom cmap', colors,2)
            ax.clear()
            state = np.copy(self.state)
            state[state > 0] = 1
            implot = ax.imshow(state, cmap=cmap, interpolation='nearest')
            # Shift grid to be at 0.5, 1.5, etc
            locs = np.arange(state.shape[0])
            for axis in [ax.xaxis, ax.yaxis]:
                axis.set_ticks(locs + 0.5, minor=True)
                axis.set(ticks=[], ticklabels=[])
            ax.grid(True, which='minor')
        else:
            for t in texts:
                t.remove()
            texts.clear()
        for i in range(self.width):
            for j in range(self.width):
                c = self.state.T[i, j]
                texts.append(ax.text(i, j, str(c), va='center', ha='center', size=20))

        plt.draw()
        plt.pause(1e-3)

    def __create_board(self, width, inputs=None):
        """
        Creates and initializes a board of the given width. Private method, do not call from the outside
        :param width: the width of the board
        :param inputs: number of input values
        """
        if inputs is None:
            self.state = np.arange(1, width ** 2 + 1, dtype=np.uint8).reshape((width, width))
            self.state.flat[-1] = 0  # last field is 0 = empty
            # shuffle the board while not solvable

            while not self.solvable() or self.solved():
                np.random.shuffle(self.state.flat)

        else:
            self.state = np.asarray(inputs).reshape((width, width))
            if not self.solvable():
                raise ValueError("Board is not solvable!")


    def solved(self):
        """
        checks if the board has been solved
        :return: True if solved, False otherwise
        """
        goal = np.arange(1, self.width**2 + 1, dtype=np.uint8).reshape((self.width, self.width))
        goal.flat[-1] = 0
        if np.all(self.state == goal):
            return True
        return False

    def solvable(self):
        """
        Check if the puzzle is solvable by counting the number of inversions
        :return: True if solvable, False otherwise
        """

        inversions = 0
        s = self.state
        for i, v in enumerate(s[np.nonzero(s)]):
            j = i + 1
            while j < s.size:
                if s.flat[j] < v and s.flat[j] != 0:
                    inversions += 1
                j += 1
        size = s.shape[0]
        # grid width is odd and number of inversion even -> solvable
        if size % 2 != 0 and inversions % 2 == 0:
            return True
        # grid width is even
        if size % 2 == 0:
            emptyrow = size - np.where(self.state == 0)[0][0]
            return (emptyrow % 2 != 0) == (inversions % 2 == 0)
        return False

    def move(self, direction):
        """
        Apply a move in the given direction
        :param direction: direction as string out of ['up', 'down', 'left', 'right']
        :return: True if the move was successful, False otherwise
        """
        #Todo IMPLEMENT THIS!
        return False


if __name__ == "__main__":
    # main "function"
    b = Board(3)
    # plot initial state
    b.plot_state()
    # Todo CALL SOLVER HERE!

    # show the (solved) board
    plt.show(block=True)