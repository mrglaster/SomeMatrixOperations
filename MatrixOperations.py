# -*- coding: utf-8 -*-
"""MathStuff.ipynb

Набор функций для решения некоторых задач по математике

Парочка матриц для тестирования:

X = [[12,7,3],
    [4 ,5,6],
    [7 ,8,9]]

Y = [[5,8,1,2],
    [6,7,3,0],
    [4,5,9,2]]    


Z = [
      [2, 3, 1], 
      [2, 2, 2],
      [3, 1, 5]
    ]
"""

import numpy as np
import sys

def inverse_matrix(matrix_origin):
    """
    Функция получает на вход матрицу, затем добавляет к ней единичную матрицу,
    проводит элементарные преобразования по строкам с первоначальной, добиваясь получения слева единичной матрицы.
    В этом случае справа окажется матрица, которая является обратной к заданнй первоначально
    """
    # Склеиваем 2 матрицы: слева - первоначальная, справа - единичная
    n = matrix_origin.shape[0]
    m = np.hstack((matrix_origin, np.eye(n)))
    for nrow, row in enumerate(m):
        # nrow равен номеру строки
        # row содержит саму строку матрицы
        divider = row[nrow] # диагональный элемент
        # делим на диагональный элемент:
        row /= divider
        # теперь вычитаем приведённую строку из всех нижележащих строк:
        for lower_row in m[nrow +1:]:
            factor = lower_row[nrow] # элемент строки в колонке nrow
            lower_row -= factor *row # вычитаем, чтобы получить ноль в колонке nrow
    # обратный ход:
    for k in range(n - 1, 0, -1):
        for row_ in range(k - 1, -1, -1):
            if m[row_, k]:
                # 1) Все элементы выше главной диагонали делаем равными нулю
                m[row_, :] -= m[k, :] * m[row_, k]
    return m[:, n:].copy()

def LU_decomposition(A):

    """
    Тип входных данных: матрица A

    Что делает функция?
    LU-декомпозиция - представление исходной матрицы A в виде произведения двух матриц L и U,
    где L - нижняя треугольная матрица, а U - верхняя треугольная матрица
    LU-разложение используется для решения систем линейных уравнений, обращения матриц и вычисления определителя.

    Возвращаемые значения: матрицы L и U

    """
    if is_square_matrix(A):
        n = len(A[0])
        L = np.zeros([n, n])
        U = np.zeros([n, n])
        for i in range(n):
            L[i][i] = 1
            if i == 0:
                U[0][0] = A[0][0]
                for j in range(1, n):
                    U[0][j] = A[0][j]
                    L[j][0] = A[j][0] / U[0][0]
            else:
                for j in range(i, n):  # считаем матрицу U
                    c = 0
                    for k in range(0, i):
                        c = c + L[i][k] * U[k][j]
                    U[i][j] = A[i][j] - c
                for j in range(i + 1, n):  # считаем матрицу L
                    c = 0
                    for k in range(0, i):
                        c = c + L[j][k] * U[k][i]
                    if U[i][i] != 0:
                        L[j][i] = (A[j][i] - c) / U[i][i]
                    else:
                        L[j][i] = 0
        return L, U
    print("Данная матрица не является квадратной! Метод LU декомпозиции применить тут нельзя!")
    sys.exit()

def calculate_determinant(matrix):
    """
    Входные данные: исходная матрица matrix

    Что делает функция?
    Функция находит определитель матрица путём перемножения
    диагональных элеметов матрицы U (рез-та LU-декомпозиции)
    Данная реализация предпочтительнее "классического" нахождения
    определителя через миноры, тк алгоритм при использовании
    последних имеет сложность O(n)=n!. Вместо этого используется
    часть результата LU-декомпозиции, сложность которой O(n)=n^3

    Возвращаемое значение: определитель матрицы
    """
    L,U = LU_decomposition(matrix)
    O = 1
    for i in range(len(U[0])):
        O *= U[i][i]
    return O

def transpose_matrix(matrix):
    """
    Функция для получения транспонированной матрицы. На вход поступает матрица (можно обычную, можно матрица Nympy)
    Транспонированная матрица - исходная матрица, в которой строки и столбцы поменяны местами
    Тип возвращаемых данных - матрица.
    """
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def input_matrix():
    print("Введите количество строк матрицы")
    rows = int(input())
    print("Введите количество столбцов матрицы")
    cols = int(input())
    if rows>1 and cols>1:
        A = [0] * rows
        for i in range(rows):
            print("введите строку матрицы №", i+1)
            str1 = input()
            str2 = str1.split()
            A[i] = [0] * cols
            for j in range(cols):
                A[i][j] = int(str2[j])
        return A
    print("Неправильная размерность матрицы!")
    sys.exit()

def is_square_matrix(matrix):
  if len(matrix)==len(matrix[0]):
    return True
  return False

def print_matrix(matrix):
    print(np.matrix(matrix))

def consist_matrix_check(matrix_A, matrix_B):
    """
    Входные данные: две матрицы любых разрядностей

    Что реализует функция:
    Проверка возможности перемножения матриц.
    Операция умножения двух матриц выполнима только в том случае,
    если число столбцов в первом сомножителе равно числу строк во втором;
    в этом случае говорят, что матрицы согласованы

    тип возвращаемого значения - True/False
    """
    if len(matrix_A[0]) == len(matrix_B):
        return True
    return False

def multiply_matrix(matrix_A, matrix_B):
    """
    Тип входных данных: две матрицы

    Что делает функция?
    функция перемножает две матрицы "строка на столбец".
    """
    if consist_matrix_check(matrix_A, matrix_B):
       return [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*matrix_B)] for X_row in matrix_A]

def worker():
    """
    функция-главное меню.
    
    """

    print("Что будем находить?")
    print("1) обратную матрицу")
    print("2) транспонированную матрицу")
    print("3) определитель матрицы")
    print("4) перемножить две матрицы")
    answer = int(input())
    if answer == 1:
        A = np.array(input_matrix(), dtype='double')
        if int(abs(calculate_determinant(A)))!=0:
            print('\n')
            print("Обратная матрица",'\n')
            print_matrix(inverse_matrix(np.copy(A)))
        else:
            print("Определитель равен 0. Утилита не может определить обратную матрицу.")
    elif answer == 2:
        A = np.array(input_matrix(), dtype='double')
        print('\n' * 2)
        print("Транспонированная матрица", '\n' )
        print_matrix(transpose_matrix(A))
    elif answer == 3:
        A = np.array(input_matrix(), dtype='double')
        print('\n' )
        print("Определитель матрицы:", '\n')
        print(calculate_determinant(A))
    elif answer == 4:
        A = np.array(input_matrix(), dtype='double')
        print('\n')
        print("Теперь перейдём ко второй матрице")
        print('\n')
        B = np.array(input_matrix(), dtype='double')
        print('\n'*2)
        print("Результат перемножения матриц: ", '\n')
        print_matrix(multiply_matrix(A, B))
    else:
        print("Неизвестный аргумент!")
        sys.exit()

def main():
   worker()

if __name__=='__main__':
    main()
