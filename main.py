import sys
import csv
# Author: Zachery Linscott
# 9/2/2024
# Sequence alignment
# Pipes | indicate matches, underscore _ indicate misses/gaps

# The alignment problem takes a 2 dimension solution


def pprint(mat):
    print('\n\n'.join(['\t'.join([str(col) for col in row]) for row in mat]))
    print('\n')


# could be faster
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

# x here is the submatrix strings
def init_sub_mat(x, sub_from_file):
    # x will be line 1 [Characters]
    # sub_from_file will be everything from line 2 [Sub values]
    mat = [[0] * (len(x) + 1) for i in range(len(x) + 1)]

    for i in range(1, len(mat)):
        mat[i][0] = mat[0][i] = x[i - 1]
    
    # will need to be modified
    # starts on second line of file
    for i in range(len(sub_from_file)):
        for j in range(len(sub_from_file)):
            mat[i + 1][j + 1] = sub_from_file[i][j]
    return mat

# needs updating
def align(mat, x, y, penalty, match):
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            prev_ij = mat[i - 1][j - 1]
            prev_row = mat[i - 1][j]
            prev_col = mat[i][j - 1]

            if x[i - 1] == y[j - 1]:
                mat[i][j] += prev_ij + match
            else:
                if prev_row > prev_col and prev_row > prev_ij:
                    mat[i][j] += prev_row + penalty
                elif prev_col > prev_row and prev_col > prev_ij:
                    mat[i][j] += prev_col + penalty
                elif prev_ij > prev_row and prev_ij > prev_col:
                    mat[i][j] += prev_ij + penalty
    return mat


def align_with_sub(mat, x, y, sub_mat, penalty=-1, align_type='global'):
    # grab characters of the sub matrix for accessing later
    sub_mat_chars = [char for char in sub_mat[0]]

    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            prev_ij = mat[i - 1][j - 1] # diagonal
            prev_row = mat[i - 1][j] # vertical
            prev_col = mat[i][j - 1] # horizontal

            row_char = x[i - 1] # what char from x are we looking at
            col_char = y[j - 1] # what char from y are we looking at

            # find x and y chars in sub matrix to compute their match/sub value
            sub_mat_row_loc = sub_mat_chars.index(row_char)
            sub_mat_col_loc = sub_mat_chars.index(col_char)
            sub_mat_score = sub_mat[sub_mat_row_loc][sub_mat_col_loc]

            diag_sub = prev_ij + sub_mat_score            
            vertical_move =  prev_row + penalty
            horiz_move = prev_col + penalty
    
            if align_type == 'global' or align_type == 'semiglobal':
                optimal = max(diag_sub, vertical_move, horiz_move)
                mat[i][j] = optimal
            
            if align_type == 'local':
                optimal = max(diag_sub, vertical_move, horiz_move, 0)
                mat[i][j] = optimal

    if align_type == 'semiglobal':
        calc_max_end()

    return mat

# helper to alignment function in cases of semiglobal alignment
def calc_max_end(mat):
    end_col_sum = 0
    end_row_sum = 0
    for i in range(len(mat)):
        end_col_sum += mat[i][-1]
    for j in mat[-1]:
        end_row_sum += j
    print(max(end_col_sum, end_row_sum))


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
    # will be line 1 and other lines as list in the future for arguments

    mat = init_penalty_mat(HW1_str_2, HW1_str_1, gap_penalty=-5, align_type='semiglobal')
    pprint(sub_mat)
    mat_global = align_with_sub(mat, HW_lst_2, HW_lst_1, sub_mat, penalty=-5, align_type='semiglobal')
    pprint(mat_global)

    # mat = init_penalty_mat(HW1_str_2, HW1_str_1, align_type='local')    
    # mat_local = align_with_sub(mat, HW_lst_2, HW_lst_1, sub_mat, penalty=-5, align_type='local')
    # print("Local alignment:\n")
    # pprint(mat_local)

if __name__ == "__main__":
    main()