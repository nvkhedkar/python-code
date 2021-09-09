c = 'str1 \u2602 \u0041'
u = u'str1 \u2602 \u0041'
b = b'nikhil'


# def py2_print():
#     print type(c), c
#     print type(u), u
#     print type(b), b, b[3]


def py3_print():
    print(type(c), c)
    print(type(u), u)
    print(type(b), b, b[3])


py3_print()


[print(x) for x in range(5)]


def print(*args, **kwargs):
    # Add MY_DBG prefix to all prints
    __builtins__.print("MY_DBG", *args, **kwargs)


print(type(c), c)
print(type(u), u)
print(type(b), b, b[3])


