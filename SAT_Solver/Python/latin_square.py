from subprocess import check_output
from matplotlib import pyplot as plt
import numpy as np


class LatinSquare():
    
    _created_files = False
    
    def __init__(self, *args, prefix = 'latin_square', identifiers =[]):
        assert args
        self.file_names = []
        self.outputs = []
        self.square_dimensions = args
        
        for index, n in enumerate(args):
            if identifiers:
                file_name = prefix + '_' + str(n) + '_' + identifiers[index] + '.txt'
            else:
                file_name = prefix + '_' + str(n) + '.txt'
                
            self.file_names.append(file_name)
            output_str = ''
            
            
            # (k,i,j) is true iff the variable k is in position (i,j)
            # (k,i,j) corresponds to the literal number k*(n**2) + i*n + j + 1
            n_squared = n**2
            
            for k in range(n):
                for i in range(n):
                    not_two_in_one_row = ''
                    for j in range(n):
                        output_str += str(k*n_squared + i*n + j + 1) + ' '
                        for j2 in range(j):
                            not_two_in_one_row += '-' + str(k*n_squared+i*n+j2+1) + ' -' + str(k*n_squared+i*n+j+1) + ' 0\n'
                    output_str += '0\n'
                    output_str += not_two_in_one_row
                    
            for k in range(n):
                for j in range(n):
                    not_two_in_one_col = ''
                    for i in range(n):
                        output_str += str(k*n_squared+i*n+j+1) + ' '
                        for i2 in range(i):
                            not_two_in_one_col += '-' + str(k*n_squared+i2*n+j+1) + ' -' + str(k*n_squared+i*n+j+1) + ' 0\n'
                    output_str += '0\n'
                    output_str += not_two_in_one_col
    
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        output_str += str(k*n_squared+i*n+j+1) + ' '
                    output_str += '0\n'
                    
            self.outputs.append(output_str)
            
    def __iter__(self):
        for output in self.outputs:
            yield output
            
        
    def create_files(self):
        for n, file_name, output in zip(self.square_dimensions, self.file_names, self.outputs):
            with open(file_name, 'w') as f:
                f.write('c '+ file_name + ' : Latin Square CNF file python generated.\n')
                f.write(output)
        self._created_files = True
    
    def show(self, subgrids_size = 0):
        
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
                    
                    if subgrids_size:
                        ax.xaxis.set_ticks([-0.5+i*subgrids_size for i in range(n)])
                        ax.yaxis.set_ticks([-0.5+i*subgrids_size for i in range(n)])
                        ax.grid(True)
                        
                    ax.imshow(grid, interpolation ='none', aspect = 'auto', cmap='Set3')
        
        plt.show()
        
