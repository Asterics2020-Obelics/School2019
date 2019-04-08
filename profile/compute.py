def generate_data(size):
    return [i ** 2 for i in range(size)]

def compute_result(data):
    total = 0
    for _ in range(10):
        total += sum(data)
    return total

def main():
    data = generate_data(size=100_000)
    result = compute_result(data)

    data = generate_data(size=200_000)
    result = compute_result(data)

if __name__ == '__main__':
    main()
