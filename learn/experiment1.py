
values = [x + 1 for x in range(10)]
print(values)


def add(x, y):
    return x + y


print(values[2:] + [66])

# while len(values) > 1:
#     print(f'Values b: {values}')
#     values = values[2:] + [add(values[0], values[1])]
#     print(f'values: {values}')