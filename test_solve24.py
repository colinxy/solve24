import sys
from solve24 import solve24, postfix2infix
from random import randint


def test():
    for _ in range(10):
        nums = [randint(1, 20) for i in range(4)]
        target = randint(1, 100)
        for sol in solve24(nums, target):
            expr = postfix2infix(sol)
            print(expr, target)
            if not eval(expr) == target:
                print("****** INCORRECT ******")
                print(nums)
                print(target)
                sys.exit()

    print("****** TEST PASSED ******")


if __name__ == '__main__':
    test()
