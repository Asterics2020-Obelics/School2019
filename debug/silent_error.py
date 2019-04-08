"""Example of a "silent error" we want to debug.
"""

def load_data():
    # Pretend that here we have some complex data
    # and it's not possible from looking at the code
    # to see that there's bad data
    return {'a': 2, 'b': '3'}

def compute_result(data):
    # Pretend that here we have some complex computation,
    # that is hard to understand from looking at the code.
    val = 2 * data['a']
    val2 = val * data['b']
    return val2

def main():
    data = load_data()
    result = compute_result(data)

    # Correct result should be 12, but we get 3333
    print(result)

main()
