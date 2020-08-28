import os


def two_num_sum_1(num_array, sum):
    num_dict = {}
    for num in num_array:
        num_dict[str(num)] = sum - num
    print(num_dict)
    keys = num_dict.keys()
    fin_arr = []
    for key, value in num_dict.items():
        if str(value) in keys:
            fin_arr.append([value, sum - value])
    print(fin_arr)
    return


def two_num_sum(num_array, sum):
    num_array = sorted(num_array)
    left, right = 0, len(num_array)-1
    while(True):
        if left >= right:
            break
        if num_array[left] + num_array[right] < sum:
            left += 1
        elif num_array[left] + num_array[right] > sum:
            right -= 1
        else:
            break
    print([num_array[left], num_array[right]])


def four_num_sum_easy(nums, sum):
    from itertools import combinations
    import math
    nums = sorted(nums)
    combos = combinations(nums, 4)
    print(nums)
    i = 0
    for c in combos:
        print(sorted(c))
    print(i)

def four_num_sum(nums, sum):
    def addn(ids):
        a = 0
        for id in ids: a += nums[id]
        return a

    nums = sorted(nums)
    n = len(nums)
    l1, l2, r1, r2 = 0, 1, n-1, n-2
    combos = []
    while (True):
        if (l1 >= r1): break
        if (addn([l1, l2, r1, r2]) < sum):
            l2 += 1
            if (addn([l1, l2, r1, r2]) < sum):
                l1 += 1
        elif(addn([l1, l2, r1, r2]) > sum):
            r2 -= 1

# two_num_sum([3, 5, -4, 8, 11, 1, -1, 6], 8)
# four_num_sum([7, 6, 4, 1, -1, 2], 16)
import numpy as np

na = np.ones((1, 5))
x1 = np.random.randint(10, size=(1, 4))
x2 = np.random.randint(10, size=(3, 4))
r, c = x2.shape
print(x1, x1.shape)
print(na, na.shape)
for cr in range(r):
    print(x2[cr:cr+1, :])

