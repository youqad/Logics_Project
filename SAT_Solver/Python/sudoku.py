from latin_square import LatinSquare
from itertools import chain
from math import sqrt
import numpy as np

class Sudoku(LatinSquare):
    def __init__(self, *args, subgrids_size=3):
        assert args
        self.subgrids_size = subgrids_size
        square_dimensions = []
        reshaped_grids = []
        identifiers = []
        
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
            
            
        LatinSquare.__init__(self, *square_dimensions, prefix = 'sudoku', identifiers=identifiers)
        
        for index,n,grid in zip(range(len(self.outputs)), square_dimensions, reshaped_grids):
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
                                        self.outputs[index] += '-' + str(current_literal) + ' -' + \
                                        str(kn_squared+(subgrids_size*i+di2)*n+(subgrids_size*j+dj2)+1) + ' 0\n'
                                for dj2 in range(dj):
                                    self.outputs[index] += '-' + str(current_literal) + ' -' + \
                                    str(kn_squared+(subgrids_size*i+di)*n+(subgrids_size*j+dj2)+1) + ' 0\n'
            for i in range(n):
                for j in range(n):
                    if 1 <= grid[i,j] <= n:
                        self.outputs[index] += str((grid[i,j]-1)*n_squared+i*n+j+1) + ' 0\n'
            
    def show(self):
        LatinSquare.show(self, subgrids_size= self.subgrids_size)
                                            
            
        
    
    

L = Sudoku(('3040','0000','0000','0201'), ('0203','0100','0024','0000'), subgrids_size=2)
L.show()