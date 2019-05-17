#-*- coding: utf-8 -*-
import numpy as np
import argparse

from sim import sort_by_cosine_sim, recommender
from data import csv_reader, user_movie_matrix_generator


class MatrixFactorization():

    def __init__(self, matrix, lr, reg_param, epochs):

        self._matrix = matrix
        self._row, self._column = matrix.shape
        self._k = 5
        self._lr = lr
        self._reg_param = reg_param
        self._epochs = epochs


    def fit(self):

        # initialize latent features
        self._P = np.random.normal(size=(self._row, self._k))
        self._Q = np.random.normal(size=(self._column, self._k))

        # initialize biases
        self._b_P = np.zeros(self._row)
        self._b_Q = np.zeros(self._column)
        self._b = np.mean(self._matrix[np.where(self._matrix != 0)])

        #training
        for epoch in range(self._epochs):
            for i in range(self._row):
                for j in range(self._column):
                    if self._matrix[i, j] > 0:
                        self.gradient_descent(i, j, self._matrix[i, j])


    def gradient_descent(self, i, j, rating):

        # get error
        prediction = self.get_prediction(i, j)
        error = rating - prediction

        # get gradient
        dp = (error * self._Q[j, :]) - (self._reg_param * self._P[i, :])
        dq = (error * self._P[i, :]) - (self._reg_param * self._Q[j, :])

        # update biases
        self._b_P[i] += self._lr * (error - self._reg_param * self._b_P[i])
        self._b_Q[j] += self._lr * (error - self._reg_param * self._b_Q[j])

        # update latent feature
        self._P[i, :] += self._lr * dp
        self._Q[j, :] += self._lr * dq


    def get_prediction(self, i, j):

        return self._b + self._b_P[i] + self._b_Q[j] + self._P[i, :].dot(self._Q[j, :].T)


    def get_complete_matrix(self):

        return self._b + self._b_P[:, np.newaxis] + self._b_Q[np.newaxis:, ] + self._P.dot(self._Q.T)


    def print_results(self):

        try:
            print()
            embedded_matrix = self.get_complete_matrix()
            test = sort_by_cosine_sim(embedded_matrix, 0)

        except IndexError:
            print("NO ENOUGH DATA. INCREASE THE SIZE OF DATA.")

        else:
            print()

            #user to user similarity
            print("========find similar user========")
            for id in range(self._matrix.shape[0]):
                print('most similar user with user_id {id} is {sim_id}'.format(id=id, sim_id=sort_by_cosine_sim(embedded_matrix,id)[0][0]))

            # movie to movie similarity
            # print()
            # print("========find similar movie========")
            # matrix_transpose = np.transpose(self._matrix)
            # for id in range(matrix_transpose.shape[0]):
            #     print('most similar movie with movie_id {id} is {sim_id}'.format(id=id, sim_id=sort_by_cosine_sim(np.transpose(embedded_matrix),id)[0][0]))
            #

            print()
            print("========recommend movie========")
            user_predict_dict = recommender(self._matrix, embedded_matrix)

            for user in range(self._matrix.shape[0]):
                recommend_movie = user_predict_dict[user][0][1]
                predicted_rate = user_predict_dict[user][0][2]
                print("recommend movie_id {} to user_id {} with predicted rating {}".format(recommend_movie, user, predicted_rate))
        print()

if __name__ == "__main__":
    # rating matrix - User X Item : (7 X 5)

    print()
    print("CHECK THE DATA SET \n* THE FIRST COLUMN MUST BE USER_ID \n* THE SECOND COLUMN MUST BE MOVIE_ID \n* THE THIRD COLUMN MUST BE RATING")
    print()

    parser = argparse.ArgumentParser()
    parser.add_argument('data_name', metavar='data_name', type=str,
                        help='csv file name. eg. rates.csv')
    parser.add_argument('data_size', metavar='data_size', type=int,
                        help='number of rows of data to get. You can get full data with 0')

    try:
        args = parser.parse_args()
        data_name = args.data_name
        data_size = args.data_size

        data_set = csv_reader(data_name, data_size)
        matrix = user_movie_matrix_generator(data_set)
    except:
        print()
        print("fail to get data. continue with base data set".upper())
        base_matrix = np.array([
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

    # P, Q is (7 X k), (k X 5) matrix
    factorizer = MatrixFactorization(base_matrix, lr=0.01, reg_param=0.01, epochs=300)
    factorizer.fit()
    factorizer.print_results()
