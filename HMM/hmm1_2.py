from hmm_lib import *


def main():
    transition_matrix, emission_matrix, initial_state_distribution, emission_sequence = read_data()
    calculate_most_likely_state_sequence(transition_matrix, emission_matrix, initial_state_distribution,
                                         emission_sequence)
    # calculate_probability_of_observed_sequence(transition_matrix, emission_matrix, initial_state_distribution, emission_sequence)


def calculate_most_likely_state_sequence(transition_matrix, emission_matrix, initial_state_distribution,
                                         emission_sequence):
    sigma = initialize_alpha(initial_state_distribution, emission_matrix, emission_sequence[0])
    sigma_index = []
    for t in range(1, len(emission_sequence)):
        sigma, next_sigma_index = update_sigma(sigma, transition_matrix, emission_matrix, emission_sequence[t])
        sigma_index.append(next_sigma_index)
    most_likely_state_sequence = backtrack(sigma, sigma_index)
    for state in most_likely_state_sequence:
        print(state, end=' ')


def calculate_probability_of_observed_sequence(transition_matrix, emission_matrix, initial_state_distribution,
                                               emission_sequence):
    alpha = initialize_alpha(initial_state_distribution, emission_matrix, emission_sequence[0])
    for t in range(1, len(emission_sequence)):
        # perform update of alpha
        alpha = update_alpha(alpha, transition_matrix, emission_matrix, emission_sequence[t])
    # marginalize out the state to get observation probability
    return marginalize(alpha)


def backtrack(sigma, most_likely_state_sequence):
    most_likely_last_state = index_of_max_and_value(sigma)[0]
    reverse_state_sequence = [most_likely_last_state]
    for element in reversed(most_likely_state_sequence):
        most_likely_parent = element[most_likely_last_state]
        reverse_state_sequence.append(most_likely_parent)
        most_likely_last_state = most_likely_parent
    return list(reversed(reverse_state_sequence))


def update_sigma(sigma, transition_matrix, emission_matrix, observation):
    new_sigma = []
    new_sigma_index = []
    # for each state
    for current_state in range(len(sigma)):
        sigma_of_state_i_per_predecessor_state = element_wise_multiplication(
            element_wise_multiplication(sigma, get_column(transition_matrix, current_state)),
            [emission_matrix[current_state][observation]] * len(sigma))
        # choose "j" (previous state) that maximizes current probability as this is most likely predecessor
        most_likely_predecessor_state, sigma_of_i = index_of_max_and_value(sigma_of_state_i_per_predecessor_state)
        new_sigma.append(sigma_of_i)
        new_sigma_index.append(most_likely_predecessor_state)
    return new_sigma, new_sigma_index




main()
