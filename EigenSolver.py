# god bless mrs. Mukash
from typing import List

from matrix import Matrix

def identity_matrix(n: int) -> Matrix:
    """Create an identity matrix of size n x n."""
    return Matrix([[1 if i == j else 0 for j in range(n)] for i in range(n)])

def subtract_lambda_I(A: Matrix, lambd: float) -> Matrix:
    """Subtract λI from matrix A."""
    n = A.shape()[0]
    I = identity_matrix(n)
    return A.add(I.scalar_multiply(-lambd))

def get_char_polynomial_coefs(A: 'Matrix') -> List[float]:
    n = A.shape()[0]
    assert n <= 3, "This function only supports matrices up to 3x3."

    if n == 1:
        return [1, -A.get(0, 0)]

    elif n == 2:
        c1 = A.trace()
        c0 = A.determinant()
        return [1, -c1, c0]

    elif n == 3:
        c2 = A.trace()

        m00 = A.minor(0, 0).determinant()
        m11 = A.minor(1, 1).determinant()
        m22 = A.minor(2, 2).determinant()

        c1 = m00 + m11 + m22 

        c0 = A.determinant()

        return [1, -c2, c1, -c0]

def row_echelon_form(matrix):
    mat = [row[:] for row in matrix.data]  
    rows, cols = matrix.shape()

    for i in range(min(rows, cols)):
        # Find the pivot for column i
        if mat[i][i] == 0:
            for j in range(i+1, rows):
                if mat[j][i] != 0:
                    # Swap rows
                    mat[i], mat[j] = mat[j], mat[i]
                    break
        if mat[i][i] != 0:
            # Normalize the pivot row
            pivot_value = mat[i][i]
            mat[i] = [element / pivot_value for element in mat[i]]

        # Eliminate all entries in column i below the pivot
        for j in range(i+1, rows):
            row_factor = mat[j][i]
            mat[j] = [mat[j][k] - row_factor * mat[i][k] for k in range(cols)]

    return mat

def reduced_row_echelon_form(matrix):
    mat = row_echelon_form(matrix)
    rows, cols = matrix.shape()

    # Eliminate entries above the pivots to achieve RREF
    for i in range(min(rows, cols)-1, -1, -1):
        pivot_col = next((j for j, x in enumerate(mat[i]) if x != 0), None)
        if pivot_col is not None:
            for j in range(i-1, -1, -1):
                row_factor = mat[j][pivot_col]
                mat[j] = [mat[j][k] - row_factor * mat[i][k] for k in range(cols)]

    return mat

def extract_eigenvector_from_rref(independent_rows):
    eigenvector = [0 for i in range(len(independent_rows[0]))]

    for main_var, row in enumerate(independent_rows):
        if row[main_var] == 1.0:
            for sup_var, value in enumerate(row[main_var+1:]):
                if value != 0:
                    eigenvector[main_var]=-value # f.e.: x+2z=0 -> x=-2z 
                    eigenvector[sup_var+main_var+1]=1.0 # then z is 1 
                    break

    return eigenvector # (x,y,z) = (-2,0,1) if y=0

def get_zero_variables(independent_rows):
    """
    variables that weren'r mentioned are free and form an eigenvector
     that consists only with them
    """
    zero_vars_flag = [1 for i in range(len(independent_rows[0]))]

    for i, row in enumerate(independent_rows):
        for j, value in enumerate(row):
            if value != 0:
                zero_vars_flag[j] = 0

    zero_vars = []
    for var, flag in enumerate(zero_vars_flag):
        if flag:
            zero_vars.append(var)

    return zero_vars

def find_eigenvector(A: Matrix, lambd: float) -> List[float]:
    """Find the eigenvector corresponding to the eigenvalue λ."""
    # Form the matrix A - λI
    A_minus_lambda_I = subtract_lambda_I(A, lambd)

    # Perform Gaussian elimination
    rref = reduced_row_echelon_form(A_minus_lambda_I)
    independent_rows = [row for row in rref if any(row)]

    if independent_rows == identity_matrix(A.num_rows).data:
        return None
    
    eigenvector = extract_eigenvector_from_rref(independent_rows)
    eigenvectors = [eigenvector] # might be more than 1 if we add eigenvec_from_zero
    
    zero_vars = get_zero_variables(independent_rows)

    if zero_vars is not None:
        eigenvec_from_zero = [0 for i in range(len(independent_rows[0]))]
        for var in zero_vars:
            eigenvec_from_zero[var] = 1
            eigenvectors.append(eigenvec_from_zero)

    return eigenvectors
        
    
def get_eigenvectors(A: Matrix, eigenvalues: List[float]):
    eigenvectors = []
    
    for lambd in eigenvalues:
        eigenvector = find_eigenvector(A, lambd)
        if eigenvector is not None: 
            eigenvectors += eigenvector

    return eigenvectors