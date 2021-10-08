import sys
from decimal import *


def print_ans(matrix):
    print(len(matrix), len(matrix[0]), end=' ')
    for row in matrix:
        for element in row:
            print(str(element), end=' ')


def hmm0():
    transition_matrix, emission_matrix, initial_state_distribution = read_data()
    next_observation_distribution = predict_next_observations(transition_matrix, emission_matrix,
                                                              initial_state_distribution)
    print_ans(next_observation_distribution)


def update_alpha(alpha, transition_matrix, emission_matrix, observation):
    new_alpha = []
    for i in range(len(alpha)):
        state_prob = 0
        for j in range(len(transition_matrix)):
            state_prob += transition_matrix[j][i] * alpha[j]
        new_alpha.append(state_prob)
    return element_wise_multiplication(get_column(emission_matrix, observation), new_alpha)


def initialize_alpha(initial_state_distribution, emission_matrix, first_observation):
    # emission_matrix holds the conditional distributions, multiplied by the state_distribution we are conditioning on
    # results in the joint distribution. For each state, with Observation = first_observation.
    relevant_observation_probabilities = get_column(emission_matrix, first_observation)
    joint_pdf_state_and_observation = element_wise_multiplication(initial_state_distribution[0],
                                                                  relevant_observation_probabilities)
    return joint_pdf_state_and_observation


def predict_next_observations(transition_matrix, emission_matrix, current_state_distribution):
    next_state_distribution = matrix_multiplication(current_state_distribution, transition_matrix)
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


def element_wise_multiplication(l1, l2):
    rows = []
    for i in range(len(l1)):
        rows.append(l1[i] * l2[i])
    return rows


def dot_product(l1, l2):
    assert len(l1) == len(l2)
    sum = Decimal(0)
    for i in range(len(l1)):
        sum += l1[i] * l2[i]
    return sum


def marginalize(matrix):
    prob = 0
    for i in range(len(matrix)):
        prob += matrix[i]
    return prob


def get_column(matrix, axis):
    rows = len(matrix)
    column = []
    for i in range(rows):
        column.append(matrix[i][axis])
    return column


def index_of_max_and_value(l1):
    index = 0
    max = -1
    for i, val in enumerate(l1):
        if val > max:
            max = val
            index = i
    return index, max


def read_data():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip())
    # return create_matrix(lines[0]), create_matrix(lines[1]), create_matrix(lines[2])
    return create_matrix(lines[0]), create_matrix(lines[1]), create_matrix(lines[2]), read_emission_sequence(lines[3])


def read_emission_sequence(input_line):
    input_line = input_line.split()
    num_elems = int(input_line[0])
    emission_sequence = []
    for i in range(1, num_elems + 1):
        emission_sequence.append(int(input_line[i]))
    return emission_sequence


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
