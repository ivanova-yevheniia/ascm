import numpy as np


'''Least squares'''
def least_squares(A, b):
    x, residuals, rank, singular_values = np.linalg.lstsq(A, b, rcond=None)
    return x

'''PINV'''
def pinv(A, b):
    A_plus = np.linalg.pinv(A)
    x = np.dot(A_plus, b)
    return x

'''QR - decomposition'''
def qr(A, b):
    Q, R = np.linalg.qr(A)
    y = np.dot(Q.T, b)
    x = np.linalg.solve(R, y)
    return x