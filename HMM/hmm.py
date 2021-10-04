import sys
from decimal import *


def main():
    transition_matrix, emission_matrix, initial_state_distribution = read_data()
    next_observation_distribution = predict_next_observations(transition_matrix, emission_matrix, initial_state_distribution)
    print_ans(next_observation_distribution)

def print_ans(matrix):
    print(len(matrix), len(matrix[0]), end=' ')
    for row in matrix:
        for element in row:
            print(str(element), end=' ')


def predict_next_observations(transition_matrix, emission_matrix, initial_state_distribution):
    next_state_distribution = matrix_multiplication(initial_state_distribution, transition_matrix)
    observation_distribution = matrix_multiplication(next_state_distribution, emission_matrix)
    return observation_distribution

def matrix_multiplication(m1, m2):
    assert len(m1[0]) == len(m2)
    result = []
    for i in range(len(m1)):
        row = []
        for j in range(len(m2[0])):
            row.append(dot_product(m1[i], get_column(m2, j)))
        result.append(row)
    return result

def dot_product(l1, l2):
    assert len(l1) == len(l2)
    sum = Decimal(0)
    for i in range(len(l1)):
        sum += l1[i] * l2[i]
    return sum
def get_column(matrix, axis):
    rows = len(matrix)
    column = []
    for i in range(rows):
        column.append(matrix[i][axis])
    return column

def read_data():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip())
    return create_matrix(lines[0]), create_matrix(lines[1]), create_matrix(lines[2])


def create_matrix(input_line):
    input_line = input_line.split()
    rows = int(input_line[0])
    columns = int(input_line[1])
    val_counter = 2
    matrix = []
    for i in range(rows):
        column = []
        for j in range(columns):
            column.append(Decimal(input_line[val_counter]))
            val_counter += 1
        matrix.append(column)
    return matrix




main()
