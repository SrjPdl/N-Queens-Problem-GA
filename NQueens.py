import numpy as np
import matplotlib.pyplot as plt
class NQueens:
    '''
    Encapsulates N-Queens Problem
    '''
    def __init__(self, num_queens) -> None:
        '''
        Initialize the N-Queens Problem
        param:num_queens: number of queens to be placed on the board'''
        self.n_queens = num_queens

    def countViolations(self, solution: list) -> int:
        '''
        Count the number of violations in the given solution.
        param:solution: list of integers representing the positions of the queens on each row.
        '''
        n_violations = 0
        for i in range(len(solution)):
            for j in range(i+1, len(solution)):
                c1 = i
                r1 = solution[i]
                c2 = j
                r2 = solution[j]

                if abs(c1-c2) == abs(r1-r2):
                    n_violations += 1
        
        return n_violations
    
    def plot_board(self, solution: list) -> plt:
        '''
        Plots the board using matplotlib.
        param:solution: list of integers representing the positions of the queens on each row.
        '''

        board = np.zeros((self.n_queens, self.n_queens))
        board[::2, ::2] = 1
        board[1::2, 1::2] = 1
        plt.imshow(board, cmap='binary')
        queen = plt.imread("res/queen.png")
        for i,j in enumerate(solution):
            plt.imshow(queen, extent=(j-0.3,j + 0.3, i - 0.3, i + 0.3))
        plt.axis("image")
        plt.xticks(range(self.n_queens))
        plt.yticks(range(self.n_queens))

        return plt
    