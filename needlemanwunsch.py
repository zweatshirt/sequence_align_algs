# Author: Zachery Linscott
# Sequence alignment
# Pipes indicate matches, dashes indicate misses/gaps

# The alignment problem takes a 2 dimension solution

# Given two sequences:
x = 'TGATGAT'
y = 'TGTTGCT'
# start by comparing x[0] and y[0]
# then compare the subsequences x[0..1] and y[0..1] and so on


# Needleman-Wunsch Alignment Scoring Matrix

#  T G A T G A T C G A T G C
# T
# G
# A
# T
# G
# T
# A
# G
# C
# T
# A 
# G 
# C

def pprint(mat):
    print('\n'.join(['\t'.join([str(col) for col in row]) for row in mat]))


# could be faster
def init_penalty_mat(x, y, gap_penalty=-1):
    mat = [[0] * (len(y) + 1) for i in range(len(x) + 1)]

    penalty = gap_penalty
    for i in range(1, len(mat)):
        mat[i][0] = mat[0][i] = penalty
        penalty += gap_penalty
    return mat


def add_penalty(mat, x, y):
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            prev_ij = mat[i - 1][j - 1]
            prev_row = mat[i - 1][j]
            prev_col = mat[i][j - 1]

            if x[i - 1] == y[j - 1]:
                mat[i][j] += prev_ij + 1
            else:
                if prev_row > prev_col and prev_row > prev_ij:
                    mat[i][j] += prev_row -1
                elif prev_col > prev_row and prev_col > prev_ij:
                    mat[i][j] += prev_col -1
                elif prev_ij > prev_row and prev_ij > prev_col:
                    mat[i][j] += prev_ij -1
    return mat


mat = init_penalty_mat(x, y, -5)
mat = add_penalty(mat, x, y)
pprint(mat)