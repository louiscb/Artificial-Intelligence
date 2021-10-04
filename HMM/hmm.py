import sys


def main():
    transition_matrix, emission_matrix, initial_state_distribution = read_data()
    predict_next_observations(transition_matrix, emission_matrix, initial_state_distribution)

def predict_next_observations(transition_matrix, emission_matrix, initial_state_distribution):
    next_state_distribution = calculate_next_state_distribution(initial_state_distribution, transition_matrix)
    observation_distribution = calculate_observation_distribution(next_state_distribution, emission_matrix)
    return observation_distribution

def calculate_observation_distribution(next_state_distribution, emission_matrix):
    pass

def calculate_next_state_distribution(current_state_distribution, transition_matrix):
    return None

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
            column.append(float(input_line[val_counter]))
            val_counter += 1
        matrix.append(column)
    return matrix




main()
