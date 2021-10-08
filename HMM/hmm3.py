from hmm_lib import *


def main():
    transition_matrix, emission_matrix, initial_state_distribution, emission_sequence = read_data()
    baum_welch(transition_matrix, emission_matrix, initial_state_distribution, emission_sequence)


def baum_welch(transition_matrix, emission_matrix, initial_state_distribution, emission_sequence):
    converged = False
    while not converged:
        alphas = run_me_my_alphas(transition_matrix, emission_matrix, initial_state_distribution, emission_sequence)
        betas = run_me_my_betas(transition_matrix, emission_matrix, initial_state_distribution, emission_sequence)
        di_gammas, gammas = run_me_my_gammas(alphas, betas, transition_matrix, emission_matrix, emission_sequence)
        new_transition_matrix, new_emission_matrix = estimate_transition_and_emission_matrix(di_gammas, gammas, len(emission_matrix[0]), emission_sequence)
        if has_converged(transition_matrix, emission_matrix, new_transition_matrix, new_emission_matrix):
            converged = True
        transition_matrix = new_transition_matrix
        emission_matrix = new_emission_matrix
        initial_state_distribution = [gammas[0]]

    return transition_matrix, emission_matrix

def has_converged(old_transition_matrix, old_emission_matrix, new_transition_matrix, new_emission_matrix):
    return old_transition_matrix == new_transition_matrix and old_emission_matrix == new_emission_matrix

def estimate_transition_and_emission_matrix(di_gammas, gammas, no_possible_observations, emission_sequence):
    new_transition_matrix = []
    new_emission_matrix = []
    for i in range(len(di_gammas[0])):
        transition_column = []
        emission_column = []
        denominator = marginalize(get_column(gammas, i)[:-1:])  # is this right?
        for j in range(len(di_gammas[0])):
            transition_numerator = marginalize_di_gamma(di_gammas, i, j)
            transition_column.append(transition_numerator / denominator)
        new_transition_matrix.append(transition_column)
        for observation in range(no_possible_observations):
            emission_numerator = 0
            for t in range(len(emission_sequence) - 1):
                if observation == emission_sequence[t]:
                    emission_numerator += gammas[t][i]
            emission_column.append(emission_numerator / denominator)
        new_emission_matrix.append(emission_column)
    return new_transition_matrix, new_emission_matrix


def marginalize_di_gamma(di_gammas, i, j):
    sum = 0
    for di_gamma in di_gammas[:-1:]:
        sum += di_gamma[i][j]
    return sum


def run_me_my_gammas(alphas, betas, transition_matrix, emission_matrix, emission_sequence):
    di_gammas = []
    gammas = []
    for t in range(len(emission_sequence) - 1):
        di_gamma = compute_di_gamma(alphas[t], betas[t + 1], transition_matrix, emission_matrix,
                                    emission_sequence[t + 1], alphas[-1])
        gamma = compute_gamma(di_gamma)
        di_gammas.append(di_gamma)
        gammas.append(gamma)
    return di_gammas, gammas


def run_me_my_alphas(transition_matrix, emission_matrix, initial_state_distribution, emission_sequence):
    alphas = []
    curr_alpha = initialize_alpha(initial_state_distribution, emission_matrix, emission_sequence[0])
    alphas.append(curr_alpha)
    for observation in emission_sequence[1::]:
        curr_alpha = update_alpha(curr_alpha, transition_matrix, emission_matrix, observation)
        alphas.append(curr_alpha)
    return alphas


def update_beta(beta, transition_matrix, emission_matrix, observation):
    betas = []
    for i in range(len(transition_matrix)):
        beta_i = []
        for j in range(len(transition_matrix)):
            beta_i.append(beta[j] * emission_matrix[j][observation] * transition_matrix[i][j])
        betas.append(marginalize(beta_i))
    return betas


def run_me_my_betas(transition_matrix, emission_matrix, initial_state_distribution, emission_sequence):
    betas = []
    curr_beta = [1] * len(initial_state_distribution[0])
    betas.append(curr_beta)
    for observation in emission_sequence[:0:-1]:
        curr_beta = update_beta(curr_beta, transition_matrix, emission_matrix, observation)
        betas.append(curr_beta)
    return list(reversed(betas))


def compute_di_gamma(alpha, beta, transition_matrix, emission_matrix, observation, penultimate_alpha):
    denominator = marginalize(penultimate_alpha)
    gamma_i = []
    for i in range(len(transition_matrix)):
        gamma_j = []
        for j in range(len(transition_matrix)):
            val = alpha[i] * transition_matrix[i][j] * emission_matrix[j][observation] * beta[j] / denominator
            gamma_j.append(val)
        gamma_i.append(gamma_j)
    return gamma_i


def compute_gamma(di_gamma):
    return [marginalize(element) for element in di_gamma]


main()
