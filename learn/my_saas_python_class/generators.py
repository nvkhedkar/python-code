
def simple_generator():
    for i in range(5):
        yield i


def run_simple_generator():
    for j in simple_generator():
        print(f"For loop: {j}")

    sg = simple_generator()
    print(f"Next value: {next(sg)}")
    print(f"Next value: {next(sg)}")
    print(f"Next value: {next(sg)}")

    my_gen = simple_generator()
    print(type(my_gen), next(my_gen))
    print(next(my_gen))


def generator_comprehension():
    gen_comp = (x for x in range(4))
    list_comp = [x for x in range(4)]

    for j in gen_comp:
        print(j)
    print(f"{type(gen_comp)}, {type(list_comp)}")
