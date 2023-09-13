from math import isclose, sqrt

def multMM(matrices):
    resultado = matrices[0]

    for i in range(1, len(matrices)):
        m2 = matrices[i]
        temp_resultado = [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]]

        for i in range(len(resultado)):
            for j in range(len(m2[0])):
                for k in range(len(resultado[0])):
                    temp_resultado[i][j] += resultado[i][k] * m2[k][j]

        resultado = temp_resultado

    return resultado

def multMV(m, v):
    resultado = [0, 0, 0, 0]
    for i in range(len(m)):
        for j in range(len(m[0])):
            resultado[i] += m[i][j] * v[j]

    return resultado

def bcCoords(A, B, C, P):
    BCP = abs((P[0] * C[1] + C[0] * B[1] + B[0] * P[1]) - (P[1] * C[0] + C[1] * B[0] + B[1] * P[0]))
    CAP = abs((A[0] * C[1] + C[0] * P[1] + P[0] * A[1]) - (A[1] * C[0] + C[1] * P[0] + P[1] * A[0]))
    ABP = abs((A[0] * B[1] + B[0] * P[1] + P[0] * A[1]) - (A[1] * B[0] + B[1] * P[0] + P[1] * A[0]))
    
    ABC = abs((A[0] * B[1] + B[0] * C[1] + C[0] * A[1]) - (A[1] * B[0] + B[1] * C[0] + C[1] * A[0]))

    """ BCP = (B[1] - C[1]) * (P[0] - C[0]) + (C[0] - B[0]) * (P[1] - C[1])
    CAP = (C[1] - A[1]) * (P[0] - C[0]) + (A[0] - C[0]) * (P[1] - C[1])
    #ABP = (A[1] - B[1]) * (P[0] - C[0]) + (B[0] - A[0]) * (P[1] - C[1])
    
    ABC = (B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1]) """

    if ABC == 0:
        return None

    u = BCP / ABC
    v = CAP / ABC
    w = ABP / ABC
    #w = 1 - u - v

    if (0 <= u <= 1) and (0 <= v <= 1) and (0 <= w <= 1) and isclose(u + v + w, 1.0):
        return (u, v, w)
    else:
        return None

def invertMatrix(matrix):
    if len(matrix) != len(matrix[0]):
        raise ValueError("La matrix debe ser cuadrada para tener una inversa.")

    n = len(matrix)
    identidad = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    for col in range(n):
        diagonal = matrix[col][col]
        if diagonal == 0:
            raise ValueError("La matrix no tiene inversa.")

        for j in range(n):
            matrix[col][j] /= diagonal
            identidad[col][j] /= diagonal
        
        for i in range(n):
            if i == col:
                continue
            
            factor = matrix[i][col]
            for j in range(n):
                matrix[i][j] -= factor * matrix[col][j]
                identidad[i][j] -= factor * identidad[col][j]

    return identidad

def subtractVectors(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Los vectores deben tener la misma longitud para realizar la resta.")

    resultado = [v1[i] - v2[i] for i in range(len(v1))]
    return resultado

def normVector(vector):
    magnitud = sqrt(sum(x ** 2 for x in vector))
    
    if magnitud == 0:
        raise ValueError("No se puede normalizar un vector nulo.")
    
    vector_normalizado = [x / magnitud for x in vector]
    
    return vector_normalizado

def cross(v1, v2):
    resultado = [0, 0, 0]
    
    resultado[0] = v1[1] * v2[2] - v1[2] * v2[1]
    resultado[1] = v1[2] * v2[0] - v1[0] * v2[2]
    resultado[2] = v1[0] * v2[1] - v1[1] * v2[0]
    
    return resultado

def dot(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Los vectores deben tener la misma longitud para calcular el producto punto.")

    resultado = sum(v1[i] * v2[i] for i in range(len(v1)))
    return resultado

def vectorNegative(vector):
    negative = [-x for x in vector]
    return negative

def multVectorScalar(vector, scalar):
    result = [scalar * value for value in vector]
    return result

def reflectVector(vector, normal):
    dot_product = dot(vector, normal)
    reflection = [2 * dot_product * normal[i] - vector[i] for i in range(len(vector))]
    return reflection

def vectorMagnitude(vector):
    return sum(i ** 2 for i in vector) ** 0.5
