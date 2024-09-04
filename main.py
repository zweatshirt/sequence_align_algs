import sys
import csv
# Author: Zachery Linscott
# 9/2/2024
# Global, local, and semiglobal sequence alignment project.
# The alignment problem takes a 2 dimension solution


def pprint(mat):
    print('\n\n'.join(['\t'.join([str(col) for col in row[1:]]) for row in mat[1:]]))
    print('\n')


# initializes the penalty matrix.
# parameters:
# x is the first string for the comparison.
# y is the second string for the comparison.
# gap penalty can be chosen, or defaults to -1.
# align type can be chosen but defaults to global.
def init_penalty_mat(x, y, gap_penalty=-1, align_type='global'):
    mat = [[0] * (len(y) + 1) for i in range(len(x) + 1)]

    if align_type == 'local' or align_type =='semiglobal':
        return mat
    
    if align_type == 'global':
        penalty = gap_penalty
        for i in range(1, len(mat)):
            mat[i][0] = penalty
            penalty += gap_penalty
        penalty = gap_penalty
        for i in range(1, len(mat[0])):
            mat[0][i] = penalty
            penalty += gap_penalty
    
    return mat

# initializes sub matrix given the string of chars and their sub values
def init_sub_mat(x, sub_from_file):
    # x will be line 1 [Characters]
    # sub_from_file will be everything from line 2 [Sub values]

    # initialize matrix of 0s
    mat = [[0] * (len(x) + 1) for i in range(len(x) + 1)]

    # populate matrix's 0th row and column with the chars
    for i in range(1, len(mat)):
        mat[i][0] = mat[0][i] = x[i - 1]
    
    # will need to be modified
    # starts on second line of file

    # populate the matrix with its sub values 
    for i in range(len(sub_from_file)):
        for j in range(len(sub_from_file)):
            mat[i + 1][j + 1] = sub_from_file[i][j]
    return mat


def align_with_sub(mat, x, y, sub_mat, penalty=-1, align_type='global'):
    # grab characters of the sub matrix for accessing later
    sub_mat_chars = [char for char in sub_mat[0]]

    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):

            # grab prior vals to determine optimum for i,j
            prev_ij = mat[i - 1][j - 1] # diagonal
            prev_row = mat[i - 1][j] # vertical
            prev_col = mat[i][j - 1] # horizontal

            row_char = x[i - 1] # what char from x are we looking at
            col_char = y[j - 1] # what char from y are we looking at

            # find x and y chars in sub matrix to compute their match/sub value
            sub_mat_row_loc = sub_mat_chars.index(row_char)
            sub_mat_col_loc = sub_mat_chars.index(col_char)
            sub_mat_score = sub_mat[sub_mat_row_loc][sub_mat_col_loc]
            dir = '' # initalize string for direction of optimal choice

            # the matrix is initialized with 0s but later populated with lists
            # to store both the value and opt choice dir string
            #  due to this, both cases have to be managed
            if isinstance(prev_ij, int):
                diag_sub = prev_ij + sub_mat_score # [i-1,i-j] val + sub matrix val
            else: diag_sub = prev_ij[0] + sub_mat_score
            if isinstance(prev_row, int):            
                vertical_move =  prev_row + penalty # [i - 1, j] val + penalty val
            else: vertical_move = prev_row[0] + penalty
            if isinstance(prev_col, int):
                horiz_move = prev_col + penalty # [i, j - 1] val + penalty val
            else: horiz_move = prev_col[0] + penalty

            # Note to self: refactor if statements here
            # the algorithm is the same for global and semiglobal here
            if align_type == 'global' or align_type == 'semiglobal':
                optimal = max(diag_sub, vertical_move, horiz_move)
                if optimal == diag_sub: dir += 'd'
                if optimal == vertical_move: dir += 'v'
                if optimal == horiz_move: dir += 'h'
                mat[i][j] = [optimal, dir]
            
            # optimum val for local can't be negative
            if align_type == 'local':
                optimal = max(diag_sub, vertical_move, horiz_move, 0)
                if optimal == diag_sub: dir += 'd'
                if optimal == vertical_move: dir += 'v'
                if optimal == horiz_move: dir += 'h'
                if optimal == 0: dir += ' '
                mat[i][j] = [optimal, dir]
    return mat

def find_optimal_alignment(mat, traceback_loc, align_type='global'):
    pass

# returns start location for semiglobal matrix backtracing
def semi_traceback_start(mat):

    # initialize optimum value and optimum val idx to 0
    end_col_opt = 0
    end_row_opt = 0
    end_row_opt_idx = 0
    end_col_opt_idx = 0

    # grab last row and column from mat
    last_col = [row[-1] for row in mat[1:]]
    last_row = mat[-1][1:]

    # find optimum value in last column
    for idx, i in enumerate(last_col): 
        if i[0] > end_col_opt:
            end_col_opt = i[0]
            end_col_opt_idx = idx

    # fin optimum value in last row
    for idx, j in enumerate(last_row):
        if j[0] > end_row_opt:
            end_row_opt = j[0]
            end_row_opt_idx = idx

    # just a print statement because I was curious.
    # True in the case of mat[n][m] being the opt, or if they happen to match
    if end_col_opt == end_row_opt:
        print("Max val of last row is the same as the max val of the last col: {}".format(end_col_opt))

    # get max of max of last row and max of last column
    max_of_row_col = max(end_col_opt, end_row_opt)

    # if the max is from the last column return the relative i,jth idx
    if max_of_row_col == last_col[end_col_opt_idx][0]:
        print("Last col has opt at i: {} j: {}".format(end_col_opt_idx, len(mat[0])))
        return [end_col_opt_idx, len(mat[0])] # i, j pair
    
    # if the max is from the last row return the relative i,jth idx
    if max_of_row_col == last_row[end_row_opt_idx][0]:
        print("Last row has opt at i: {} j: {}".format(len(mat) -1, end_row_opt_idx))
        return [len(mat) - 1, end_row_opt_idx] # i, j pair
    



def main():
    # align_types = ["global", "local", "semiglobal", "affine"]
    # seq1 = []
    # seq2 = []
    # sub_mat = []

    # # input1, input2 = sys.argv[1], sys.argv[2]
    # seq_file1 = input("Enter the full path of the first sequence file: ")
    # seq_file2 = input("Enter the full path of the second sequence file: ")
    # sub_mat_f = input("Enter the full path of the sub matrix file: ")
    # align_type = input(
    #     "Enter the alignment type ({}, {}, {}, or {}): "
    #     .format(align_types[0], align_types[1], align_types[2], align_types[3])
    # )
    # gap_penalty = input("Enter the gap penalty: ")

    # with open(seq_file1, 'r', encoding='utf-8') as f1:
    #     seq1 = f1.readlines()[1]

    # with open(seq_file2, 'r', encoding='utf-8') as f2:
    #     seq2 = f2.readlines()[1]

    # with open(sub_mat_f, 'r', encoding='utf-8') as sub_mat_f:
    #     read = csv.reader(sub_mat_f)
    #     [sub_mat.append(row) for row in read]
    #     sub_mat.pop(0) #discard first row

    # print(seq1, seq2, sub_mat)
    # # Output alignment of the two sequences, the OPT matrix, the optimal alignment score


    HW1_str_1 = 'TGATGA' # vertical
    HW_lst_1 = [c for c in HW1_str_1]
    HW1_str_2 = 'TTACTGC' # horizontal
    HW_lst_2 = [c for c in HW1_str_2]
    print(HW_lst_2)

    
    sub_mat = [[4, -2, 1, -2], [-2, 4, -2, 1], [1, -2, 4, -2], [-2, 1, -2, 4]]
    sub_mat = init_sub_mat('ACGT', sub_mat)

    mat = init_penalty_mat(HW1_str_2, HW1_str_1, gap_penalty=-5, align_type='semiglobal')
    mat = align_with_sub(mat, HW1_str_2, HW1_str_1, sub_mat, penalty=-5, align_type='semiglobal')
    pprint(mat)
    print(semi_traceback_start(mat))
  

if __name__ == "__main__":
    main()