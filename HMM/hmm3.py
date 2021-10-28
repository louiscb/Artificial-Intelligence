from hmm_lib import *
from math import log


def main():
    transition_matrix, emission_matrix, initial_state_distribution, emission_sequence = read_data()
    transition_matrix, emission_matrix = baum_welch(transition_matrix, emission_matrix, initial_state_distribution,
                                                    emission_sequence)
    print_ans(transition_matrix)
    print("")
    print_ans(emission_matrix)


def baum_welch(transition_matrix, emission_matrix, initial_state_distribution, emission_sequence):
    old_log_prob = float('-inf')
    log_prob = 0
    iter = 0
    max_iter = 150
    while log_prob > old_log_prob and iter < max_iter:
        if log_prob != 0:
            old_log_prob = log_prob
        alphas, scale_factors = run_me_my_alphas(transition_matrix, emission_matrix, initial_state_distribution,
                                                 emission_sequence)
        betas = run_me_my_betas(transition_matrix, emission_matrix, initial_state_distribution, emission_sequence[::-1],
                                scale_factors[::-1])
        di_gammas, gammas = run_me_my_gammas(alphas, betas, transition_matrix, emission_matrix, emission_sequence)
        new_transition_matrix, new_emission_matrix = estimate_transition_and_emission_matrix(di_gammas, gammas,
                                                                                             len(emission_matrix[0]),
                                                                                             emission_sequence)
        transition_matrix = new_transition_matrix
        emission_matrix = new_emission_matrix
        initial_state_distribution = [gammas[0]]
        log_prob = compute_log_prob(scale_factors)
        iter += 1

    return transition_matrix, emission_matrix


def compute_log_prob(scale_factors):
    log_prob = 0
    for factor in scale_factors:
        log_prob += log(factor)
    log_prob *= -1
    return log_prob


def estimate_transition_and_emission_matrix(di_gammas, gammas, no_possible_observations, emission_sequence):
    N = len(di_gammas[0])

    new_transition_matrix = []
    denominators = [0] * N
    numerators = []
    for i in range(N):
        numerators.append([0] * N)

    for t in range(len(emission_sequence) - 1):
        for i in range(N):
            denominators[i] += gammas[t][i]
            for j in range(N):
                numerators[i][j] += di_gammas[t][i][j]

    for i in range(N):
        new_transition_matrix.append([numer / denominators[i] for numer in numerators[i]])

    new_emission_matrix = []
    denom = [0] * N
    numer = []
    for i in range(N):
        numer.append([0] * no_possible_observations)
    for t in range(len(emission_sequence)):
        for i in range(N):
            denom[i] += gammas[t][i]
            for j in range(no_possible_observations):
                if j == emission_sequence[t]:
                    numer[i][j] += gammas[t][i]
    for i in range(N):
        new_emission_matrix.append([num / denom[i] for num in numer[i]])
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
    gammas.append(alphas[-1])
    return di_gammas, gammas


def run_me_my_alphas(transition_matrix, emission_matrix, initial_state_distribution, emission_sequence):
    alphas = []
    scale_factors = []
    curr_alpha = None
    for t in range(len(emission_sequence)):
        if t == 0:
            curr_alpha = initialize_alpha(initial_state_distribution, emission_matrix, emission_sequence[0])
        else:
            curr_alpha = update_alpha(curr_alpha, transition_matrix, emission_matrix, emission_sequence[t])
        scale_factor = marginalize(curr_alpha)
        scale_factor = 1 / scale_factor
        curr_alpha = [alpha_i * scale_factor for alpha_i in curr_alpha]
        alphas.append(curr_alpha)
        scale_factors.append(scale_factor)
    return alphas, scale_factors


def update_beta(beta, transition_matrix, emission_matrix, observation):
    betas = []
    for i in range(len(transition_matrix)):
        beta_i = 0
        for j in range(len(transition_matrix)):
            beta_i += (beta[j] * emission_matrix[j][observation] * transition_matrix[i][j])
        betas.append(beta_i)
    return betas


def run_me_my_betas(transition_matrix, emission_matrix, initial_state_distribution, emission_sequence, scale_factors):
    betas = []
    curr_beta = [scale_factors[0]] * len(initial_state_distribution[0])
    for t in range(len(emission_sequence)):
        if t == 0:
            betas.append(curr_beta)
        else:
            curr_beta = update_beta(curr_beta, transition_matrix, emission_matrix, emission_sequence[t - 1])
            curr_beta = [beta_i * scale_factors[t] for beta_i in curr_beta]
            betas.append(curr_beta)
    return betas[::-1]


def compute_di_gamma(alpha, beta, transition_matrix, emission_matrix, observation, last_alpha):
    denominator = marginalize(last_alpha)
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
