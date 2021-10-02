print(100, end=" ")
print(0)

lst = [2, 4, 1, 3]
# new = lst.sort()
# print(new)

print(lst*2)

# 3
class HE:
    h1 = 0
    def __init__(self, h=0):
        self.h2 = h
        HE.h1 += h

he1 = HE()
he2 = HE(1)
he3 = HE(2)

print(he3.h1)

# 4
d1 = {}
a, b, c = 164, 936, 728
d1[a, b, c] = a + b - c
print(d1)

d2 = {}
d, e, f = 482, 925, 859
d2[d, e, f] = e, f, d
print(d2)

print([1, 2, 3][2::-1])
print([1, 2, 3][::-1])