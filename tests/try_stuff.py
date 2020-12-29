import argparse, re


def check_validity_trs_file_path(arg_value, pat='[\w\d\:\-\.\\\/]{1,1024}'):
    recomp = re.compile(pat)
    if not recomp.match(arg_value) or not arg_value.endswith('.trs'):
        print('Invalid arg value')
        raise argparse.ArgumentError(f"Argument {arg_value} not in correct format")
    return arg_value


def check_disk_usage():
    import shutil
    total, used, free = shutil.disk_usage("c:/nvk")
    print(f"Total: {(total // (2 ** 30))} GiB {total}")
    print("Used: %d GiB" % (used // (2 ** 30)))
    print("Free: %d GiB" % (free // (2 ** 30)))


import random


def are_three_equal(iarr):
  if iarr[0] == iarr[1] == iarr[2] or iarr[1] == iarr[2] == iarr[3] \
          or iarr[2] == iarr[3] == iarr[0] or iarr[2] == iarr[3] == iarr[0]:
      return 1
  return 0


def are_two_equal(iarr):
    if ((iarr[0] == iarr[1])
        or (iarr[0] == iarr[2])
        or (iarr[0] == iarr[3])
        or (iarr[1] == iarr[2])
        or (iarr[1] == iarr[3])
        or (iarr[2] == iarr[3])
    ):
        return 1
    return 0


def are_two_equal_sz3(iarr):
    if ((iarr[0] == iarr[1])
            or (iarr[0] == iarr[2])
            or (iarr[1] == iarr[2])
    ):
        return 1
    return 0


all_nums = dict()
equals, all_eq, th_eq, two_eq = 0, 0, 0, 0
n1 = 9
n2 = 3
bign = 100000
for i in range(bign):
    arr = [random.randint(0, n1), random.randint(0, n1), random.randint(0, n1), random.randint(0, n1)]

    if arr[0] == arr[1] == arr[2] == arr[3]:
        arr2 = [random.randint(0, 3), random.randint(0, 3), random.randint(0, 3), random.randint(0, 3)]
        if arr2[0] == arr2[1] == arr2[2] == arr2[3]:
            all_eq += 1
        elif are_three_equal(arr2):
            th_eq += 1
        elif are_two_equal(arr2):
            two_eq += 1

    elif arr[0] == arr[1] == arr[2] or arr[1] == arr[2] == arr[3] \
            or arr[2] == arr[3] == arr[0] or arr[2] == arr[3] == arr[0]:
        arr2 = [random.randint(0, 2), random.randint(0, 2), random.randint(0, 2)]
        if arr2[0] == arr2[1] == arr2[2]:
            th_eq += 1
        elif are_two_equal_sz3(arr2):
            two_eq += 1

    elif ((arr[0] == arr[1])
            or (arr[0] == arr[2])
            or (arr[0] == arr[3])
            or (arr[1] == arr[2])
            or (arr[1] == arr[3])
            or (arr[2] == arr[3])
    ):
        arr2 = [random.randint(0, 1), random.randint(0, 1)]
        if arr2[0] == arr2[1]:
            two_eq += 1

    # if ((arr[0] == arr[1] and arr2[0] == arr2[1])
    #         or (arr[0] == arr[2] and arr2[0] == arr2[2])
    #         or (arr[0] == arr[3] and arr2[0] == arr2[3])
    #         or (arr[1] == arr[2] and arr2[1] == arr2[2])
    #         or (arr[1] == arr[3] and arr2[1] == arr2[3])
    #         or (arr[2] == arr[3] and arr2[2] == arr2[3])
    # ):
    #     # print(arr, arr2)
    #     equals += 1
# print(equals, two_eq/bign, th_eq/bign, all_eq/bign, 100*float(equals) / float(bign))
# print(two_eq / 2, )

print(bign, two_eq/bign, 100*th_eq/bign, all_eq, (two_eq + th_eq + all_eq)/bign)