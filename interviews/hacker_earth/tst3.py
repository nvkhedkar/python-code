import pandas as pd
import sys, requests

x = requests.get(url='https://1drv.ms/u/s!AtAAGckP_LuV3W0_8WyT-juYdIbd?e=CUQR85', verify=False).content
pd.read_csv(x.decode('utf-8'))
# pd.read_csv('https://1drv.ms/u/s!AtAAGckP_LuV3Wyf08BipNyOJAnm?e=CZE1qS')
# pd.read_csv('https://query.data.world/s/HqjNNadqEnwSq1qnoV_JqyRJkc7o6O')
print(pd.shape)
sys.exit()

word = "I love Python programming"
print(word[7:13])
print(word[-18:-12])

names = 'names'
print(names[:3])
print(names[0:3])
print(names[-1])

mytup = ('a', [1, 2])
print(mytup, type(mytup))

d = dict(a=1, b=2)
print(d)

l1 = set([1, 2, 3, 4, 5, 6])
l2 = set([2, 3, 4, 5, 6, 7, 8, 9])
print(l1.difference(l2))
print(l1.symmetric_difference(l2))


d = {0, 1, 2}
for x in d:
    print(d.add(x))

for i in range(1,6):
    if (i % 3 == 0):
        # print(str(i) + " is Divisible by 3")
        continue

    # print(str(i) + " is not divisible by 3")

min = (lambda x, y: x if x < y else y)
print(min(101*99, 102*98))

print( ((500//7) % 5) ** 3)

from functools import reduce
C = set([2, 5, 9, 12, 13, 15, 16, 17, 18, 19])
F = set([2, 4, 5, 6, 7, 9, 13, 16])
H = set([1, 2, 5, 9, 10, 11, 12, 13, 15])
S = set([x + 1 for x in range(20)])
slist = lambda x: sorted(list(x))
# print(sorted(list(C & F & H)))
# print(sorted(list(C & F - H)))
# print( slist((C&F | C&H | F&H) - (C & F & H)))
# print(slist(S - (C | F | H)))

import numpy as np
arr = np.array( [1, 2, 3, 5, 4, 6, 7, 8, 5, 3, 2])
print(arr[0::2])

a1 = np.array([[1, 2],
 [5, 6]])

a2= np.array([[3, 4],
 [7, 8]])
print(a1)
a4 = np.hstack((a1, a2))
a3 = np.array([[9, 10, 11, 12]])
print(np.vstack((a4, a3)))
