from latin_square import LatinSquare
from itertools import chain
from math import sqrt
import numpy as np
from random import sample

class Sudoku(LatinSquare):
    """
    Sudoku game : a Latin Square in which each number appears only once in each subgrid*subgrid block

    """
    def __init__(self, *args, subgrids_size=3, examples_folder='../Examples/', color_map = '', random=None, solvable=True):
        assert args
        self.subgrids_size = subgrids_size
        square_dimensions = []
        reshaped_grids = []
        identifiers = []

        if random:
            args = (grid for grid in self.random(*args, param=random, solvable=solvable))

        for grid in args:
            reshaped_grid = []
            identifier = ''
            
            number_coefficients = 0
            for coeff in chain.from_iterable(grid):
                number_coefficients+=1
                reshaped_grid.append(int(coeff))
                
            dimension = sqrt(number_coefficients)
            
            for coeff in chain.from_iterable(grid):
                if identifier or 1<= int(coeff) <= dimension:
                    if not (1<= int(coeff) <= dimension):
                        coeff = 0
                    identifier += str(coeff)
            
            assert dimension == int(dimension)
            assert dimension/subgrids_size == int(dimension/subgrids_size)
            
            dimension = int(dimension)
            square_dimensions.append(dimension)
            
            reshaped_grid = np.array(reshaped_grid).reshape((dimension, dimension))
            reshaped_grids.append(reshaped_grid)
            
            identifier = np.base_repr(int(identifier),36)
            identifiers.append(identifier)
            
        print(reshaped_grids)
        print(square_dimensions)
        LatinSquare.__init__(self, *square_dimensions, prefix = 'sudoku', identifiers=identifiers, original_grids = reshaped_grids,
                             examples_folder=examples_folder, color_map=color_map)

    def generate_file(self, n, original_grid=None, verbose = False):
        output_str = LatinSquare.generate_file(self, n, original_grid)
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

    def random(self, *args, param=27, solvable=True):
        if isinstance(param, int):
            for n in args:
                yield self.random_sudoku(n, param, solvable)

    @staticmethod
    def random_sudoku(n, number_of_fixed_coeff, solvable = True):
        """
        Return a randomly filled n*n Sudoku grid.
        The "solvable" option ensures there exists a solution, since a completeley filled Sudoku grid is generated
        before erasing n*n-number_of_fixed_coeff numbers.
        """
        grid = [[None for i in range(n)] for j in range(n)]
        m = sqrt(n)
        assert int(m) == m
        m = int(m)

        not_erased_coefficients = set(sample([(i,j) for i in range(n) for j in range(n)], number_of_fixed_coeff))

        def grid_filled_up_to(i = 0, j =0):
            i_current_block_origin, j_current_block_origin = m*(i//m), m*(j//m)
            random_numbers  = sample(list(range(1, n + 1)), n)
            if solvable or (i,j) in not_erased_coefficients:
                for k in random_numbers:
                    if k not in grid[i] and k not in [row[j] for row in grid] \
                            and k not in [row_block for row in grid[i_current_block_origin:i]
                                          for row_block in row[j_current_block_origin:j_current_block_origin+m]]:
                        grid[i][j] = k
                        if (i, j) == (n-1, n-1):
                            return grid
                        next_position = (i, j + 1) if j <= n - 2 else (i + 1, 0)
                        if grid_filled_up_to(*next_position) is not None:
                            return grid
                # No number can be put in this position : let's backtrack
                grid[i][j] = None
                return None
            else:
                grid[i][j] = 0
                if (i, j) == (n-1, n-1):
                    return grid
                next_position = (i, j + 1) if j <= n - 2 else (i + 1, 0)
                if grid_filled_up_to(*next_position) is not None:
                    return grid
                grid[i][j] = None
                return None

        grid = grid_filled_up_to()
        return ''.join((str(grid[i][j]) if (i,j) in not_erased_coefficients else '0') for i in range(n) for j in range(n))



            
    
    # Normal << Very Difficult < Evil < Excessive < Egregious < Excruciating < Extreme
    # http://www.extremesudoku.info/sudoku.html Monday, 30th January 2017
    
    # Normal :  ('700020005','600710000','000005907','030080740','006000100','049060020','903100000','000053001','500090002')
    # ('645000000','000240600','008001007','002005009','000000000','010300200','380970021','720050000','000000080')
    # Very Difficult : ('620900800','008200090','070608300','000002405','000000000','305400000','009307040','040009100','007004062')
    #                  ('000380050','200460900','05300006','030000800','608000203','001000090','300000520','002043007','070021000')
    # Evil : ('700000003','020903060','003010200','050601090','009000100','030409050','008030600','060208040','200000009')
    # Excessive: ('500200106','001009000', '020010009', '100300070','004000200', '060005003','400050010','000700300','308001004')
    # Egregious : ('906010500','080090070','005006001','000400100','690080035','001002000','200300800','030020040','009040302')
    # Excruciating : ('400090003','000304000','007080400','070000090','601050807','090000060','002070300','000506000', '800010002')
    # Extreme : ('800050007', '000302000','004090300', '020000090', '705080401', '010000060', '003070600', '000409000', '100060005')
    
    # Easy : ('020390506','607100400','509672000','900000210','000000000','052000004','000836107','005009602','806025040')
    # '306720589080500000009000002503002046700903005860400901400000300000004010928017604'
    # Medium : '091300050080054100000060090010006003006000800500400060040070000009130020060008710'
    

G = Sudoku(('700020005','600710000','000005907','030080740','006000100','049060020','903100000','000053001','500090002'), ('620900800','008200090','070608300','000002405','000000000','305400000','009307040','040009100','007004062'), subgrids_size=3)
# G.show()


L = Sudoku('091300050080054100000060090010006003006000800500400060040070000009130020060008710', subgrids_size=3)
# L.show()

M = Sudoku(9, random=37, solvable=False)
# M.show()


N = Sudoku(9, random=27, solvable=True)
N.show()
