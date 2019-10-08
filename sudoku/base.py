import numpy as np


class SudokuPuzzle(object):

	VALID_SIZES = [6, 9]

	def __init__(self, init_grid, subgrid_size):
		self._grid = np.array(init_grid)
		self._sub_size = subgrid_size
		self._fixed_mask = self._grid > 0
		self._max_val = len(init_grid)
		self._choices = np.r_[1:self._max_val + 1]

		assert self._grid.shape[0] in SudokuPuzzle.VALID_SIZES and \
			   self._grid.shape[1] in SudokuPuzzle.VALID_SIZES, \
			   "Invalid grid size!"
		assert self._max_val % self._sub_size == 0, "Invalid subgrid size!"

	def fill(self, i, j, val):
		assert val >= 0 and val <= self._max_val, "Invalid value!"
		assert not self._fixed_mask[i][j], "Cannot fill fixed value!"
		self._grid[i][j] = int(val)

	def is_filled(self, i, j):
		return self._grid[i][j] > 0

	def get_possible(self, i, j):
		assert self._grid[i][j] == 0, "Value already filled!"

		bl_i, bl_j = i // self._sub_size, j // self._sub_size
		bl_i, bl_j = bl_i * self._sub_size, bl_j * self._sub_size
		p = set(self._choices)
		p -= set(self._grid[i])
		p -= set(self._grid.transpose()[j])
		p -= set(self._grid[bl_i:bl_i+self._sub_size, bl_j:bl_j+self._sub_size].flatten())
		return list(p)

	def is_valid(self):
		def check_rows(grid):
			for row in range(0, self._max_val):
				counts = np.unique(grid[row], return_counts=True)
				counts = counts[1][1:] if counts[0][0] == 0 else counts[1]
				if not np.all(counts == 1):
					return False

		# Verify rows
		g = self._grid
		check_rows(g)

		# Verify cols
		g = g.transpose()
		check_rows(g)

		# Verify blocks
		g = np.array(np.split(self._grid, self._sub_size, axis=1))
		g = np.array(np.split(g, self._sub_size, axis=1)) \
		      .reshape(self._max_val, self._max_val)
		check_rows(g)

		return True

	def is_complete(self):
		target_sum = self._choices.sum()
		all_filled = np.all(self._grid > 0)
		col_sum = np.all(self._grid.sum(axis=0) == target_sum)
		row_sum = np.all(self._grid.sum(axis=1) == target_sum)

		p1 = np.array(np.split(self._grid, self._sub_size, axis=1))
		p2 = np.array(np.split(p1, self._sub_size, axis=1)) \
		       .reshape(self._max_val, self._max_val)
		block_sum = np.all(p2.sum(axis=1) == target_sum)

		return all_filled and col_sum and row_sum and block_sum

	def size(self):
		return self._max_val

	def num_filled(self):
		return np.sum(self._grid > 0)

	def num_blank(self):
		s = self._grid.shape
		return s[0] * s[1] - self.num_filled()

	def __str__(self):
		return np.array2string(self._grid, separator='  ')