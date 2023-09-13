# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt
import numpy as np


def lcm(numbers):
    lcm = numbers[0]
    for num in numbers[1:]:
        lcm = int(num * lcm / math.gcd(num, lcm))
    return lcm


def decompose_number(n):
    dp = [[[] for i in range(n + 1)] for j in range(n + 1)]
    for i in range(n + 1):
        dp[i][i] = [i]
    for i in range(1, n + 1):
        for j in range(i - 1, 0, -1):
            dp[i][j] = [[j, k] for k in dp[i-j][j]] + dp[i][j+1]
    
    return dp[n][1]


def flat_list(lists):
    if isinstance(lists, list):
        res = []
        for _list in lists:
            if isinstance(_list, list):
                res.extend(flat_list(_list))
            else:
                res.append(_list)
        
        return res
    else:
        return [lists]
    

def max_order_and_docomposed_list(n, docomposed_number_lists):
    max_order = lcm(docomposed_number_lists[0])
    max_docomposed_list = [docomposed_number_lists[0]]
    for number_list in docomposed_number_lists[1:]:
        order = lcm(number_list)
        if order > max_order:
            max_order = order
            max_docomposed_list = number_list
    
    return max_order, max_docomposed_list


def combination(n, number_list):
    res = 1
    for number in number_list:
        res *= np.math.factorial(n) // (np.math.factorial(number) * np.math.factorial(n - number))
        n -= number
    return res


def plot_order_probability(n, docomposed_number_lists):
    max_order, _ = max_order_and_docomposed_list(n, docomposed_number_lists)
    
    order_list = sorted([lcm(number_list) for number_list in docomposed_number_lists])
    order_list_length = len(order_list)
    pK = []
    index = 0
    for K in np.arange(max_order + 1):
        for i, order in enumerate(order_list[index:]):
            if order >= K:
                index += i
                pK.append(index / order_list_length)
                break
        
    plt.plot(np.arange(max_order + 1), pK)
    plt.xlabel('K')
    plt.ylabel('p(K)')
    plt.title(f'Maximum order: {max_order}')
    plt.show()
    
    
def logistic_map_shuffle(n, x0, mu=np.float64(3.8)):
    x = np.zeros(n, np.float64)
    x[0] = x0
    for i in range(1, n):
        x[i] = mu * x[i-1] * (1 - x[i-1])
    return np.argsort(x)


def count_inversions(sequence):
    count = 0
    for i in range(len(sequence)):
        for j in range(i + 1, len(sequence)):
            if sequence[i] > sequence[j]:
                count += 1
    return count


def plot_inversion(n, mu=np.float64(3.8)):
    x_list = np.linspace(0, 1, 100000, np.float64)
    y_list = []
    for x in x_list:
        shuffled_sequence = logistic_map_shuffle(n, x)
        inversion_num = count_inversions(shuffled_sequence)
        y_list.append(inversion_num)
    plt.plot(x_list, y_list)
    plt.xlabel('x0')
    plt.ylabel('the number of inversions')
    plt.title('logistic shuffle')
    plt.show()
    
    

def main():
    N = 30
    print('Decomposing...')
    docomposed_number_lists = [flat_list(number_list) for number_list in decompose_number(N)]
    print('Finish!')
    
    max_order, max_docomposed_list = max_order_and_docomposed_list(N, docomposed_number_lists)
    print(f'n = {N}, {max_order}, {max_docomposed_list}')
    
    plot_order_probability(N, docomposed_number_lists)
    
    shuffled_sequence = logistic_map_shuffle(N, x0=np.float64(0.5))
    inversion_num = count_inversions(shuffled_sequence)
    print(f'the number of inversions: {inversion_num}')
    
    plot_inversion(N)
    

if __name__ == '__main__':
    main()
