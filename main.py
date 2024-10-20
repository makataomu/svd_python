from Matrix import Matrix
from CubicEquation import CubicEquation
from EigenSolver import get_char_polynomial_coefs, get_eigenvectors

A = Matrix([[3,-1,1], [7, -5,1], [6,-6,2]])
c3, c2, c1, c0 = get_char_polynomial_coefs(A) # c3 always 1 
eigenvalues = CubicEquation(c3, c2, c1, c0) 
eigenvectors = get_eigenvectors(A, eigenvalues)
eigenvalues, eigenvectors