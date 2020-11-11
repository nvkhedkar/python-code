
class Heap:
    def __init__(self, m=-1):
        self.values = list()
        self.max = m
        self.size = 0

    @staticmethod
    def heapify(arr):
        return

    def insert(self, value):
        if 0 < self.max == self.values.__len__():
            return
        self.values.append(value)
        self.size = len(self.values)
        index = self.size - 1
        while index > 0 and value > self.parent_value(index):
            self.swap(index, self.parent_index(index))
            index = self.parent_index(index)

    def parent_value(self, index):
        return self.values[self.parent_index(index)]

    def parent_index(self, index):
        return int((index - 1) / 2)

    def swap(self, idx1, idx2):
        temp = self.values[idx1]
        self.values[idx1] = self.values[idx2]
        self.values[idx2] = temp

    def remove(self):
        removed = self.values[0]
        self.values[0] = self.values.pop()
        index = 0
        while index < len(self.values) and not self.is_valid_parent(index):
            index = self.bubble_down(index)
        return removed

    def left_child_index(self, index):
        return index * 2 + 1

    def right_child_index(self, index):
        return index * 2 + 2

    def left_child(self, index):
        return self.values[self.left_child_index(index)]

    def right_child(self, index):
        return self.values[self.right_child_index(index)]

    def is_valid_parent(self, index):
        if not self.has_left_child(index):
            return True
        is_valid = self.values[index] >= self.left_child(index)
        if self.has_right_child(index):
            is_valid = is_valid and self.values[index] >= self.right_child(index)
        return is_valid

    def has_right_child(self, index):
        return self.right_child_index(index) < len(self.values)

    def has_left_child(self, index):
        return self.left_child_index(index) < len(self.values)

    def bubble_down(self, index):
        if not self.has_left_child(index):
            return index
        swap_index = self.left_child_index(index)
        if self.has_right_child(index):
            if self.right_child(index) > self.left_child(index):
                swap_index = self.right_child_index(index)
        self.swap(index, swap_index)
        return swap_index

