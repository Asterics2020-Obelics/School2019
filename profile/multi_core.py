"""Example of a function that might use multiple cores"""
import numpy as np

size = 10000
print('a')
a = np.random.random_sample((size, size))
b = np.random.random_sample((size, size))
print('b')
n = np.dot(a,b)
print('c')
