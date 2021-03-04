import random


def swap(lst, i, j):
    tmp = lst[i]
    lst[i] = lst[j]
    lst[j] = tmp


def my_sort(lst):
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] > lst[j]:
                swap(lst, i, j)
    # return lst


def bubble_sort(lst):
    for i in range(len(lst)):
        sortd = False
        for j in range(1, len(lst) - i):
            if lst[j] < lst[j - 1]:
                sortd = True
                swap(lst, j, j - 1)
            print(i, j, lst)

        if not sortd:
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


# arr = [random.randint(1, 100) for x in range(22)]
arr = [29, 31, 98, 60, 21, 19, 10, 76, 19, 10, 35, 96, 85, 49, 70, 87, 100, 77, 94, 40, 46, 40]
# arr = [5, 8, 1, 4, 7, 2, 6]
print(arr)
quick_sort(lst=arr)
print(arr)
