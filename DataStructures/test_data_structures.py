import os, sys
CURR_FILE = os.path.basename(__file__)
CURR_DIR = os.path.dirname(__file__)
from DataStructures.Heap import Heap


def test_heap():
    hp = Heap(20)
    hp.insert(10)
    hp.insert(5)
    hp.insert(17)
    hp.insert(4)
    hp.insert(22)
    print(hp.values)
    hp.remove()
    return


def main(argv):
    test_heap()
    return


if __name__ == "__main__":
   main(sys.argv[1:])
