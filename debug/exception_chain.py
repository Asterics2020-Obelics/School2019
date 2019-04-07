"""Chained exception example"""
a, b = 1, 0
try:
    a / b
except ZeroDivisionError:
    print('Bad data:', a, c)
