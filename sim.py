from sklearn.metrics.pairwise import cosine_similarity
from operator import itemgetter

import numpy as np


def find_no_rate(matrix):

    V, D = matrix.shape

    no_rate_list = []
    for i in range(V):
        for j in range(D):
            if(matrix[i][j] == 0):
                no_rate_list.append([i, j])

    return no_rate_list


def sort_by_cosine_sim(array, id):

    sim_list = []
    for i in range(array.shape[0]):
        if(i != id):
            k, v = i, cosine_similarity([array[id]], [array[i]])[0][0]
            sim_list.append((k,v))
        else:
            pass
    sorted_list = sorted(sim_list, key=itemgetter(1), reverse=True)
    return sorted_list


def recommender(original_R, embedded_R):

    V, D = original_R.shape

    no_rate_list = find_no_rate(original_R)

    predict_rate_list = []
    for row, column in no_rate_list:
        predict_rate = round(embedded_R[row][column], 2)
        if predict_rate >= 5:
            predict_rate = 5
        elif predict_rate <= 0:
            predict_rate = 0
        predict_rate_list.append([row, column, predict_rate])

    user_predict_dict = {}
    for user in range(V):
        user_predict_list = []
        for rate in predict_rate_list:
            if(user == rate[0]):
                user_predict_list.append(rate)
        user_predict_list = sorted(user_predict_list, key=lambda t:t[2], reverse=True)
        user_predict_dict[user] = user_predict_list

    return user_predict_dict


R = np.array([
    [4, 0, 2, 1, 3, 0],
    [0, 2, 3, 1, 0, 2],
    [4, 0, 2, 1, 3, 4],
    [4, 1, 2, 0, 4, 2],
    [2, 2, 5, 0, 0, 0],
    [2, 2, 4, 4, 4, 0],
    [0, 0, 0, 1, 3, 5],
    [2, 3, 0, 2, 5, 0],
    [0, 4, 2, 1, 0, 2],
    [0, 0, 0, 0, 4, 0],
])
