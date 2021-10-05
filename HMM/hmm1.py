from hmm_lib import *


def main():
    transition_matrix, emission_matrix, initial_state_distribution, emission_sequence = read_data()
    probability = calculate_probability_of_observed_sequence(transition_matrix, emission_matrix, initial_state_distribution,
                                               emission_sequence)
    print(probability, end='')


def calculate_probability_of_observed_sequence(transition_matrix, emission_matrix, initial_state_distribution,
                                               emission_sequence):
    alpha = initialize_alpha(initial_state_distribution, emission_matrix, emission_sequence[0])
    for t in range(1, len(emission_sequence)):
        #perform update of alpha
        alpha = update_alpha(alpha, transition_matrix, emission_matrix, emission_sequence[t])
    #marginalize out the state to get observation probability
    return marginalize(alpha)


def update_alpha(alpha, transition_matrix, emission_matrix, observation):
    new_alpha = []
    for i in range(len(alpha)):
        state_prob = 0
        for j in range(len(transition_matrix)):
            state_prob += transition_matrix[j][i] * alpha[j]
        new_alpha.append(state_prob)
    return element_wise_multiplication(get_column(emission_matrix, observation), new_alpha)


def initialize_alpha(initial_state_distribution, emission_matrix, first_observation):
    # probability of given observation, by state
    relevant_observation_probabilities = get_column(emission_matrix, first_observation)
    probability_of_observation_by_state = element_wise_multiplication(initial_state_distribution[0],
                                                                      relevant_observation_probabilities)
    return probability_of_observation_by_state


main()
