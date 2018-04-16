import numpy as np
import matplotlib
matplotlib.use('Qt5Agg') # for PyCharm
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class Pegboard(object):
    """
    A simple pegboard representation using a 2D numpy array.
    Fields with 0 are considered free, fields with 1 are considered occupied und fields with 2 are invalid fields (corner areas)
    """
    def __init__(self, size_outer=7, size_inner=3):
        """
        Constructor. Will initialize a board of the given size with a free space in the center.
        :param size_outer: the total size of the boards square
        :param size_inner: the width of boards "arms".
        """

        self.fig = None
        self.ax = None
        self.peg_circles = None
        self.board = self.__create_board(size_outer, size_inner)

    def __create_board(self, size_outer, size_inner):
        """
        Private helper method to initialize a board. Do not call from the outside.
        :param size_outer: the total size of the  boards square
        :param size_inner: the width of boards "arms".
        """
        board = np.ones((size_outer, size_outer), dtype=np.uint8)

        start_index = size_outer//2 - size_inner//2
        end_index = size_outer//2 + size_inner//2 + 1
        # set the corner areas in the array to 2 (invalid)
        board[0:start_index, 0:start_index] = 2
        board[end_index:, 0:start_index] = 2
        board[end_index:, end_index:] = 2
        board[0:start_index, end_index:] = 2

        # starting position in the center must be free (0)
        board[size_outer//2, size_outer//2] = 0

        return board

    def get_moves(self):
        """
        get all valid moves on the board as a list
        :return: List with all valid moves in the form:
              [(<coordinates of the jumping peg>, <coordinates of the jumped over peg>, <coordinates of the free space to jump to>]
        """

        # TODO Implement this!
        # This are the only valid moves!
        validMoves = [ "up", "right", "down", "left" ]
        moves = []
        for x in size_outer:
            for y in size_outer:

        return moves

    def move(self, move):
        """
        Executes the given move on the board. A valid move must be a list with 3 2D coordinates in the form:
            [(<coordinates of the jumping peg>, <coordinates of the jumped over peg>, <coordinates of the free space to jump to>].
            If the move is invalid or not possible on the board this method will raise a ValueError.
        :param move: a move in the form described above
        """
        if not self.valid_move(move):
            raise ValueError("Invalid move {0}".format(move))
        self.board[move[0]] = 0
        self.board[move[1]] = 0
        self.board[move[2]] = 1

    def valid_move(self, move):
        """
        Checks if the move is valid. Will raise a ValueError if the Format is invalid
        :param move: a move in the Format described in move()
        :return: True if the move is valid, False otherwise
        """
        if len(move) != 3:
            raise ValueError("A valid move requires 3 2D indices")

        if len(move[0]) != 2:
            raise ValueError("A valid move requires 2D indices")

        start = np.asarray(move[0])
        jumped = np.asarray(move[1])
        target = np.asarray(move[2])
        total_dist = np.sum(np.abs(start-jumped)) + np.sum(np.abs(jumped-target))
        if self.board[move[0]] != 1 or self.board[move[1]] != 1 or self.board[move[2]] != 0 or total_dist != 2:
            return False
        return True

    def finished(self):
        """
        Returns True if the game is finished (only one peg left on the board)
        :return: True if finished, False otherwise
        """
        return len(self.board[self.board == 1]) == 1

    def plot_state(self, interactive=True):
        """
        plots the current board state using matplotlib
        :param interactive: if True the function will reuse the plot from a previous call. If false a new plot will be generated for each call
        """
        if interactive:
            plt.ion()

        # if this is the first time this function is called
        if not interactive or self.fig is None:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111)

            # plot the board and ignore the peg positions
            colors = [(1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (0.0, 0.0, 0.0, 1.0)]
            cmap = LinearSegmentedColormap.from_list('Custom cmap', colors, 3)
            self.ax.clear()
            self.ax.imshow(self.board.T, cmap=cmap, interpolation='nearest')
            # Shift grid to be at 0.5, 1.5, etc
            locs = np.arange(self.board.shape[0])
            for axis in [self.ax.xaxis, self.ax.yaxis]:
                axis.set_ticks(locs + 0.5, minor=True)
                axis.set(ticks=locs, ticklabels=locs)
            self.ax.grid(True, which='minor')
        else:
            # just remove the previous peg positions
            for circ in self.peg_circles:
                circ.remove()
        # plot the peg positions as circles
        peg_rows, peg_cols = np.where(self.board.T == 1)
        self.peg_circles = []
        for pos in zip(peg_rows, peg_cols):
            circ = plt.Circle((pos), 0.4, color='black')
            circ.set_edgecolor('black')
            self.ax.add_artist(circ)
            self.peg_circles.append(circ)

        plt.draw()
        plt.pause(1e-6)


if __name__ == "__main__":
    # main "function"
    peg = Pegboard(9, 3)
    peg.plot_state()

    # just play a random game as an example
    while not peg.finished():
        # get current moves
        moves = peg.get_moves()
        if len(moves) == 0:
            print("game lost")
            break

        # make a random move
        make_move = np.random.randint(len(moves))
        print("making move", moves[make_move])
        peg.move(moves[make_move])

        # update the board state plot
        peg.plot_state()
    if peg.finished():
        print("game won!")

    print(peg.board)
    peg.plot_state()

    # keep the last figure
    plt.show(block=True)
