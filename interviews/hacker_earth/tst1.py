def add(a,b):
    assert(a > b)
    assert(b > a)
    print(a/b)

import random
arr = [-3, 2, 3, -4, 3, 1]# [random.randint(-100, 100) for i in range(random.randint(5, 10))]
ln = len(arr)
best_sum, best_i = 0, 0
for i in range(ln):
    cn = i
    addition, j = arr[i], 2
    last_cn = 0
    while cn < ln:
        last_cn = cn
        cn += j
        j += 1
    addition = sum(arr[i:last_cn+1])
    if i == 0:
        best_sum = addition
    elif addition > best_sum:
        best_sum = addition
        best_i = i
    print(i, last_cn, arr[i:last_cn+1], addition)
print(best_sum, best_i)