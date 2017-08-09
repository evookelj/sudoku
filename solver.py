from random import randint
import sys
import time
from sudokuextract.extract import extract_sudoku, load_image, predictions_to_suduko_string

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

	def pop_from(self,r,c,val):
		vals = self.board[r][c]
		if isinstance(vals,list) and val in vals:
			self.board[r][c].remove(val)
			if len(self.board[r][c])==1:
				self.board[r][c] = self.board[r][c][0]
			return True
		return False

	def check_xwings(self):
		# only 2 candidates for a value, in each of 2 different units of the same kind,
		# and these candidates lie also on 2 other units of the same kind,
		# then all other candidates for that value can be eliminated from the latter two units.

		item_and_loc = {}
		for r in range(9):
			for c in range(9):
				if isinstance(self.board[r][c],int):
					continue
				key = str(self.board[r][c])
				if self.row(r).count(self.board[r][c])==2 and len(self.board[r][c])==2:
					if key not in item_and_loc:
						item_and_loc[key] = []
					item_and_loc[key].append([r,c])

		for c in range(9):
			for r in range(9):
				if isinstance(self.board[r][c],int):
					continue
				key = str(self.board[r][c])
				if self.col(c).count(self.board[r][c])==2 and len(self.board[r][c])==2:
					if key not in item_and_loc:
						item_and_loc[key] = []
					item_and_loc[key].append([r,c])

		pairs = []
		for key in item_and_loc:
			this_pair = {}
			rs = [item[0] for item in item_and_loc[key]]
			cs = [item[1] for item in item_and_loc[key]]
			if len(set(rs))==1:
				same_row = True
				same_col = False
			elif len(set(cs))==1:
				same_col = True
				same_row = False
			else:
				continue

			for second_key in item_and_loc:
				if second_key==key:
					continue
				second_rs = [item[0] for item in item_and_loc[second_key]]
				second_cs = [item[1] for item in item_and_loc[second_key]]
				if (same_col and rs==second_rs) or (same_row and cs==second_cs):
					key_arr = [int(item) for item in key.strip("[]").split(",")]
					second_key_arr = [int(item) for item in second_key.strip("[]").split(",")]
					try:
						val = [item for item in key_arr if item in second_key_arr][0]
					except:
						continue

					if same_row:
						rows = [item for item in range(9) if item not in rs+second_rs]
						cols = [ cs[0] ]
					if same_col:
						rows = [ rs[0] ]
						cols = [item for item in range(9) if item not in cs+second_cs]

					for row in rows:
						for col in cols:
							self.pop_from(row,col,val)

	def check_pointing_pairs(self):

		# BY SQUARE
		for r in range(0,9,3):
			for c in range(0,9,3):

				new_group = self.check_group(self.square(r,c))
				for row in range(r,r+3):
					for col in range(c,c+3):
						self.board[row][col] = new_group[3*(row-r)+(col-c)]
				sq = self.square(r,c)
				nums = [i for i in range(1,10) if i not in sq]
				if len(nums)<3:
					continue
				occurences = {str(num):[[],[]] for num in nums}
				for i in range(len(sq)):
					item_r = (i/3) + r
					item_c = (i%3) + c
					item = sq[i]
					if isinstance(item,list):
						for number in item:
							if number in nums:
								occurences[str(number)][0].append(item_r)
								occurences[str(number)][1].append(item_c)

				occurence_pairs = {str(num):[] for num in nums}
				for num in nums:
					if occurences[str(num)]==[[],[]]:
						# nums.remove(num)
						continue
					oc_rs = occurences[str(num)][0]
					oc_cs = occurences[str(num)][1]
					for i in range(len(oc_rs)):
						occurence_pairs[str(num)].append([oc_rs[i],oc_cs[i]])

				for num in nums:
					arr_num_occurence_rs = list(set(occurences[str(num)][0]))
					arr_num_occurence_cs = list(set(occurences[str(num)][1]))

					# pr = r==3 and c==6 and num==6

					# REMOVE POINTING PAIRS BY SQUARE
					safe_occurences = []
					for row in arr_num_occurence_rs:
						this_row = self.row(row)
						this_row_cols = [i for i in range(len(this_row)) if (isinstance(this_row[i],list) and num in this_row[i]) or (isinstance(this_row[i],int) and this_row[i]==num)]
						if all(c<=a_col<c+3 for a_col in this_row_cols): # all occurences of num in this square
							for this_sq_col in this_row_cols:
								safe_occurences.append([row, this_sq_col])
							break

					if len(safe_occurences)==0:
						for col in arr_num_occurence_cs:
							this_col = self.col(col)
							this_col_rows = [i for i in range(len(this_col)) if (isinstance(this_col[i],list) and num in this_col[i]) or (isinstance(this_col[i],int) and this_col[i]==num)]
							if all(r<=a_row<r+3 for a_row in this_col_rows): # all occurences of num in this square
								for this_sq_row in this_col_rows:
									safe_occurences.append([this_sq_row, col])
								break

					if len(safe_occurences)>0:
						for sq_row in range(r,r+3):
							for sq_col in range(c,c+3):
								if [sq_row,sq_col] not in safe_occurences:
									x = self.pop_from(sq_row,sq_col,num)
									# pass
						# continue

					# REMOVE POINTING PAIRS BY ROW/COL
					if len(arr_num_occurence_rs)==1:
						remove_r = arr_num_occurence_rs[0]
						for remove_c in range(0,c)+range(c+3,9):
							if not remove_c in arr_num_occurence_cs:
								self.pop_from(remove_r,remove_c,num)

					if len(arr_num_occurence_cs)==1:
						remove_c = arr_num_occurence_cs[0]
						for remove_r in range(0,r)+range(r+3,9):
							if not remove_r in arr_num_occurence_rs:
								self.pop_from(remove_r,remove_c,num)

	def check_nums(self):
		for num in range(1,10):
			occurence_rs = set()
			occurence_cs = set()
			for r in range(9):
				for c in range(9):
					if self.board[r][c]==num:
						occurence_rs.add(r)
						occurence_cs.add(c)

			# remove row/col possibilities
			for r in occurence_rs:
				for c in range(9):
					self.pop_from(r,c,num)

			for r in range(9):
				for c in occurence_cs:
					self.pop_from(r,c,num)

	def check_group(self,group,pr=False):
		new_group = []
		num_occurences = {str(num):[] for num in range(1,10)}
		taken_arrs = [i for i in group if isinstance(i,list) and group.count(i)==len(i)]
		taken_arr_vals = list(set([num for arr in taken_arrs for num in arr]))
		taken = [j for j in group if isinstance(j, int)]

		exists_only_with = {str(main_num):{str(num):True for num in range(1,10) if num!=main_num and num not in taken} for main_num in range(1,10) if main_num not in taken}

		for i in range(len(group)):
			if not isinstance(group[i],list):
				valid_set = group[i]
				num_occurences[str(valid_set)].append(i)
			else:
				valid_set = [num for num in group[i] if num not in taken]

				# new
				for this_number in sorted(valid_set):
					for key in exists_only_with[str(this_number)]:
						if this_number in valid_set and int(key) not in valid_set:
							exists_only_with[str(this_number)][key] = False
							exists_only_with[key][str(this_number)] = False
				# new

				for num in valid_set:
					num_occurences[str(num)].append(i)
				if group[i] not in taken_arrs:
					valid_set = [item for item in valid_set if item not in taken_arr_vals]
				else:
					valid_set = group[i]
				if len(valid_set)==1:
					valid_set = valid_set[0]
					taken.append(valid_set)
			new_group.append(valid_set)

		# new
		pre_new = new_group
		for main_num in exists_only_with:
			exc = [key for key in exists_only_with[main_num] if exists_only_with[main_num][key]]
			if len(exc)==1:
				ocs = len([i for i in new_group if isinstance(i,list) and (int(main_num) in i and int(exc[0]) in i)])
				other = [key for key in exists_only_with[exc[0]] if exists_only_with[exc[0]][key]]
				if len(other)==1 and ocs==2:
					for i in range(len(new_group)):
						if isinstance(new_group[i],list) and (int(main_num) in new_group[i] and int(exc[0]) in new_group[i]):
							new_group[i] = [int(main_num), int(exc[0])]
		# new
		
		for num in num_occurences:
			if len(num_occurences[num])==1:
				new_group[num_occurences[num][0]] = int(num)
		return new_group

	def is_finished(self):
		num_finished = len([self.board[r][c] for r in range(9) for c in range(9) if not isinstance(self.board[r][c],list)])
		return num_finished==81

	def solve_a(self):
		start = time.time()
		last_board = 0
		while not self.is_finished() and time.time()-start<2:
			# last_board = self.board[:]
			self.check_squares()
			self.check_cols()
			self.check_rows()
			self.check_pointing_pairs()
			self.check_nums()
			self.check_xwings()
		end = time.time()
		print "elapsed: %f"%(end-start)
		return 0

def solve(name,puzzle):
	print name.upper()
	b = Board()
	b.load_givens(puzzle)
	b.solve_a()
	print b.square(3,3)
	print ""
	# with open('%s.txt'%(name),'w') as t:
	# 	for row in puzzle:
	# 		for item in row:
	# 			if int(item)<1:
	# 				t.write(".")
	# 			else:
	# 				t.write(str(item))
	with open('%s_solved.txt'%(name),'w') as t:
		for row in b.board:
			for item in row:
				if isinstance(item,list):
					t.write(".")
				else:
					t.write(str(item))
	return b.board

def solve_image(file):
	img = load_image(file)
	predictions, sudoku_box_images, whole_sudoku_image = extract_sudoku(img)
	print predictions_to_suduko_string(predictions)
	x = solve('%s'%(file),predictions.tolist())
	print predictions_to_suduko_string(x)

if __name__ == "__main__":
	solve_image('puzzle5.png') 
	# b = Board()
	# b.check_group([6, [1, 3, 5, 8], [1, 3, 8], 9, [1, 2, 4, 5, 8], [1, 2, 4, 8], [5, 8], [1, 3, 5, 8], 7])


