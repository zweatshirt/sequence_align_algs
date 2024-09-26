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
            sub_mat[i][j] = float(sub_mat[i][j])

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
            sub_mat_score = float(sub_mat[sub_mat_row_loc][sub_mat_col_loc])
            dir = '' # initalize string for direction of optimal choice

            # the matrix is initialized with 0s but later populated with lists
            # to store both opt value and opt direction string.
            # due to this, both cases have to be managed.
            if isinstance(prev_ij, list):
                diag_sub = float(prev_ij[0]) + sub_mat_score # [i-1,i-j] val + sub matrix val
            else: diag_sub = float(prev_ij) + sub_mat_score
            if isinstance(prev_row, list):            
                vertical_move =  float(prev_row[0]) + penalty # [i - 1, j] val + penalty val
            else: vertical_move = float(prev_row) + penalty
            if isinstance(prev_col, list):
                horiz_move = float(prev_col[0]) + penalty # [i, j - 1] val + penalty val
            else: horiz_move = float(prev_col) + penalty

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


# Score is not correct
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
def opt_align(mat, i=0, j=0, first_col=None, first_row=None, x='', y='', x_aligned=[], y_aligned=[], align_type=G, iter=0, score=0):
    
    # add sum of opt alignment score
    if iter == 0:
        if align_type == G: # global starting loc case
            i = len(x)
            j = len(y)
            score = mat[len(mat) - 1][len(mat[0]) - 1]
            if isinstance(score, list): score = score[0]
        if align_type == SG: # semiglobal starting loc case
            # mat = [row[1:] for row in mat[1:]]
            i, j, score = semi_traceback_start(mat)
            print(i, j)

        if align_type == L: # local starting loc case
            i, j, score = local_traceback_start(mat)
        # this is simply due to the way I handle the matrix
        # with global/semiglobal compared to local...
        if align_type == G or align_type == SG: 
            mat = [row[1:] for row in mat[1:]]
          
        # grab the first row and col in semiglobal case
        if align_type == SG:
            first_row = mat[0]
            first_col = [row[0] for row in mat]

    if i == 0 and j == 0: # base case, particularly common for global
        return [''.join(reversed(x_aligned)), ''.join(reversed(y_aligned)), str(score)]
    
    print(i, j, iter)
    # semiglobal base case
    if (align_type == SG and i == 0) or (align_type == SG and j == 0):
        return [''.join(reversed(x_aligned)), ''.join(reversed(y_aligned)), str(score)]

    elem = mat[i - 1][j - 1]
  
    # local alignment base case
    if isinstance(elem, list): local_elem = elem[0]
    else: local_elem = elem
    if align_type == L and local_elem == 0:
        x_aligned.append(x[i - 1])
        y_aligned.append(y[j - 1])
        return [''.join(reversed(x_aligned)), ''.join(reversed(y_aligned)), str(score)]

    if i == 0 and j > 0: # in first row 
        x_aligned.append('_')
        y_aligned.append(y[j - 1])
        return opt_align(mat, i, j - 1, first_col, first_row, x, y, x_aligned, y_aligned, align_type, iter + 1, score)

    if j == 0 and i > 0: # in first column
        x_aligned.append(x[i - 1])
        y_aligned.append('_')
        return opt_align(mat, i - 1, j, first_col, first_row, x, y, x_aligned, y_aligned, align_type, iter + 1, score)
    

    # if the move is diagonal
    if i > 0 and j > 0 and 'd' in elem[1]:
        if align_type == SG and (i == 0 or j == 0):
            return [''.join(reversed(x_aligned)), ''.join(reversed(y_aligned)), str(score)]
        x_aligned.append(x[i - 1])
        y_aligned.append(y[j - 1])
        return opt_align(mat, i - 1, j - 1, first_col, first_row, x, y, x_aligned, y_aligned, align_type, iter + 1, score)
    
    # if the move is horizontal
    if i > 0 and 'h' in elem[1]:
        x_aligned.append('_')
        y_aligned.append(y[j - 1])
        return opt_align(mat, i, j - 1, first_col, first_row, x, y, x_aligned, y_aligned, align_type, iter + 1, score)
    
    # if the move is vertical
    if j > 0 and 'v' in elem[1]:
        x_aligned.append(x[i - 1])
        y_aligned.append('_')
        return opt_align(mat, i - 1, j, first_col, first_row, x, y, x_aligned, y_aligned, align_type, iter + 1, score)


# this function check for the highest value in the entire matrix
# and returns it as the starting loc for local traceback
# parameter:
# mat - m x n penalty matrix that has been populated with values
def local_traceback_start(mat):
    max_elem = 0
    max_ij = None
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if isinstance(mat[i][j], list):
                elem = mat[i][j][0]
            else: elem = mat[i][j]

            if elem > max_elem:
                max_elem = elem
                max_ij = (i, j)

    return [val for val in max_ij] + [max_elem]


# returns start location for semiglobal matrix backtracing
# by checking the last row and last column of the 
# populated penalty matrix
# parameter:
# mat - specifically an m x n penalty matrix that is semiglobal and already filled.
def semi_traceback_start(mat):

    # initialize optimum val and optimum val idx to 0
    end_col_opt, end_row_opt = float('-inf'), float('-inf')
    end_row_opt_idx, end_col_opt_idx = 0, 0

    # grab last row and column from mat
    last_col = [row[-1] for row in mat[1:]]
    last_row = mat[-1][1:]
    print(last_row)

    # find optimum value in last column
    for idx, i in enumerate(last_row): 
        if isinstance(i, list): i = i[0]
        if i > end_row_opt:
            end_row_opt = i
            end_row_opt_idx = idx
            print(i)
            print(idx)

    # find optimum value in last row
    for idx, j in enumerate(last_col):
        if isinstance(j, list): j = j[0]
        if j > end_col_opt:
            end_col_opt = j
            end_col_opt_idx = idx
            print("in j loop", idx, end_col_opt_idx)
    
    # just a print statement because I was curious.
    # True in the case of mat[n][m] being the opt, or if they happen to match
    # if end_col_opt == end_row_opt:
    #     print("Max val of last row is the same as the max val of the last col: {}".format(end_col_opt))

    # get max of max of last row and max of last column
    max_of_row_col = max(end_col_opt, end_row_opt)

    # if the max is from the last column return the relative i,jth idx
    if max_of_row_col == last_col[end_col_opt_idx][0]:
        print(f"val in last col with end_col_opt_idx: {end_col_opt_idx} len of mat -1 is: {len(mat) - 1}")
        # return [end_col_opt_idx, len(mat[0]) - 1] # i, j pair
        # return [len(mat) - 1, end_col_opt_idx + 1, max_of_row_col]

        return [end_col_opt_idx + 1, len(mat[0]) - 1, max_of_row_col]

    
    # if the max is from the last row return the relative i,jth idx
    if max_of_row_col == last_row[end_row_opt_idx][0]:
        # return (len(mat) - 1, end_row_opt_idx) # i, j pair
        # return [end_row_opt_idx + 1, len(mat[0]) - 1, max_of_row_col]
        print(last_row)
        print(f"val in last row with end_row_opt_idx: {end_row_opt_idx} len of mat -1 is: {len(mat) - 1}")
        return [len(mat) - 1, end_row_opt_idx, max_of_row_col]