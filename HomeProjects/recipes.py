import numpy as np


def reshape_array():
    a = np.array([i for i in range(12)])
    print(a.reshape(4, 3))
    print(a.reshape(4, 3, order='F'))
    print(a.reshape(4, 3, order='A'))


def sorting_array():
    a = np.array([np.random.randint(0, 100) for i in range(9)])
    a = a.reshape(3, 3)
    print("Unsorted\n", a)
    print("sorted column 2\n", a[a[:, 2].argsort()])
    # following does not seem to work ok
    print("sorted row 2\n", a[a[2, :].argsort()])


def split_array_by_columns():
    a = np.array([np.random.randint(0, 40) for i in range(20)])
    labels = np.array([np.random.randint(0, 2) for i in range(5)])
    a = a.reshape(5, 4)
    labels = labels.reshape(5, 1)
    print(labels)
    x = np.hstack((a, labels))
    print(x, x.shape)
    unique_labels = np.unique(x[:, -1])
    for k in unique_labels:
        sub_array = x[x[:, -1] == k]
        label_removed = np.delete(sub_array, -1, axis=1)
        print(label_removed, label_removed.shape)


split_array_by_columns()
