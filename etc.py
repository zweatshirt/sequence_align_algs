# Author: Zachery Linscott

# This is just to print the matrices somewhat nicely.
# parameter:
# mat - any m x n matrix
def pprint(mat):
    print('\n\n'.join(['\t'.join([str(col[0] if isinstance(col, list) else col) for col in row]) for row in mat]))
    # print('\n\n'.join(['\t'.join([str(col) for col in row]) for row in mat]))
    print('\n')