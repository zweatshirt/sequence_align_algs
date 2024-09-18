from constants import G, SG, L

# Author: Zachery Linscott

# fills in the penalty matrix
# optimum values depend on whether the alignment type is:
# global, local, semiglobal
# parameters:
# mat - an n x m 0 filled penalty matrix that has been initialized by init_penalty_mat()
# x - string 1 to compare
# y - string 2 to compare
# sub_mat - an n x m matrix initialized by init_sub_mat()
# penalty - penalty score
# align_type - which alignment algorithm: global, local, semiglobal 
def align_with_sub(mat, x, y, sub_mat, penalty=-1, align_type=G):
    # grab characters of the sub matrix for accessing later
    sub_mat_chars = sub_mat.pop(0)

    for i in range(len(sub_mat)):
        for j in range(i):
            sub_mat[i][j] = int(sub_mat[i][j])

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
            sub_mat_score = int(sub_mat[sub_mat_row_loc][sub_mat_col_loc])
            dir = '' # initalize string for direction of optimal choice

            # the matrix is initialized with 0s but later populated with lists
            # to store both opt value and opt direction string.
            # due to this, both cases have to be managed.
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
            if align_type == G or align_type == SG:
                optimal = max(diag_sub, vertical_move, horiz_move)
                if optimal == diag_sub: dir += 'd'
                if optimal == vertical_move: dir += 'v'
                if optimal == horiz_move: dir += 'h'
                mat[i][j] = [optimal, dir]
            
            # optimum val for local can't be negative
            if align_type == L:
                optimal = max(diag_sub, vertical_move, horiz_move, 0)
                if optimal == diag_sub: dir += 'd'
                if optimal == vertical_move: dir += 'v'
                if optimal == horiz_move: dir += 'h'
                if optimal == 0: dir += ' '
                mat[i][j] = [optimal, dir]
    return mat


# recursive traceback algorithm that handles the 3 primary cases:
# global, semigloba, local.
# parameters:
# mat: whichever penatly matrix we are looking to do traceback for
# i and j: the location of the element that we are at looking.
# first_col and first_row: used in the case of semiglobal alignment
#     if the element is in the first row or column we return for semiglobal
# x and y: the base strings that we are looking to align
# x_aligned and y_aligned: lists of the new optimally aligned strings
#    x_aligned and y_aligned are reversed, so they need to be reversed upon final return
# align_type: the align_type that we want to perform traceback for
# iter: what iteration in the recursion the func is at
def opt_align(mat, i=None, j=None, first_col=None, first_row=None, x='', y='', x_aligned=[], y_aligned=[], align_type=G, iter=0):
    
    # add sum of opt alignment score

    if iter == 0:
        if align_type == G: # global starting loc case
            i = len(x)
            j = len(y)
        if align_type == SG: # semiglobal starting loc case
            i, j = semi_traceback_start(mat) 
        if align_type == L: # local starting loc case
            i, j = local_traceback_start(mat)

        # this is simply due to the way I handle the matrix
        # with global/semiglobal compared to local...
        if align_type == G or align_type == SG: 
            mat=[row[1:] for row in mat[1:]]

        # grab the first row and col in semiglobal case
        if align_type == SG:
            first_row = mat[0]
            first_col = [row[0] for row in mat]


    if i == 0 and j == 0: # base case, particularly common for global
        return [''.join(reversed(x_aligned)), ''.join(reversed(y_aligned))]
    
    if i == 0 and j > 0: # in first row 
        x_aligned.append('_')
        y_aligned.append(y[j - 1])
        return opt_align(mat, i, j - 1, first_col, first_row, x, y, x_aligned, y_aligned, align_type, iter + 1)

    if j == 0 and i > 0: # in first column
        x_aligned.append(x[i - 1])
        y_aligned.append('_')
        return opt_align(mat, i - 1, j, first_col, first_row, x, y, x_aligned, y_aligned, align_type, iter + 1)
    
    elem = mat[i - 1][j - 1]

    # local alignment base case
    if isinstance(elem, list): local_elem = elem[0]
    else: local_elem = elem
    if align_type == L and local_elem == 0:
        x_aligned.append(x[i - 1])
        y_aligned.append(y[j - 1])
        return [''.join(reversed(x_aligned)), ''.join(reversed(y_aligned))]
    
    # semiglobal base case
    if align_type == SG and (elem in first_row or elem in first_col):
        x_aligned.append(x[i - 1])
        y_aligned.append(y[j - 1])
        return [''.join(reversed(x_aligned)), ''.join(reversed(y_aligned))]

    # if the move is diagonal
    if i > 0 and j > 0 and 'd' in elem[1]:
        x_aligned.append(x[i - 1])
        y_aligned.append(y[j - 1])
        return opt_align(mat, i - 1, j - 1, first_col, first_row, x, y, x_aligned, y_aligned, align_type, iter + 1)
    
    # if the move is horizontal
    if i > 0 and 'h' in elem[1]:
        x_aligned.append('_')
        y_aligned.append(y[j - 1])
        return opt_align(mat, i, j - 1, first_col, first_row, x, y, x_aligned, y_aligned, align_type, iter + 1)
    
    # if the move is vertical
    if j > 0 and 'v' in elem[1]:
        x_aligned.append(x[i - 1])
        y_aligned.append('_')
        return opt_align(mat, i - 1, j, first_col, first_row, x, y, x_aligned, y_aligned, align_type, iter + 1)


# this function check for the highest value in the entire matrix
# and returns it as the starting loc for local traceback
# parameter:
# mat - m x n penalty matrix that has been populated with values
def local_traceback_start(mat):
    max_elem = 0
    max_ij = None
    for i in range(len(mat)):
        for j in range(i):
            if isinstance(mat[i][j], list):
                elem = mat[i][j][0]
            else: elem = mat[i][j]

            if elem > max_elem:
                max_elem = elem
                max_ij = (i, j)
    return max_ij


# returns start location for semiglobal matrix backtracing
# by checking the last row and last column of the 
# populated penalty matrix
# parameter:
# mat - specifically an m x n penalty matrix that is semiglobal and already filled.
def semi_traceback_start(mat):

    # initialize optimum val and optimum val idx to 0
    end_col_opt, end_row_opt, end_col_opt_idx, end_col_opt_idx = 0, 0, 0, 0

    # grab last row and column from mat
    last_col = [row[-1] for row in mat[1:]]
    last_row = mat[-1][1:]

    # find optimum value in last column
    for idx, i in enumerate(last_col): 
        if i[0] > end_col_opt:
            end_col_opt = i[0]
            end_col_opt_idx = idx

    # find optimum value in last row
    for idx, j in enumerate(last_row):
        if j[0] > end_row_opt:
            end_row_opt = j[0]
            end_row_opt_idx = idx

    # just a print statement because I was curious.
    # True in the case of mat[n][m] being the opt, or if they happen to match
    # if end_col_opt == end_row_opt:
    #     print("Max val of last row is the same as the max val of the last col: {}".format(end_col_opt))

    # get max of max of last row and max of last column
    max_of_row_col = max(end_col_opt, end_row_opt)

    # if the max is from the last column return the relative i,jth idx
    if max_of_row_col == last_col[end_col_opt_idx][0]:
        # return [end_col_opt_idx, len(mat[0]) - 1] # i, j pair
        return [len(mat) - 1, end_col_opt_idx]
    
    # if the max is from the last row return the relative i,jth idx
    if max_of_row_col == last_row[end_row_opt_idx][0]:
        # return (len(mat) - 1, end_row_opt_idx) # i, j pair
        return [end_row_opt_idx, len(mat[0]) - 1]