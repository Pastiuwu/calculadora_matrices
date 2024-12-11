# operations/matrix_operations.py

def validate_square_matrix(matrix):
    """Verifica si la matriz es cuadrada."""
    if len(matrix) != len(matrix[0]):
        raise ValueError("La matriz debe ser cuadrada.")

def add_matrices(A, B):
    """Suma de matrices."""
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Las matrices deben tener las mismas dimensiones.")
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def subtract_matrices(A, B):
    """Resta de matrices."""
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Las matrices deben tener las mismas dimensiones.")
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def multiply_matrices(A, B):
    """Multiplicación de matrices."""
    if len(A[0]) != len(B):
        raise ValueError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda.")
    return [
        [sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
        for i in range(len(A))
    ]

def transpose_matrix(matrix):
    """Transposición de matriz."""
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def calculate_determinant(matrix):
    """Calcula el determinante de una matriz cuadrada."""
    validate_square_matrix(matrix)

    # Caso base: matriz 2x2
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    # Caso general: expansión por cofactores
    det = 0
    for col in range(len(matrix)):
        submatrix = [
            [matrix[i][j] for j in range(len(matrix)) if j != col]
            for i in range(1, len(matrix))
        ]
        det += ((-1) ** col) * matrix[0][col] * calculate_determinant(submatrix)
    return det

def calculate_inverse(matrix):
    """Calcula la inversa de una matriz cuadrada."""
    validate_square_matrix(matrix)
    determinant = calculate_determinant(matrix)
    if determinant == 0:
        raise ValueError("La matriz no es invertible.")

    size = len(matrix)
    cofactors = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            submatrix = [
                [matrix[x][y] for y in range(size) if y != j]
                for x in range(size) if x != i
            ]
            cofactors[i][j] = ((-1) ** (i + j)) * calculate_determinant(submatrix)

    adjugate = transpose_matrix(cofactors)
    return [[adjugate[i][j] / determinant for j in range(size)] for i in range(size)]

def scalar_multiply(matrix, scalar):
    """Multiplicación de una matriz por un escalar."""
    return [[element * scalar for element in row] for row in matrix]
