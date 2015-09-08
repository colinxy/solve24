#! /usr/bin/env python3

"""
24 GAME:
With 4 numbers, use addition, subtraction, multiplication and
division and parenthesis to achieve 24.

Note: this is an extended version of 24 solver, allowing more
than 4 numbers as input, and targets other than 24. Also,
operators other than addition, subtraction, multiplication and
division can be supported. But one word of advice, do not put
exponent into the operators that might cost memory error even
for small inputs.

The program gives all possible solutions to each set of input
numbers. The program makes use of reverse polish notation to
enumerate any combination of numbers and operations, without
the concern of parenthesis.

The time complexity for the solution is O(N! * M^(N-1) * N^2)
where N is the number of inputs and M is the number of allowed
operations. Therefore, the execution time is going to increase
dramatically as number of inputs increases.


usage: solve24.py [-h] [-t TARGET]

Solve the 24 game

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        specify target (default 24)
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
rp_pattern_cache = {4: [['num', 'num', 'num', 'num',  'op',  'op',  'op'],
                        ['num', 'num', 'num',  'op', 'num',  'op',  'op'],
                        ['num', 'num', 'num',  'op',  'op', 'num',  'op'],
                        ['num', 'num',  'op', 'num', 'num',  'op',  'op'],
                        ['num', 'num',  'op', 'num',  'op', 'num',  'op']]
                    }


def solve24(numbers, target=24):
    for num_patterns in permutations(numbers):
        for op_patterns in product(set_of_operators,
                         repeat=len(numbers)-1):
            for combin_patterns in reverse_polish_pattern(len(numbers)):
                notation = reverse_polish_notation(num_patterns,
                                                   op_patterns,
                                                   combin_patterns)
                if reverse_polish_eval(notation) == target:
                    yield notation


def pretty_print(results, input_numbers):
    print()
    results = list(results)
    for result in results:
        print('     ',
              ' '.join([str(num_or_op) if isinstance(num_or_op, int)
                        else op_repr[num_or_op]
                        for num_or_op in result]))
    print('===', len(results), "solution(s) for", sorted(input_numbers), '===')


def reverse_polish_eval(stack):
    assert len([i for i in stack if isinstance(i, int)]) * 2 - len(stack) == 1

    if op.pow in stack:
        return NotImplemented

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


def reverse_polish_pattern(input_count):
    """
    Matching pattern: the number of numbers is larger than
    the number of operators at each point

    All possible patterns for 4 numbers:
    num num num num  op  op  op
    num num num  op num  op  op
    num num num  op  op num  op
    num num  op num num  op  op
    num num  op num  op num  op
    """

    if input_count in rp_pattern_cache:
        return rp_pattern_cache[input_count]

    def rp_pattern(n, patterns):
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

    result = [[]]
    while len(result[0]) < 2 * input_count - 1:
        rp_pattern(input_count, result)
    rp_pattern_cache[input_count] = result

    return result


def reverse_polish_notation(number_pattern,
                            operator_pattern,
                            combination_pattern):
    assert len(number_pattern) + len(operator_pattern) == \
           len(combination_pattern)

    number_pattern_local, operator_pattern_local = \
        list(reversed(number_pattern)), list(reversed(operator_pattern))

    return [number_pattern_local.pop() if num_or_op == 'num'
            else operator_pattern_local.pop()
            for num_or_op in combination_pattern]


def main(target):
    input_numbers = []
    index = 1
    while True:
        try:
            input_numbers.append(int(input('Number ' +
                                           str(index) +
                                           ': ')))
            index += 1
        except ValueError:
            # print(input_numbers)
            start = time()
            pretty_print(solve24(input_numbers, target), input_numbers)
            print('Execution time: {0:.03} second(s)\n'.format(time()-start))
            input_numbers.clear()
            index = 1
        except (Exception, KeyboardInterrupt):
            print()
            sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Solve the 24 game')
    parser.add_argument('-t', '--target', type=int,
                        default=24, help='specify target (default 24)')
    args = parser.parse_args()

    main(args.target)
