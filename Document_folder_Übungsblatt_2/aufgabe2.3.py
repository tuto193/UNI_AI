import numpy as np
import matplotlib
matplotlib.use('Qt5Agg') # for PyCharm
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from copy import deepcopy

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
        
        freifeld=self.searchnull()
               
        if(direction=='up'):
            if freifeld[0]!=0:
                value=self.state[freifeld[0]-1,freifeld[1]]
                #Tauschen
                self.state[freifeld[0],freifeld[1]]=value
                self.state[freifeld[0]-1,freifeld[1]]=0
                self.history.append(direction)
                return True
         
        if(direction=='down'):
            if freifeld[0]!=2:
                value=self.state[freifeld[0]+1,freifeld[1]]
                #Tauschen
                self.state[freifeld[0],freifeld[1]]=value
                self.state[freifeld[0]+1,freifeld[1]]=0
                self.history.append(direction)
                return True
                
        if(direction=='left'):
            if freifeld[1]!=0:
                value=self.state[freifeld[0],freifeld[1]-1]
                #Tauschen
                self.state[freifeld[0],freifeld[1]]=value
                self.state[freifeld[0],freifeld[1]-1]=0
                self.history.append(direction)
                return True
                
        if(direction=='right'):
            if freifeld[1]!=2:
                value=self.state[freifeld[0],freifeld[1]+1]
                #Tauschen
                self.state[freifeld[0],freifeld[1]]=value
                self.state[freifeld[0],freifeld[1]+1]=0
                self.history.append(direction)
                return True
            
        return False
    
    
    def hashing(self,board):
        zeile1=board.state[0]
        zeile2=board.state[1]
        zeile3=board.state[2]
        
        hashsum=zeile1[0]*100000000+zeile1[1]*10000000+zeile1[2]*1000000+zeile2[0]*100000+zeile2[1]*10000+zeile2[2]*1000+zeile3[0]*100+zeile3[1]*10+zeile3[2]

        if hashsum in allstate:
            return False
        else:
            allstate.append(hashsum)
        return True
     
    
    def searchnull(self):
        pos=[]
        width=3
        for i in range(width):
            for j in range(width):
                if self.state[i,j]==0:
                    pos=[i,j]
        return pos             


    def solver(self,allboards=[]):
        print("Solver")
   
        vorgaenger=[]
        vorgaenger=deepcopy(allboards)
        allboards=[]
            
        if len(vorgaenger)==0:
            a1=deepcopy(self)
            a2=deepcopy(self)
            a3=deepcopy(self)
            a4=deepcopy(self)
            
            if a1.move('up')==True:
                allboards.append(a1)
                if a1.solved():
                    print("finish")
                    return True
             
            if a2.move('down')==True:
                allboards.append(a2)
                if a2.solved():
                    print("finish")
                    return True
            
            if a3.move('left')==True:
                allboards.append(a3)
                if a3.solved():
                    print("finish")
                    return True
     
            if a4.move('right')==True:
                allboards.append(a4)
                if a4.solved():
                    print("finish")
                    return True
      
        else:
            length=len(vorgaenger)
            print(len(vorgaenger))
            while length!=0:
                a1=deepcopy(vorgaenger[length-1])
                a2=deepcopy(vorgaenger[length-1])
                a3=deepcopy(vorgaenger[length-1])
                a4=deepcopy(vorgaenger[length-1])
                length=length-1

                if a1.move('up')==True:
                    if a1.hashing(a1)==True:
                        allboards.append(a1)
                    if a1.solved():
                        print("finish")
                        print(a1.state)
                        print(a1.history)
                        return True
             
                if a2.move('down')==True:
                    if a2.hashing(a2)==True:
                        allboards.append(a2)
                    if a2.solved():
                        print("finish")
                        print(a2.state)
                        print(a2.history)
                        return True
            
                if a3.move('left')==True:
                    if a3.hashing(a3)==True:
                        allboards.append(a3)
                    if a3.solved():
                        print("finish")
                        print(a3.state)
                        print(a3.history)
                        return True
     
                if a4.move('right')==True:
                    if a4.hashing(a4)==True:
                        allboards.append(a4)                
                    if a4.solved():
                        print("finish")
                        print(a4.state)
                        print(a4.history)
                        return True
         
        if self.solved():
            print("finish")
            return True
        
        self.solver(allboards)
        
        
if __name__ == "__main__":
    # main "function"
    b = Board(3)
    # plot initial state
    b.plot_state()

    global allstate
    allstate=[] 
    
    b.solver()
    
    if b.hashing(b)==True:
        print("hier")

    print(b.history) 
    plt.show(block=True)