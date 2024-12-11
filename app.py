from flask import Flask, render_template, request
from fractions import Fraction

app = Flask(__name__)

#globales

def sumar_matrices(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def restar_matrices(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def multiplicar_matrices(a, b):
    filas_a, columnas_a = len(a), len(a[0])
    filas_b, columnas_b = len(b), len(b[0])
    if columnas_a != filas_b:
        raise ValueError("Las dimensiones no son compatibles para la multiplicación.")
    resultado = [[0] * columnas_b for _ in range(filas_a)]
    for i in range(filas_a):
        for j in range(columnas_b):
            for k in range(columnas_a):
                resultado[i][j] += a[i][k] * b[k][j]
    return resultado

#x matriz

def transponer_matriz(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

def determinante_matriz(m): 
    if len(m) != len(m[0]):
        raise ValueError("La matriz no es cuadrada.")
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]  # a x d - b x c
    
    det = 0
    for c in range(len(m)):  # c = indice
        menor = [fila[:c] + fila[c+1:] for fila in m[1:]]  # Submatriz (eliminamos la fila 0 y la columna c de cada fila)
        det += ((-1) ** c) * m[0][c] * determinante_matriz(menor) #  determinante * cofactor
    return det

def inversa_matriz(m):
    if len(m) != len(m[0]):
        raise ValueError("La matriz no es cuadrada.")
    det = determinante_matriz(m)
    if det == 0:
        raise ValueError("El determinante es 0, la matriz no tiene inversa.")
    m_fracciones = [[Fraction(x) for x in fila] for fila in m]
    
    # Paso 5: Calcular la matriz adjunta
    adjunta = [[((-1) ** (i + j)) * determinante_matriz(
                [fila[:j] + fila[j+1:] for fila in (m_fracciones[:i] + m_fracciones[i+1:])]) 
                for j in range(len(m))] for i in range(len(m))]
    
    # Paso 6: Transponer la matriz adjunta (intercambiar filas y columnas)
    adjunta_transpuesta = transponer_matriz(adjunta)
    
    # Paso 7: Calcular la matriz inversa dividiendo cada elemento de la adjunta transpuesta por el determinante
    inversa = [[adjunta_transpuesta[i][j] / Fraction(det) for j in range(len(m))] for i in range(len(m))]
    
    # Paso 8: Retornar la matriz inversa
    return inversa

def multiplicar_por_dos(m):
    return [[elemento * 2 for elemento in fila] for fila in m]

def elevar_al_cuadrado(m):
    return [[elemento ** 2 for elemento in fila] for fila in m]

@app.route('/', methods=['GET', 'POST'])
def inicio():
    resultado = None
    error = None
    es_determinante = False

    # default o get (form)
    filas_a = int(request.form.get('filas_a', 4))
    columnas_a = int(request.form.get('columnas_a', 4))
    filas_b = int(request.form.get('filas_b', 4))
    columnas_b = int(request.form.get('columnas_b', 4))

    
    matriz_a = [[0] * columnas_a for _ in range(filas_a)]
    matriz_b = [[0] * columnas_b for _ in range(filas_b)]

    if request.method == 'POST':
        try:
            
            filas_a = int(request.form.get('filas_a', 4))
            columnas_a = int(request.form.get('columnas_a', 4))
            filas_b = int(request.form.get('filas_b', 4))
            columnas_b = int(request.form.get('columnas_b', 4))

            
            matriz_a = [
                [int(request.form.get(f'a{i}{j}', 0)) for j in range(columnas_a)] for i in range(filas_a)
            ]
            matriz_b = [
                [int(request.form.get(f'b{i}{j}', 0)) for j in range(columnas_b)] for i in range(filas_b)
            ]

            
            operacion = request.form.get('operacion')
            if operacion == 'sumar':
                resultado = sumar_matrices(matriz_a, matriz_b)
            elif operacion == 'restar':
                resultado = restar_matrices(matriz_a, matriz_b)
            elif operacion == 'multiplicar':
                resultado = multiplicar_matrices(matriz_a, matriz_b)
            elif operacion == 'determinante_a':
                resultado = determinante_matriz(matriz_a)
                es_determinante = True
            elif operacion == 'determinante_b':
                resultado = determinante_matriz(matriz_b)
                es_determinante = True
            elif operacion == 'transponer_a':
                resultado = transponer_matriz(matriz_a)
            elif operacion == 'transponer_b':
                resultado = transponer_matriz(matriz_b)
            elif operacion == 'inversa_a':
                resultado = inversa_matriz(matriz_a)
            elif operacion == 'inversa_b':
                resultado = inversa_matriz(matriz_b)
            elif operacion == 'multiplicar_x2_a':
                resultado = multiplicar_por_dos(matriz_a)
            elif operacion == 'multiplicar_x2_b':
                resultado = multiplicar_por_dos(matriz_b)
            elif operacion == 'elevar_a2_a':
                resultado = elevar_al_cuadrado(matriz_a)
            elif operacion == 'elevar_a2_b':
                resultado = elevar_al_cuadrado(matriz_b)
            else:
                raise ValueError("Operación no válida.")
        except ValueError as ve:
            error = f"Error de entrada: {ve}"
        except Exception as e:
            error = f"Ocurrió un error: {e}"

    return render_template(
    'index.html',
    resultado=resultado,
    error=error,
    es_determinante=es_determinante,
    filas_a=filas_a,
    columnas_a=columnas_a,
    filas_b=filas_b,
    columnas_b=columnas_b,
    matriz_a=matriz_a,
    matriz_b=matriz_b
)

if __name__ == '__main__':
    app.run(debug=True)
