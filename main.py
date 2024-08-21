import sys
import csv
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


# mat = init_penalty_mat(x, y, -5)
# mat = add_penalty(mat, x, y)
# pprint(mat)


def main():
    align_types = ["global", "local", "semiglobal", "affine"]
    seq1 = []
    seq2 = []
    sub_mat = []

    # input1, input2 = sys.argv[1], sys.argv[2]
    seq_file1 = input("Enter the full path of the first sequence file: ")
    seq_file2 = input("Enter the full path of the second sequence file: ")
    sub_mat_f = input("Enter the full path of the sub matrix file: ")
    align_type = input(
        "Enter the alignment type ({}, {}, {}, or {}): "
        .format(align_types[0], align_types[1], align_types[2], align_types[3])
    )
    gap_penalty = input("Enter the gap penalty: ")

    with open(seq_file1, 'r', encoding='utf-8') as f1:
        seq1 = f1.readlines()[1]

    with open(seq_file2, 'r', encoding='utf-8') as f2:
        seq2 = f2.readlines()[1]

    with open(sub_mat_f, 'r', encoding='utf-8') as sub_mat_f:
        read = csv.reader(sub_mat_f)
        [sub_mat.append(row) for row in read]
        sub_mat.pop(0) #discard first row

    print(seq1, seq2, sub_mat)
    # Output alignment of the two sequences, the OPT matrix, the optimal alignment score


if __name__ == "__main__":
    main()