
def count_to(num, arr):
    iterator = zip(range(num), arr)
    for i, elem in iterator:
        yield elem


test_arr = [f'elem{i}' for i in range(10)]
for i in count_to(3, test_arr):
    print(i)

