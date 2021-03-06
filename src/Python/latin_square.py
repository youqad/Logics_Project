from grid import Grid
import numpy as np


class LatinSquare(Grid):
    """
    Latin Square logic game : given a size n, build a n*n numbered grid in which a given appears only once in each row
    and column
    """

    def __init__(self, *args, prefix = 'latin_square', identifiers =[], original_grids = [], examples_folder='../Examples/',
                 color_map = ''):
        Grid.__init__(self, *args, prefix = prefix, identifiers = identifiers,  original_grids =  original_grids,
                      examples_folder = examples_folder, color_map = color_map)

    def generate_file(self, n, original_grid=None, verbose = False):
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


    def generate_grid(self, n, valuation, ax, original_grid = None):
        grid = np.zeros((n, n))

        for (k, i, j) in valuation:
            grid[i, j] = k + 1
            if original_grid is not None and 1 <= original_grid[i,j] <= n:
                ax.text(j, i, str(k + 1), ha='center', va='center', weight='extra bold', backgroundcolor=(1, 1, 1, 0.1))
            else:
                ax.text(j, i, str(k + 1), ha='center', va='center', style='italic', backgroundcolor=(1, 1, 1, 0.1))

        try:
            ax.xaxis.set_ticks([-0.5 + i * self.subgrids_size for i in range(n)])
            ax.yaxis.set_ticks([-0.5 + i * self.subgrids_size for i in range(n)])
            ax.grid(True)
        except AttributeError:
            pass

        return grid

    @staticmethod
    def decode_literals(n, l):
        return (((int(l) - 1) // (n ** 2)) % n, ((int(l) - 1) // n) % n, (int(l) - 1) % n)

