import sys
import csv
import os.path
from constants import G, SG, L, A, SEQ_DIR, SUBS_DIR
from mat_init import init_penalty_mat, init_sub_mat
from align import align_with_sub, opt_align
from etc import pprint

# Author: Zachery Linscott
# 9/2/2024
# Global, local, and semiglobal sequence alignment project.


def main():
    seq1 = []
    seq2 = []
    sub_mat = []

    # input1, input2 = sys.argv[1], sys.argv[2]
    # sequence files input
    seq_file1 = "{}/{}".format(
        SEQ_DIR, input("Enter the name of the first sequence file (e.g. sequenceA1.txt): ")
    )
    assert(os.path.exists(seq_file1))
    seq_file2 = "{}/{}".format(
        SEQ_DIR, input("Enter the name of the second sequence file (e.g. sequenceA2.txt): ")
    )
    assert(os.path.exists(seq_file2))
    # sub matrix file input
    sub_mat_f = "{}/{}".format(
        SUBS_DIR, input("Enter the name of the submatrix file (e.g. AAnucleoPP.txt): ")
    )
    assert(os.path.exists(sub_mat_f))

    # alignment type
    at = input(
        "Enter the alignment type (e.g. {}, {}, {}, or {}): "
        .format(G, L, SG, A)
    )
    assert(at in [G, L, SG, A])

    # gap penalty
    gp = input("Enter the gap penalty as a positive integer (it will be converted to negative): ")
    assert(gp.isnumeric() and gp > 0)
    gp = -1 * int(gp) 


    # read files
    with open(seq_file1, 'r', encoding='utf-8') as f1:
        seq1 = f1.readlines()[1]

    with open(seq_file2, 'r', encoding='utf-8') as f2:
        seq2 = f2.readlines()[1]

    with open(sub_mat_f, 'r', encoding='utf-8') as sub_mat_f:
        read = csv.reader(sub_mat_f)
        [sub_mat.append(row) for row in read]
        sub_mat.pop(0) #discard first row

    # initialize an empty penalty matrix given the gap penalty
    mat = init_penalty_mat(seq1, seq2, gap_penalty=gp, align_type=at)
    # populate matrix given the sub matrix read from the file
    mat = align_with_sub(mat, seq1, seq2, sub_mat=sub_mat, penalty=gp, align_type=at)

    print('Optimally aligned sequences:\n' + '\n'.join(opt_align(mat, x=seq1, y=seq2, align_type=at)), end='\n\n')
    print("Optimum alignment matrix:\n")
    pprint(mat)
    # Output alignment of the two sequences, the OPT matrix, the optimal alignment score

    # HOMEWORK CASE
    # x = 'TTACTGC' # horizontal
    # y = 'TGATGA' # vertical
    
    # sub_mat = [[4, -2, 1, -2], [-2, 4, -2, 1], [1, -2, 4, -2], [-2, 1, -2, 4]]
    # sub_mat = init_sub_mat('ACGT', sub_mat)

    # mat = init_penalty_mat(x, y, gap_penalty=-5, align_type=L)
    # mat = align_with_sub(mat, x, y, sub_mat, penalty=-5, align_type=L)
    # pprint(mat)
    # print(opt_align(mat, x=x, y=y, align_type=L))

    # works for global but not semiglobal or local
    # print(opt_align(mat, x=x, y=y, align_type='semiglobal'))
    # sns.heatmap(mat)

if __name__ == "__main__":
    main()