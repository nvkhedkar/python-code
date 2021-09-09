
def swap_easy(a, b):
    return b, a


def swap(aa, bb):
    z = aa
    aa = bb
    bb = z
    print(f"inside: {aa}, {bb}")


def swap_a(**kwargs):
    z = kwargs['aa']
    kwargs['aa'] = kwargs['bb']
    kwargs['bb'] = z
    print(f"inside: {kwargs['aa']}, {kwargs['bb']}")


def swap_lst(lst):
    z = lst[0]
    lst[0] = lst[1]
    lst[1] = z
    print(f"inside: {lst[0]}, {lst[1]}")


def swap_cls(cobj):
    z = cobj.a
    cobj.a = cobj.b
    cobj.b = z
    print(f"inside: {cobj.a}, {cobj.b}")


class Calc:
    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b


def run_swap():
    a = 1
    b = 2
    # swap_a(aa=a, bb=b)
    # lst = [a, b]
    # swap_lst(lst)
    # tpl = (a, b)
    # swap_lst(tpl)
    calc = Calc(a, b)
    swap_cls(calc)
    print(calc.a, calc.b)
    # print(a, b, lst)


def get_recurring(input):
    seen = set()
    recurring = set()
    for char in input:
        if char in seen:
            recurring.add(char)
        seen.add(char)

    return recurring


print(set('nikhil_is_cool'))
