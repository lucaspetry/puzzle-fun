from . import SudokuPuzzle


class NaiveSudokuSolver(object):

	def __init__(self):
		pass


	def solve(self, puzzle):
		assert isinstance(puzzle, SudokuPuzzle), "Invalid puzzle!"
		max_iter = puzzle.num_blank()
		num_iter = 0
		filled = 0

		while num_iter < max_iter:
			prev_filled = filled
			for i in range(0, puzzle.size()):
				for j in range(0, puzzle.size()):
					if not puzzle.is_filled(i, j):
						p = puzzle.get_possible(i, j)
						if len(p) == 1:
							puzzle.fill(i, j, p[0])
							filled += 1
			num_iter += 1

			if puzzle.is_complete():
				break

			if prev_filled == filled:
				break
		print("Num blank: ", max_iter)
		print("Num iter:  ", num_iter)
		print("Num filled:", filled)
		if filled < max_iter:
			print("Could not complete the puzzle!")
