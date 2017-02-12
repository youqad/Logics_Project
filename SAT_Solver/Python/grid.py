from subprocess import check_output
from matplotlib import pyplot as plt
import numpy as np
from random import sample


class Grid():
    _created_files = False

    _color_maps = frozenset(
        ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap',
         'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r',
         'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r',
         'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'Pu' 'Rd_r', 'Purples',
         'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYl' 'Bu_r', 'RdYlGn',
         'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r',
         'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r',
         'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr',
         'bwr_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copp' 'er', 'copper_r', 'cubehelix', 'cubehelix_r',
         'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gi' 'st_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r',
         'gist_ncar', 'gist_ncar_r', 'gist_rainb' 'ow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg',
         'gist_yarg_r', 'gnuplot', 'g' 'nuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv',
         'hsv_r', 'inferno', 'i' 'nferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r',
         'ocean', 'oce' 'an_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r',
         'seismi' 'c', 'seismic_r', 'spectral', 'spectral_r', 'spring', 'spring_r', 'summer', 'summer_r', 'terrain',
         'terrain_r', 'viridis', 'viridis_r', 'winter', 'winter_r'])

    def __init__(self, *args, prefix= 'game', identifiers=[],  original_grids = [], examples_folder='../Examples/', color_map=''):
        assert args
        self.color_map = color_map
        self.examples_folder = examples_folder
        self.file_names = []
        self.outputs = []
        self.square_dimensions = args
        self.prefix = prefix
        self.original_grids = original_grids

        for index,n,grid in zip(range(len(args)), args, original_grids):
            file_name = self.prefix + '_' + str(n).replace('(', '').replace(')', '').replace(', ', '_')
            if identifiers:
                file_name+= '_' + identifiers[index] + '.txt'
            else:
                file_name+= '.txt'

            self.file_names.append(file_name)

            output_str = self.generate_file(n, original_grid = grid)

            self.outputs.append(output_str)

    def __iter__(self):
        for output in self.outputs:
            yield output

    def create_files(self):
        for n, file_name, output in zip(self.square_dimensions, self.file_names, self.outputs):
            with open(self.examples_folder + file_name, 'w') as f:
                f.write('c ' + file_name + ' : ' + ' '.join(self.prefix.split('_')).capitalize() + ' CNF file python generated.\n')
                f.write(output)
        self._created_files = True

    def show(self):

        if not self._created_files:
            self.create_files()

        number_squares = len(self.square_dimensions)

        fig, axes = plt.subplots(number_squares, sharex=False, sharey=False)

        several_axes = True if isinstance(axes, np.ndarray) else False

        for index, n, file_name in zip(range(number_squares), self.square_dimensions, self.file_names):

            output = check_output(["./../OCamL/DPLL", self.examples_folder + file_name]).decode("utf-8")

            if output[:4] == 'true':

                ax = axes if not several_axes else axes[index]

                if self.color_map:
                    current_color_map = self.color_map
                else:
                    current_color_map = sample(self._color_maps, 1)[0]

                valuation = output[5:].split()
                valuation = [self.decode_literals(n, l) for l in valuation if self.decode_literals(n, l) is not None]

                grid = self.generate_grid(n, valuation, ax, original_grid = None if not self.original_grids else self.original_grids[index])

                ax.imshow(grid, interpolation='nearest', aspect='auto', cmap=current_color_map)
        plt.show()

    def generate_grid(self, dimensions, valuation, ax, original_grid = None):
        raise NotImplementedError

    def generate_file(self, dimensions, original_grid=None, verbose=False):
        raise NotImplementedError

    @staticmethod
    def decode_literals(dimensions, l):
        raise NotImplementedError

