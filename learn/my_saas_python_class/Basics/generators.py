
def simple_generator():
    for i in range(5):
        yield i


for j in simple_generator():
    print(f"For loop: {j}")

sg = simple_generator()
print(f"Next value: {next(sg)}")
print(f"Next value: {next(sg)}")
print(f"Next value: {next(sg)}")

gen_comp = (x for x in range(4))
list_comp = [x for x in range(4)]


for j in gen_comp:
    print(j)


my_gen = simple_generator()
print(type(my_gen), next(my_gen))
print(next(my_gen))


print(f"{type(gen_comp)}, {type(list_comp)}")
