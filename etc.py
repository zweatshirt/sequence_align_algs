# Author: Zachery Linscott

# This is just to print the matrices somewhat nicely.
# parameter:
# mat - any m x n matrix
def pprint(mat):
    print('\n\n'.join(['\t'.join([str(col) for col in row[1:]]) for row in mat[1:]]))
    print('\n')