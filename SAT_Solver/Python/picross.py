from grid import Grid
import numpy as np


class LatinSquare(Grid):

    def __init__(self, *args, prefix = 'latin_square', identifiers =[], examples_folder='../Examples/', color_map = ''):
        Grid.__init__(self, *args, prefix='latin_square', identifiers=[], examples_folder='../Examples/', color_map='')

    @staticmethod
    def generate_file(n):
        # (k,i,j) is true iff the variable k is in position (i,j)
        # (k,i,j) corresponds to the literal number k*(n**2) + i*n + j + 1
        n_squared = n ** 2
        output_str = ''

        for k in range(n):
            for i in range(n):
                not_two_in_one_row = ''
                for j in range(n):
                    output_str += str(k * n_squared + i * n + j + 1) + ' '
                    for j2 in range(j):
                        not_two_in_one_row += '-' + str(k * n_squared + i * n + j2 + 1) + ' -' + str(
                            k * n_squared + i * n + j + 1) + ' 0\n'
                output_str += '0\n'
                output_str += not_two_in_one_row

        for k in range(n):
            for j in range(n):
                not_two_in_one_col = ''
                for i in range(n):
                    output_str += str(k * n_squared + i * n + j + 1) + ' '
                    for i2 in range(i):
                        not_two_in_one_col += '-' + str(k * n_squared + i2 * n + j + 1) + ' -' + str(
                            k * n_squared + i * n + j + 1) + ' 0\n'
                output_str += '0\n'
                output_str += not_two_in_one_col

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    output_str += str(k * n_squared + i * n + j + 1) + ' '
                output_str += '0\n'

        return output_str


    def generate_grid(self, n, valuation, ax):
        # valuation = output[7:-2].split(' || ')[:-1]
        # color_list = plt.cm.Set3(np.linspace(0, 1, n))
        # grid = np.zeros((n,n),dtype='f,f,f,f')
        # grid.fill((1.,1.,1.,1.))

        grid = np.zeros((n, n))

        for (k, i, j) in valuation:
            grid[i, j] = k + 1
            ax.text(j, i, str(k + 1), ha='center', va='center', weight='heavy', backgroundcolor=(1, 1, 1, 0.1))

        if self.subgrids_size:
            ax.xaxis.set_ticks([-0.5 + i * self.subgrids_size for i in range(n)])
            ax.yaxis.set_ticks([-0.5 + i * self.subgrids_size for i in range(n)])
            ax.grid(True)

        return grid