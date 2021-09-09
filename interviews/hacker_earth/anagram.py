import string
import math

alpha_dict = {k:i for i, k in enumerate(string.ascii_lowercase)}


def find_ana(words):
    final_dict = {}
    ordered = []
    for word in words:
        unique_chars = dict()
        for a in word:
            unique_chars[a] = alpha_dict[a]
        special_power = 0
        for k, v in unique_chars.items():
            special_power += math.pow(2, v)
        if not final_dict or special_power not in final_dict.keys():
            final_dict[special_power] = []
        final_dict[special_power].append(word)

    for k in sorted(final_dict):
        print(" ".join(final_dict[k]))
    return


words = ["eah", "hea", "hac", "ahe",  "cah", "bah"]
import heapq
ll = []
for w in words:
    heapq.heappush(ll, w)
print(ll)
# find_ana(words)
# T = input()
# for i in T:
#     N = input()
#     words = []
#     for j in range(N):
#         words.append(input())
#     find_ana(words)




