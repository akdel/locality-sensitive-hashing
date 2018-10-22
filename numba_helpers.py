import numpy as np
import numba as nb

@nb.njit
def create_random_vectors(k, d):
    return np.random.randn(k, d)


@nb.njit
def check_pass(v1, v2):
    dot = np.dot(v1, v2)
    if dot < 0:
        return 0
    else:
        return 1


@nb.njit
def vector_score(observation, table):
    r = np.zeros(table.shape[0])
    for i in range(table.shape[0]):
        r[i] = check_pass(observation, table[i])
    return r


@nb.njit(parallel=True)
def vector_scores(table, observations, res):
    for i in nb.prange(observations.shape[0]):
        for j in range(table.shape[0]):
            res[i, j] = check_pass(observations[i], table[j])
    return res
