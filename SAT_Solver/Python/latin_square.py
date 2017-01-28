from subprocess import check_output
from matplotlib import pyplot as plt
import numpy as np


class LatinSquare():
    
    _created_files = False
    
    def __init__(self, *args):
        assert args
        self.file_names = []
        self.outputs = []
        self.square_dimensions = args
        
        for n in args:
            file_name = 'latin_square_' + str(n) + '.txt'
            self.file_names.append(file_name)
            output_str = ''
            d = {}
            count = 1
            
            for k in range(n):
                for i in range(n):
                    not_two_in_one_row = ''
                    for j in range(n):
                        d[(k,i,j)] = count
                        output_str += str(count) + ' '
                        count +=1
                        for j2 in range(j):
                            not_two_in_one_row += '-' + str(d[(k,i,j2)]) + ' -' + str(count) + ' 0\n'
                    output_str += '0\n'
                    output_str += not_two_in_one_row
                    
            for k in range(n):
                for j in range(n):
                    not_two_in_one_col = ''
                    for i in range(n):
                        output_str += str(d[(k,i,j)]) + ' '
                        for i2 in range(i):
                            not_two_in_one_col += '-' + str(d[(k,i2,j)]) + ' -' + str(d[(k,i,j)]) + ' 0\n'
                    output_str += '0\n'
                    output_str += not_two_in_one_col
    
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        output_str += str(d[(k,i,j)]) + ' '
                    output_str += '0\n'
                    
            self.outputs.append(output_str)
            
    def __iter__(self):
        for output in self.outputs:
            yield output
            
        
    def create_files(self):
        for n, file_name, output in zip(self.square_dimensions, self.file_names, self.outputs):
            with open(file_name, 'w') as f:
                f.write('c Latin Square CNF file python generated.\n')
                f.write(output)
        self._created_files = True
    
    def show(self, ):
        
        if not self._created_files:
            self.create_files()
                
        number_squares = len(self.square_dimensions)
        
        fig, axes = plt.subplots(number_squares, sharex = False, sharey = False)
        
        several_axes = True if isinstance(axes, np.ndarray) else False
        
        for index,n,file_name in zip(range(number_squares), self.square_dimensions, self.file_names):
            
                output = check_output(["./../OCamL/DPLL", file_name]).decode("utf-8") 
                
                if output[:4] == 'true':
                    
                    ax = axes if not several_axes else axes[index]
                    
                    # valuation = output[7:-2].split(' || ')[:-1]
                    valuation = output[5:].split()
                    valuation = [(((int(l)-1)//(n**2))%n, ((int(l)-1)//n)%n, (int(l)-1)%n) for l in valuation]
                    
                    # color_list = plt.cm.Set3(np.linspace(0, 1, n))
                    # grid = np.zeros((n,n),dtype='f,f,f,f')
                    # grid.fill((1.,1.,1.,1.))
                    
                    grid = np.zeros((n,n))
                    
                    for (k,i,j) in valuation:
                        grid[i,j] = k+1
                        ax.text(j,i,str(k+1),ha='center',va='center')
                                            
                    ax.imshow(grid, interpolation ='none', aspect = 'auto', cmap='Set3')
        
        plt.show()

L = LatinSquare(5, 4)
L.show()