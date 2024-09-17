from constants import G, SG, L

# Author: Zachery Linscott

# initializes the penalty matrix.
# parameters:
# x - the first string for the comparison.
# y - the second string for the comparison.
# gap_penalty - penalty val that can be chosen, or defaults to -1.
# align_type - which alignment algorithm: global, local, semiglobal.
def init_penalty_mat(x, y, gap_penalty=-1, align_type=G):
    mat = [[0] * (len(y) + 1) for i in range(len(x) + 1)]

    if align_type == L or align_type == SG:
        return mat
    
    if align_type == G:
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
# parameters:
# x - string of characters from file for sub matrix
# sub_from_file - substitution matrix from file (an n x m matrix)
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