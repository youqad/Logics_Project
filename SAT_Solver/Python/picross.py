from grid import Grid
import numpy as np


class Picross(Grid):
    def __init__(self, *args, prefix = 'picross', identifiers=[], examples_folder='../Examples/', color_map = ''):
        assert args
        dimensions = []
        identifiers, new_identifiers = ([], True) if not identifiers else (identifiers, False)

        for grid in args:

            if new_identifiers:
                identifier = ''.join(str(number) for row_col in grid for numbers in row_col for number in numbers)
                identifier = np.base_repr(int(identifier), 36)
                identifiers.append(identifier)

            x, y = len(grid[0]), len(grid[1])
            dimensions.append((x, y))

        Grid.__init__(self, *dimensions, prefix=prefix, identifiers=identifiers, original_grids=args, examples_folder=examples_folder, color_map=color_map)


    def generate_file(self, dimensions, original_grid=None, verbose = True):
        # n : rows / m : columns
        # Cells  : (i,j) is true iff the cell in position (i,j) is black
        #                -> associated with the literal 1 <= i*max(n,m) + j <= max(n,m)**2
        # Blocks : (k,i,j) is true iff the i-th block of the k-th sequence (= row OR column) starts from the j-th position
        #                 -> associated with the literal max(n,m)**2+1 <= max(n,m)**2 + k*(m+n)**2 + i*(m+n) + j + 1 <= (m+n)**3 + max(n,m)**2 + 1
        n, m = dimensions
        max_dim = max(n,m)
        n_plus_m = n+m
        max_dim_squared = max_dim**2
        n_plus_m_squared = (n+m)**2


        output_str = ''

        flattened_grid = [block for sequence in original_grid for block in sequence]


        for k in range(n_plus_m):
            len_sequence = len(flattened_grid[k])
            len_row_or_col = m if k < n else n

            for i in range(len_sequence):
                lower_bound = sum(flattened_grid[k][i2]+1 for i2 in range(i))
                upper_bound = len_row_or_col-(sum(flattened_grid[k][i2]+1 for i2 in range(i,len_sequence))-2)

        ########################
        # BLOCKS
        ########################

        # for each sequence (=row or column), the i-th block is somewhere

                verbose_comment = 'c '
                for j in range(lower_bound,upper_bound):
                    output_str += str(max_dim_squared + k*n_plus_m_squared + i*n_plus_m + j + 1) + ' '
                    if verbose:
                        verbose_comment += str((k, i, j)) + ' or '
                output_str += '0\n'
                if verbose:
                    output_str += verbose_comment[:-4] + '\n'

        # for each sequence (=row or column), the i-th block is at one position at most
                for j in range(lower_bound,upper_bound):
                    for j2 in range(lower_bound, j):
                        output_str += '-' + str(max_dim_squared + k*n_plus_m_squared + i*n_plus_m + j + 1) + ' -' \
                                      + str(max_dim_squared + k*n_plus_m_squared + i*n_plus_m + j2 + 1) + ' 0\n'
                        if verbose:
                            output_str += 'c ' + str((k, i, j)) + ' => not ' +  str((k, i, j2)) + '\n'

        # for each sequence (=row or column), two successive blocks don't overlap, and are separated by at least 1 cell
                if i < len_sequence-1:
                    for j in range(lower_bound,upper_bound):
                        for dj in range(flattened_grid[k][i]+1):
                            if j+dj < len_row_or_col:
                                output_str += '-' + str(max_dim_squared + k*n_plus_m_squared + i*n_plus_m + j + 1) + ' -' \
                                              + str(max_dim_squared + k*n_plus_m_squared + (i+1)*n_plus_m + j+dj +1) + ' 0\n'
                                if verbose:
                                    output_str += 'c ' + str((k, i, j)) + ' => not ' + str((k, i+1, j+dj)) + '\n'

        ########################
        # CELLS
        ########################

        # each cell of each block is colored
                for j in range(lower_bound, upper_bound):
                    for dj in range(flattened_grid[k][i]+1):
                        not_colored = True if dj == flattened_grid[k][i] else False

                        output_str += '-' + str(max_dim_squared + k * n_plus_m_squared + i * n_plus_m + j + 1) \
                                      + (' -' if not_colored else ' ')  + str(
                            1 + ((k * max_dim + j + dj) if k < n else ((j + dj) * max_dim + (k - n)))) \
                                      + ' 0\n'
                        if verbose:
                            output_str += 'c ' + str((k, i, j)) + ' => ' + (' not ' if not_colored else '') \
                                          + str((k,j+dj) if k<n else (j+dj, k-n)) + '\n'


        for i in range(n):
            for j in range(m):
        # each colored cell is in one block of its row
                verbose_comment = 'c '+ str((i,j)) + ' => '
                output_str += '-' + str(i * max_dim + j + 1)

                for i2 in range(len(flattened_grid[i])):
                    for di2 in range(flattened_grid[i][i2]):
                        len_sequence = len(flattened_grid[i])
                        len_row_or_col = m
                        lower_bound = sum(flattened_grid[i][i3] + 1 for i3 in range(i2))
                        upper_bound = len_row_or_col - (
                        sum(flattened_grid[i][i3] + 1 for i3 in range(i2, len_sequence)) - 2)

                        if lower_bound <= j - di2 < upper_bound:
                            if verbose:
                                verbose_comment += str((i, i2, j-di2)) + ' or '
                            output_str += ' ' + str(max_dim_squared + i*n_plus_m_squared + i2*n_plus_m + j-di2 + 1)
                output_str += ' 0\n'
                if verbose:
                    output_str += verbose_comment[:-4] + '\n'


        # each colored cell is in one block of its column
                verbose_comment = 'c '+ str((i,j)) + ' => '
                output_str += '-' + str(i * max_dim + j + 1)

                for j2 in range(len(flattened_grid[j+n])):
                    for dj2 in range(flattened_grid[j+n][j2]):
                        len_sequence = len(flattened_grid[j+n])
                        len_row_or_col = n
                        lower_bound = sum(flattened_grid[j+n][j3] + 1 for j3 in range(j2))
                        upper_bound = len_row_or_col - (
                        sum(flattened_grid[j+n][j3] + 1 for j3 in range(j2, len_sequence)) - 2)

                        if lower_bound <= i - dj2 < upper_bound:
                            if verbose:
                                verbose_comment += str((j+n, j2, i-dj2)) + ' or '
                            output_str += ' ' + str(max_dim_squared + (j+n)*n_plus_m_squared + j2*n_plus_m + i-dj2 + 1)
                output_str += ' 0\n'
                if verbose:
                    output_str += verbose_comment[:-4] + '\n'

        return output_str


    def generate_grid(self, dimensions, valuation, ax, original_grid = None):

        n, m = dimensions
        grid = np.zeros((n, m))

        for (i, j) in valuation:
            grid[i, j] = 1

        return grid

    @staticmethod
    def decode_literals(dimensions, l):
        n, m = dimensions
        if int(l) <= max(n, m)**2:
            N = max(n, m)
            return (((int(l) - 1) // N) % N, (int(l) - 1) % N)
        else:
            # N = n+m
            # return (((int(l) - 1) // (N ** 2)) % N, ((int(l) - 1) // N) % N, (int(l) - 1) % N)
            return None



# x = [[3], [2,1], [3,2], [2,2], [6], [1,5], [6], [1], [2]]
# y = [[1,2], [3,1], [1,5], [7,1], [5], [3], [4], [3]]


# P = Picross([[[3], [2,1], [3,2], [2,2], [6], [1,5], [6], [1], [2]], [[1,2], [3,1], [1,5], [7,1], [5], [3], [4], [3]]])
P = Picross([[[6], [3, 1, 3], [1, 3, 1, 3], [3, 14], [1, 1, 1], [1, 1, 2, 2], [5, 2, 2], [5, 1, 1], [5, 3, 3, 3], [8, 3, 3, 3]], [[4], [4], [1, 5], [3, 4], [1, 5], [1], [4, 1], [2, 2, 2], [3, 3], [1, 1, 2], [2, 1, 1], [1, 1, 2], [4, 1], [1, 1, 2], [1, 1, 1], [2, 1, 2], [1, 1, 1], [3, 4], [2, 2, 1], [4, 1]]])
# P = Picross([[[2, 1],[1, 1],[3],[1, 1],[1, 1],[2],[1, 1],[1, 2],[2]], [[2, 1],[2, 1, 3],[7],[1, 3],[2, 1]]])
print(P.original_grids)
print(P.file_names)
P.show()