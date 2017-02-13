from grid import Grid
import numpy as np
from urllib.request import urlopen


class Picross(Grid):
    """
    Picross game :

    Example
    Problem:                 Solution:

    . . . . . . . .  3       . # # # . . . .  3
    . . . . . . . .  2 1     # # . # . . . .  2 1
    . . . . . . . .  3 2     . # # # . . # #  3 2
    . . . . . . . .  2 2     . . # # . . # #  2 2
    . . . . . . . .  6       . . # # # # # #  6
    . . . . . . . .  1 5     # . # # # # # .  1 5
    . . . . . . . .  6       # # # # # # . .  6
    . . . . . . . .  1       . . . . # . . .  1
    . . . . . . . .  2       . . . # # . . .  2
    1 3 1 7 5 3 4 3          1 3 1 7 5 3 4 3
    2 1 5 1                  2 1 5 1
    The problem above could be represented by :

    L = [[[3], [2,1], [3,2], [2,2], [6], [1,5], [6], [1], [2]],
    [[1,2], [3,1], [1,5], [7,1], [5], [3], [4], [3]]]

    """
    def __init__(self, *args, prefix = 'picross', identifiers=[], examples_folder='../Examples/', color_map = ''):
        assert args
        dimensions = []
        identifiers, new_identifiers = ([], True) if not identifiers else (identifiers, False)
        grids = []

        for grid in args:
            if isinstance(grid, str):
                new_grid = []
                with urlopen(grid) as f:
                    # n : number of rows
                    # m : number of columns
                    n, m = int(next(f)), int(next(f))
                    dimensions.append((n, m))
                    rows_or_columns = []
                    for line in f:
                        if not line.strip():
                            new_grid.append(rows_or_columns)
                            rows_or_columns = []
                            continue
                        block = list(map(int, line.split()))
                        rows_or_columns.append(block)
                    else:
                        new_grid.append(rows_or_columns)
                grids.append(new_grid)
                formatted_grid = new_grid
            else:
                # n : number of rows
                # m : number of columns
                n, m = len(grid[0]), len(grid[1])
                dimensions.append((n, m))
                grids.append(grid)
                formatted_grid = grid

            if new_identifiers:
                identifier = ''.join(str(number) for row_col in formatted_grid for numbers in row_col for number in numbers)
                identifier = np.base_repr(int(identifier), 36)
                identifier = identifier[:100]
                identifiers.append(identifier)

        Grid.__init__(self, *dimensions, prefix=prefix, identifiers=identifiers, original_grids=grids, examples_folder=examples_folder, color_map=color_map)


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
                        if j+dj < len_row_or_col:
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




# P = Picross([[[3], [2,1], [3,2], [2,2], [6], [1,5], [6], [1], [2]], [[1,2], [3,1], [1,5], [7,1], [5], [3], [4], [3]]])
# P = Picross([[[6], [3, 1, 3], [1, 3, 1, 3], [3, 14], [1, 1, 1], [1, 1, 2, 2], [5, 2, 2], [5, 1, 1], [5, 3, 3, 3], [8, 3, 3, 3]], [[4], [4], [1, 5], [3, 4], [1, 5], [1], [4, 1], [2, 2, 2], [3, 3], [1, 1, 2], [2, 1, 1], [1, 1, 2], [4, 1], [1, 1, 2], [1, 1, 1], [2, 1, 2], [1, 1, 1], [3, 4], [2, 2, 1], [4, 1]]])
# P = Picross([[[5], [2, 3, 2], [2, 5, 1], [2, 8], [2, 5, 11], [1, 1, 2, 1, 6], [1, 2, 1, 3], [2, 1, 1], [2, 6, 2], [15, 4], [10, 8], [2, 1, 4, 3, 6], [17], [17], [18], [1, 14], [1, 1, 14], [5, 9], [8], [7]],
#              [[5], [3, 2], [2, 1, 2], [1, 1, 1], [1, 1, 1], [1, 3], [2, 2], [1, 3, 3], [1, 3, 3, 1], [1, 7, 2],
#               [1, 9, 1], [1, 10], [1, 10], [1, 3, 5], [1, 8], [2, 1, 6], [3, 1, 7], [4, 1, 7], [6, 1, 8], [6, 10],
#               [7, 10], [1, 4, 11], [1, 2, 11], [2, 12], [3, 13]]])

# P = Picross([[[1],[1,3],[3],[1,1],[1,1]], [[1],[3],[2],[5],[1]]])

# P = Picross([[[1, 7], [7], [2, 7], [2,2,1], [2,1,3], [2,1], [3,2], [4,2], [6,1], [4,1,3]],[[1,8], [8], [4], [5, 3], [4, 1,1], [3,1,2], [3,1], [3,1,1,1], [3,2,1], [4,1,2]]])

# P = Picross([[[3],[5],[4,3],[7],[5],[3],[5],[1,8],[3,3,3],[7,3,2],[5,4,2],[8,2],[10],[2,3],[6]],
# [[3],[4],[5],[4],[5],[6],[3,2,1],[2,2,5],[4,2,6],[8,2,3],[8,2,1,1],[2,6,2,1],[4,6],[2,4],[1]]])

# P = Picross("https://gist.githubusercontent.com/youqad/214e7df3f40dde0cfd467eb12a6d07c8/raw/124866402f84747ea5279c9fc95761778ddc484b/gistfile1.txt")
# P = Picross("https://gist.githubusercontent.com/youqad/1ac91abe875821461aa6e00673a19df9/raw/e703483bdd75563ce33c22b6b17fca35f5b844bf/gistfile1.txt")

# P = Picross("https://gist.githubusercontent.com/youqad/7f2bb172630a1cfff10f687e7e5ac7a3/raw/4cb2053dc1c2529a6a3df5178c8348abec1c97a8/gistfile1.txt")
# P =Picross("https://gist.githubusercontent.com/youqad/58a6fece57c5e15230145c1736255d5b/raw/ae46b1a40be232cf005c4d526cb2ae2291eb9ab1/gistfile1.txt")
# P = Picross("https://gist.githubusercontent.com/youqad/4f198642c89747703b7b63fd0905810d/raw/1892b9d8fd3b4ca7563e38db880a84caed8b1d31/gistfile1.txt")
# P = Picross("https://gist.githubusercontent.com/youqad/323eb0a573119d095fff60bce6fc9a38/raw/0d3308b2e7cd7560213f4014ee0244b0221a0152/gistfile1.txt")
# P = Picross("https://gist.githubusercontent.com/youqad/679798a979b25c96b467ba6da972a861/raw/1ed4abd272e2a7104ad10304cddf7abe6169a28d/gistfile1.txt")
# P = Picross("https://gist.githubusercontent.com/youqad/835a0943bbfef6a77b4c2fed3b1785f9/raw/413676fff3780666ef9eef846406bab528dce120/gistfile1.txt")

P = Picross("https://gist.githubusercontent.com/youqad/8d4d0a5da468243aae08a333c412f95c/raw/26ab2cbb906b0fbe0bfdc09dfdef8b43d0106857/gistfile1.txt")

# P = Picross("https://gist.githubusercontent.com/youqad/a94a6c5393e9570bcf105d609d28e635/raw/2683e7347b9d2bf633db632baa0f040945d87110/gistfile1.txt")

# P = Picross("https://gist.githubusercontent.com/youqad/e823bcd8d239a23833b20da9b5d0bbaf/raw/d60310e98c885fc6befa78ec40e4750bc3a485b4/gistfile1.txt")

# P = Picross("https://gist.githubusercontent.com/youqad/74f271fae6aa78d1646b6b02e60c6369/raw/3dec0764fd4d3c1b87882021d295b3924a2784ed/gistfile1.txt")


P.show()