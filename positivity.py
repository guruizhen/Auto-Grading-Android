import numpy as np


def weak_positivity_validation(num_t, num_m):
    """
    :param num_t: the number of test cases
    :param num_m: the number of methods
    :return: weak positivity table
    """

    method_coverage_table = np.random.randint(0, 2, (num_m, num_t))
    weak_positivity_table = np.zeros((num_m, num_m))

    for i in range(num_m):
        for j in range(i + 1, num_m):
            flag = False
            p11 = False
            p10 = False
            p01 = False
            p00 = False
            for k in range(num_t):
                if method_coverage_table[i, k] == 1 and method_coverage_table[j, k] == 1:
                    p11 = True
                if method_coverage_table[i, k] == 1 and method_coverage_table[j, k] == 0:
                    p10 = True
                if method_coverage_table[i, k] == 0 and method_coverage_table[j, k] == 1:
                    p01 = True
                if method_coverage_table[i, k] == 0 and method_coverage_table[j, k] == 0:
                    p00 = True
                if p11 and p10 and p01 and p00:
                    flag = True
                    break
            weak_positivity_table[i, j] = flag
            weak_positivity_table[j, i] = flag
    return weak_positivity_table


if __name__ == '__main__':
    w = weak_positivity_validation(num_t=5, num_m=5)
    print(w)
