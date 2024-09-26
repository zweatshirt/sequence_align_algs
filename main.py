import csv
import os.path
from constants import G, SG, L, SEQ_DIR, SUBS_DIR
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

    # sequence files input
    seq_file1 = "{}/{}".format(
        SEQ_DIR, input("Enter the name of the first sequence file (e.g. sequenceA1.txt): ")
    )
    assert os.path.exists(seq_file1), f"{seq_file1} doesn't exist."
    seq_file2 = "{}/{}".format(
        SEQ_DIR, input("Enter the name of the second sequence file (e.g. sequenceA2.txt): ")
    )
    assert os.path.exists(seq_file2), f"{seq_file2} doesn't exist."

    # sub matrix file input
    sub_mat_f = "{}/{}".format(
        SUBS_DIR, input("Enter the name of the submatrix file (e.g. AAnucleoPP.txt): ")
    )
    assert os.path.exists(sub_mat_f), f"{sub_mat_f} doesn't exist."

    # alignment type
    at = input(
        "Enter the alignment type (e.g. {}, {}, or {}): "
        .format(G, L, SG)
    )
    assert at.casefold() in [G, L, SG], 'Mispelled the alignment type.'
    at = at.lower()

    # gap penalty
    gp = input("Enter the gap penalty: ")

    try:
        gp = float(gp)
    except:
        if gp[0] == '-' and gp[1:].isnumeric():
            gp = -float(gp[1:])
        assert gp.isnumeric(), 'The input must be a numerical value.'
    if gp > 0: gp = -gp 

    # read files
    with open(seq_file1, 'r', encoding='utf-8') as f1:
        seq1 = f1.readlines()[1]

    with open(seq_file2, 'r', encoding='utf-8') as f2:
        seq2 = f2.readlines()[1]

    with open(sub_mat_f, 'r', encoding='utf-8') as sub_mat_f:
        read = csv.reader(sub_mat_f)
        [sub_mat.append(row) for row in read]
        sub_mat.pop(0) #discard first row

    # weird edgecase for the B sequence files
    if '\n' in seq1: seq1 = seq1.replace('\n', '')
    if '\n' in seq2: seq2 = seq2.replace('\n', '')

    # initialize an empty penalty matrix given the gap penalty
    mat = init_penalty_mat(seq1, seq2, gap_penalty=gp, align_type=at)
    # populate matrix given the sub matrix read from the file
    mat = align_with_sub(mat, seq1, seq2, sub_mat=sub_mat, penalty=gp, align_type=at)

    opt_seq1, opt_seq2, score = opt_align(mat, x=seq1, y=seq2, align_type=at)

    print(f'Original sequences:\n\t{seq1}\n\t{seq2}')
    print('\n\nAlignment type: {}\nGap penalty: {}'.format(at.capitalize(), str(gp)))

    if (len(opt_seq1) == 0 and len(opt_seq2) == 0):
        print('\nNo optimal alignment for the sequences (all gaps)\nScore: {}\n'.format(score))
    else:
        print('\nOptimally aligned sequences:\n\t{}\n\t{}\n\tScore: {}\n'.format(opt_seq1, opt_seq2, score))
    print("Optimum alignment matrix:\n")
    pprint(mat)

if __name__ == "__main__":
    main()