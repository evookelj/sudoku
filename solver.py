from random import randint
import sys
import time

class Board:

	def __init__(self):
		self.board = [[range(1,10) for i in range(9)] for i in range(9)]

	def square(self,r,c):
		return [self.board[row][col] for row in range(r,r+3) for col in range(c,c+3)]

	def row(self, r):
		return self.board[r]

	def col(self, c):
		return [row[c] for row in self.board]

	def load_givens(self, given_board):
		for r in range(9):
			for c in range(9):
				if given_board[r][c] > 0:
					self.board[r][c] = given_board[r][c]

	def check_squares(self):
		for r in range(0,9,3):
			for c in range(0,9,3):
				new_group = self.check_group(self.square(r,c))
				for row in range(r,r+3):
					for col in range(c,c+3):
						self.board[row][col] = new_group[3*(row-r)+(col-c)]

	def check_rows(self):
		for r in range(9):
			new_group = self.check_group(self.row(r))
			for c in range(9):
				self.board[r][c] = new_group[c]

	def check_cols(self):
		for c in range(9):
			new_group = self.check_group(self.col(c))
			for r in range(9):
				self.board[r][c] = new_group[r]

	def check_group(self,group):
		new_group = []
		taken = [group[j] for j in range(len(group)) if isinstance(group[j], int)]
		for i in range(len(group)):
			if not isinstance(group[i],list):
				valid_set = group[i]
			else:
				valid_set = [num for num in group[i] if num not in taken]
				if len(valid_set)==1:
					valid_set = valid_set[0]
					taken.append(valid_set)
			new_group.append(valid_set)
		return new_group

	def is_finished(self):
		num_finished = len([self.board[r][c] for r in range(9) for c in range(9) if not isinstance(self.board[r][c],list)])
		return num_finished==81

	def solve_slow(self):
		start = time.time()
		while not b.is_finished():
			b.check_squares()
			b.check_cols()
			b.check_rows()
		end = time.time()
		print "elapsed %f"%(end-start)

	def solve_fast(self):
		start = time.time()
		num_finished = 0
		for r in range(9):
			for c in range(9):
				vals = self.board[r][c]
				if not isinstance(vals,list):
					continue
					num_finished += 1
				for pos in vals:
					if pos in self.row(r) or pos in self.col(c) or pos in self.square((r%3)*3, (c&3)*3):
						self.board[r][c] = vals.remove(pos)
				if not isinstance(self.board[r][c],list):
					num_finished += 1
		end = time.time()
		print "elapsed %f"%(end-start)

if __name__ == "__main__":
	b = Board()
	b.load_givens([
		[-1,-1,-1,2,9,-1,-1,-1,-1],
		[5,-1,-1,-1,3,8,-1,4,1],
		[7,3,-1,-1,4,1,-1,2,1],
		[8,-1,5,1,6,2,3,-1,-1],
		[-1,9,1,-1,8,-1,-1,-1,6],
		[4,-1,-1,-1,7,-1,1,8,2],
		[6,4,-1,-1,-1,7,5,-1,-1],
		[-1,-1,7,9,5,-1,-1,6,-1],
		[9,-1,-1,3,2,-1,-1,-1,-1]
		])
	b.solve_slow()
b.solve_fast()