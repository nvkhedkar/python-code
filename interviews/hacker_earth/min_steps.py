import heapq


def shift_pos(arr, num, from_pos, to_pos):
    # print(f'shift {num} from {from_pos} to {to_pos}')
    for i in range(from_pos, to_pos, -1):
        arr[i] = arr[i-1]
    arr[to_pos] = num


def get_pos(num, curr_pos, arr):
    for i in range(curr_pos, len(arr)):
        if arr[i] == num:
            return i


def min_steps_inc(sorted_arr, inarr):
    # sorted_arr = sorted(arr)
    print(inarr)
    sorted_pos = {x: i for i, x in enumerate(sorted_arr)}
    print(sorted_pos)
    swaps = 0
    for i, a in enumerate(inarr):
        if not i == sorted_pos[a]:
            print(f'before: {inarr}')
            shift_pos(inarr, sorted_arr[i], get_pos(sorted_arr[i], i, inarr), i)
            print(f'after: {inarr}\n')
            swaps += 1

    return swaps


def min_steps_dec(sorted_arr, inarr):
    # sorted_arr = sorted(arr)
    sorted_pos = {x: i for i, x in enumerate(sorted_arr)}
    print(sorted_pos, inarr)
    swaps = 0
    for i in range(len(inarr), 0, -1):
        a = inarr[i]
        if not i == sorted_pos[a]:
            print(f'\nbefore: {inarr}')
            shift_pos(inarr, sorted_arr[i], get_pos(sorted_arr[i], i, inarr), i)
            print(f'after: {inarr}')
            swaps += 1

    return swaps


def find_min(carr):
    rcarr = [x for x in carr]
    inc = min_steps_inc(sorted(carr), carr)
    rcarr.reverse()
    dec = min_steps_inc(sorted(rcarr), rcarr)
    print(inc, dec)
    return inc if inc < dec else dec
# dec = min_steps(sorted(arr))


garr = [1, 3, 4, 2, 6, 5]
find_min(garr)