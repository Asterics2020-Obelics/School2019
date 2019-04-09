"""Chained exception example"""
a, b = 1, 0
try:
    result = a / b
except ZeroDivisionError:
    result = c

print(f"Result: {result}")
