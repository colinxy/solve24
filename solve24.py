#! /usr/bin/env python3

"""
24 GAME:
With 4 numbers, use addition, subtraction, multiplication and
division and parenthesis to achieve 24.

Note: this is an extended version of 24 solver, allowing more
than 4 numbers as input, and targets other than 24. Also,
operators other than addition, subtraction, multiplication and
division can be supported. To add a new operator, add the
function of the operator into global variable `set_of_operators',
and its representation into global variable `op_repr'.
The operator is assumed to be binary.

The program gives all possible solutions to each set of input
numbers. The program makes use of reverse polish (postfix)
notation to enumerate any combination of numbers and operations,
without the concern of parenthesis.

The program make use of brute force enumeration, and do not

The time complexity for the solution is O(N! * M^(N-1) * N^2)
where N is the number of inputs and M is the number of allowed
operations. Therefore, the execution time is going to increase
dramatically as number of inputs increases.


usage: solve24.py [-h] [-t TARGET] [-q]

Solve the 24 game

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        specify target (default 24)
  -q, --quick           turn on quick mode (find the first solution available)
  """

__author__ = 'yxy'


import sys
from time import time
import argparse
from itertools import product, permutations
import operator as op
from fractions import Fraction


set_of_operators = {op.add, op.sub, op.mul, op.truediv}
op_repr = {op.add: '+', op.sub: '-',
           op.mul: '*', op.truediv: '/'}
postfix_cache = {
    4: [['num', 'num', 'num', 'num',  'op',  'op',  'op'],
        ['num', 'num', 'num',  'op', 'num',  'op',  'op'],
        ['num', 'num', 'num',  'op',  'op', 'num',  'op'],
        ['num', 'num',  'op', 'num', 'num',  'op',  'op'],
        ['num', 'num',  'op', 'num',  'op', 'num',  'op']],
}


def solve24(nums, target=24):
    for num_patterns in permutations(nums):
        for op_patterns in product(set_of_operators,
                                   repeat=len(nums)-1):
            for comb_patterns in postfix_pattern(len(nums)):
                notation = postfix_notation(num_patterns,
                                            op_patterns,
                                            comb_patterns)
                if postfix_eval(notation) == target:
                    yield notation


def pretty_print(results, input_nums, quick):
    """
    results: Iterable
    """
    print()
    count = 0
    for result in results:
        count += 1
        print(postfix2infix(result))
        if quick:
            break

    if not quick:
        print(count, "solution(s) for", sorted(input_nums))


def postfix2infix(postfix):
    repr_stack = []
    for token in postfix:
        if isinstance(token, int):
            repr_stack.append(str(token))
        else:  # operator
            rhs = repr_stack.pop()
            lhs = repr_stack.pop()
            expr = "({} {} {})".format(lhs, op_repr[token], rhs)
            repr_stack.append(expr)

    return repr_stack[0]


def postfix_eval(stack):
    # assert len([i for i in stack if isinstance(i, int)]) * 2 - len(stack) == 1

    # if op.pow in stack:
    #     return NotImplemented

    result_stack = []
    for num_or_op in stack:
        if isinstance(num_or_op, int):
            result_stack.append(num_or_op)
        else:
            x = result_stack.pop()
            y = result_stack.pop()
            try:
                result_stack.append(Fraction(y, x)
                                    if num_or_op == op.truediv
                                    else num_or_op(y, x))
            except ZeroDivisionError:
                return

    return result_stack[0]


def postfix_pattern(input_count):
    """
    Matching pattern: the number of numbers
    is larger than the number of operators
    at each point

    All possible patterns for 4 numbers:
    num num num num  op  op  op
    num num num  op num  op  op
    num num num  op  op num  op
    num num  op num num  op  op
    num num  op num  op num  op
    """

    if input_count in postfix_cache:
        return postfix_cache[input_count]


    result = [[]]
    while len(result[0]) < 2 * input_count - 1:
        get_pattern(input_count, result)
    postfix_cache[input_count] = result

    return result


def get_pattern(n, patterns):
    present_length = len(patterns)
    for i in range(present_length):
        if patterns[i].count('num') < n:
            if patterns[i].count('num') - patterns[i].count('op') > 1:
                patterns.append(patterns[i].copy() + ['op'])
                patterns[i].append('num')
            else:
                patterns[i].append('num')
        else:
            patterns[i].append('op')


def postfix_notation(num_pattern,
                     op_pattern,
                     comb_pattern):
    # assert len(num_pattern) + len(op_pattern) == len(comb_pattern)

    num_pattern_local, op_pattern_local = \
        list(reversed(num_pattern)), list(reversed(op_pattern))

    return [num_pattern_local.pop() if num_or_op == 'num'
            else op_pattern_local.pop()
            for num_or_op in comb_pattern]


def main(target, quick):
    input_nums = []

    while True:
        index = 1
        try:
            input_nums.append(int(input('Number {}: '.format(index))))
            index += 1
        except ValueError:
            # print(input_nums)
            if len(input_nums) == 0:
                continue

            start = time()
            pretty_print(solve24(input_nums, target), input_nums, quick)
            print('Execution time: {:.03} second(s)\n'
                  .format(time()-start))
            input_nums.clear()
        except (Exception, KeyboardInterrupt):
            print()
            sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Solve the 24 game')
    parser.add_argument('-t', '--target', type=int,
                        default=24, help='specify target (default 24)')
    parser.add_argument('-q', '--quick', action='store_true',
                        help='turn on quick mode (find ' + \
                             'the first solution available)')
    args = parser.parse_args()

    main(args.target, args.quick)
