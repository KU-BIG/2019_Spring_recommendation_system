import csv
import numpy as np


def csv_reader(csv_name, row_size):

    f = open(csv_name, 'r', encoding='utf-8')
    rd = csv.reader(f)
    if(row_size <= 0):
        rd = list(rd)
    else:
        rd = list(rd)[:row_size]

    data_set = []
    for i in rd:
        try:
            i[0] = int(i[0])
            i[1] = int(i[1])
            i[2] = int(i[2])
        except:
            pass
        data_set.append(i)

    return data_set #[[userId, movieID, rating, timestamps], ...]


def user_movie_matrix_generator(data_set):

    user_list = []
    movie_list = []

    for data in data_set:
        if(type(data[0]) != type("")):
            user_list.append(data[0])
            movie_list.append(data[1])
    user_list = list(set(user_list))
    movie_list = list(set(movie_list))

    user_max_id = max(user_list)
    movie_max_id = max(movie_list)

    user_movie_matrix = np.zeros((user_max_id, movie_max_id))

    for data in data_set:
        if(type(data[0]) != type("")):
            for row in range(user_max_id):
                for column in range(movie_max_id):
                    if(row == data[0]-1 and column == data[1]-1):
                        user_movie_matrix[row][column] = data[2]

    return user_movie_matrix #shape : user X movies