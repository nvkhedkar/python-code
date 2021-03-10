import random


def swap_old(lst, i, j):
    tmp = lst[i]
    lst[i] = lst[j]
    lst[j] = tmp


def swap(lst, i, j):
    lst[i], lst[j] = lst[j], lst[i]


def my_sort(lst):
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] > lst[j]:
                swap(lst, i, j)
    # return lst


def bubble_sort(lst):
    for i in range(len(lst)):
        is_sorted = False
        for j in range(1, len(lst) - i):
            if lst[j] < lst[j - 1]:
                is_sorted = True
                swap(lst, j, j - 1)
            print(i, j, lst)

        if not is_sorted:
            break


def selection_sort(lst):
    for i in range(len(lst)):
        minidx = i
        for j in range(i + 1, len(lst)):
            if lst[j] < lst[minidx]:
                minidx = j
        swap(lst, i, minidx)
    return


def quick_sort(lst):
    quick_sort_low(lst, 0, len(lst))
    return


def quick_sort_low(lst, st, ed):
    if st >= ed:
        return
    pivot = lst[ed - 1]
    boundary = st - 1
    for i in range(st, ed):
        '''
        if lst[i] <= pivot:
        <= ensures swapping of pivot 
        '''
        if lst[i] < pivot or i == ed - 1:
            boundary += 1
            swap(lst, i, boundary)
    print('partition:', st, ed, boundary, lst[st:ed])
    quick_sort_low(lst, st, boundary)
    quick_sort_low(lst, boundary + 1, ed)


def merge_sort_inplace(lst):
    merge_sort_inplace_low(lst, 0, len(lst))
    return


def merge_sort_inplace_low(lst, st, ed):
    if ed - st < 2:
        return
    middle = int((ed - st) / 2)
    print(f'st: {st} m: {middle} ed: {ed} lst: {lst[st:ed]}')
    merge_sort_inplace_low(lst, st, middle)
    merge_sort_inplace_low(lst, middle, ed)
    return


def merge_sort(lst):
    if len(lst) < 2:
        return
    middle = int(len(lst) / 2)
    left, right = lst[0:middle], lst[middle:]
    print(f'right: {right} left: {left}')
    merge_sort(right)
    merge_sort(left)

    merge_lists(right, left, lst)
    print(f'lst: {lst}')
    return


def merge_lists(right, left, lst):
    i, j, w = 0, 0, 0
    while i < len(right) and j < len(left):
        if right[i] <= left[j]:
            lst[w] = right[i]
            i += 1
        else:
            lst[w] = left[j]
            j += 1
        w += 1

    for lv in left[j:]:
        lst[w] = lv
        w += 1

    for rv in right[i:]:
        lst[w] = rv
        w += 1


# arr = [random.randint(1, 100) for x in range(22)]
# arr = [29, 31, 98, 60, 21, 19, 10, 76, 19, 10, 35, 96, 85, 49, 70, 87, 100, 77, 94, 40, 46, 40, 41]
arr = [5, 8, 1, 4, 7, 2, 6]
print(arr)
merge_sort_inplace(lst=arr)
print(arr)
