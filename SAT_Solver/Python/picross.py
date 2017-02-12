from grid import Grid
import numpy as np


class Picross(Grid):
    def __init__(self, *args, prefix = 'picross', identifiers=[], examples_folder='../Examples/', color_map = ''):
        assert args
        dimensions = []
        identifiers = [] if not identifiers else identifiers
        new_identifiers = True if not identifiers else False

        for grid in args:

            if new_identifiers:
                identifier = ''.join(str(number) for row_col in grid for numbers in row_col for number in numbers)
                identifier = np.base_repr(int(identifier), 36)
                identifiers.append(identifier)

            x, y = len(grid[0]), len(grid[1])
            dimensions.append((x, y))

        Grid.__init__(self, *dimensions, prefix=prefix, identifiers=identifiers, original_grids=args, examples_folder=examples_folder, color_map=color_map)


    def generate_file(self, n, original_grid=None):
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

        subgrids_size = self.subgrids_size
        number_subgrids = n//subgrids_size
        n_squared = n**2

        for k in range(n):
            kn_squared = k*n_squared
            for i in range(number_subgrids):
                for j in range(number_subgrids):
                    for di in range(subgrids_size):
                        for dj in range(subgrids_size):
                            current_literal = kn_squared+(subgrids_size*i+di)*n+(subgrids_size*j+dj)+1
                            for di2 in range(di):
                                for dj2 in range(subgrids_size):
                                    output_str += '-' + str(current_literal) + ' -' + \
                                    str(kn_squared+(subgrids_size*i+di2)*n+(subgrids_size*j+dj2)+1) + ' 0\n'
                            for dj2 in range(dj):
                                output_str += '-' + str(current_literal) + ' -' + \
                                str(kn_squared+(subgrids_size*i+di)*n+(subgrids_size*j+dj2)+1) + ' 0\n'
        for i in range(n):
            for j in range(n):
                if 1 <= original_grid[i,j] <= n:
                    output_str += str((original_grid[i,j]-1)*n_squared+i*n+j+1) + ' 0\n'

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



# x = [[3], [2,1], [3,2], [2,2], [6], [1,5], [6], [1], [2]]
# y = [[1,2], [3,1], [1,5], [7,1], [5], [3], [4], [3]]