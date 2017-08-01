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
		taken = set([j for j in group if isinstance(j, int)])
		for i in range(len(group)):
			if not isinstance(group[i],list):
				valid_set = group[i]
			else:
				valid_set = set([num for num in group[i] if num not in taken])
				if len(valid_set)==1:
					valid_set = valid_set[0]
					taken.add(valid_set)
			new_group.append(valid_set)
			if len(taken)==len(group):
				new_group += group[i+1:]
				return new_group

		return new_group

	def is_finished(self):
		num_finished = len([self.board[r][c] for r in range(9) for c in range(9) if not isinstance(self.board[r][c],list)])
		return num_finished==81

	def solve(self):
		start = time.time()
		while not self.is_finished():
			if time.time()-start>1:
				print "solve_a failed"
				return 1
			self.check_squares()
			self.check_cols()
			self.check_rows()
		end = time.time()
		print "elapsed a %f"%(end-start)
		return 0

def solve(puzzle):
	b = Board()
	b.load_givens(puzzle)
	b.solve()

if __name__ == "__main__":
	print "FLASH"
	puzzle = [
		[-1,-1,-1,2,9,-1,-1,-1,-1],
		[5,-1,-1,-1,3,8,-1,4,1],
		[7,3,-1,-1,4,1,-1,2,1],
		[8,-1,5,1,6,2,3,-1,-1],
		[-1,9,1,-1,8,-1,-1,-1,6],
		[4,-1,-1,-1,7,-1,1,8,2],
		[6,4,-1,-1,-1,7,5,-1,-1],
		[-1,-1,7,9,5,-1,-1,6,-1],
		[9,-1,-1,3,2,-1,-1,-1,-1]
		]

	solve(puzzle)

	print "EASY"
	puzzle = [
		[0,0,8,7,3,1,0,0,0],
		[0,0,7,5,4,9,0,2,3],
		[9,0,0,6,2,8,1,0,0],
		[4,7,3,2,0,0,0,0,8],
		[8,1,6,0,5,0,0,0,2],
		[5,0,0,0,0,0,0,0,6],
		[0,5,4,1,6,0,0,0,9],
		[0,0,1,0,0,0,0,0,4],
		[3,0,2,9,7,0,0,0,0]
	]
	solve(puzzle)

	print "MEDIUM"
	puzzle = [
		[0,8,1,3,0,0,0,6,2],
		[4,0,0,0,0,0,0,3,0],
		[2,0,5,1,0,0,0,0,9],
		[5,0,3,0,1,0,0,7,0],
		[0,6,0,4,3,0,0,9,8],
		[0,0,0,0,9,0,0,0,0],
		[7,0,0,8,2,0,4,1,0],
		[0,0,2,0,7,0,0,0,0],
		[0,0,0,6,0,0,5,0,0]
	]
	solve(puzzle)

	print "HARD"
	puzzle = [
		[0,0,9,0,3,0,0,4,6],
		[0,5,3,0,0,0,9,0,0],
		[6,0,0,9,7,2,1,0,0],
		[0,0,0,0,0,4,0,0,0],
		[9,7,5,0,8,0,0,6,0],
		[0,0,8,0,5,0,0,0,1],
		[5,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,1,5,0,0],
		[0,0,0,0,9,8,0,7,0]
	]
	solve(puzzle)

	print "EXPERT"
	puzzle = [
		[0,0,9,0,2,0,6,0,0],
		[0,0,0,4,0,0,0,5,0],
		[5,4,0,0,0,1,0,0,0],
		[0,5,0,9,4,3,2,0,6],
		[9,0,2,0,0,0,0,0,0],
		[0,0,6,0,0,0,0,0,0],
		[0,0,0,5,0,2,0,0,0],
		[8,0,0,3,0,0,1,0,0],
		[1,2,0,0,0,0,0,4,0]
	]
	solve(puzzle)

	print "HARDEST"
	puzzle = [
		[8,0,0,0,0,0,0,0,0],
		[0,0,3,6,0,0,0,0,0],
		[0,7,0,0,9,0,2,0,0],
		[0,5,0,0,0,7,0,0,0],
		[0,0,0,0,4,5,7,0,0],
		[0,0,0,1,0,0,0,3,0],
		[0,0,1,0,0,0,0,6,8],
		[0,0,8,5,0,0,0,1,0],
		[0,9,0,0,0,0,4,0,0]
	]
	solve(puzzle)

