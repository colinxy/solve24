"""
24 GAME:
With 4 numbers, use addition, subtraction, multiplication and
division and parenthesis to achieve 24.

Note: this is an extended version of 24solver, allowing more
than 4 numbers as input, and targets other than 24. Also,
operators other than addition, subtraction, multiplication and
division can be supported. But one word of advice, do not put
exponent into the operators that might cost memory error even
for small inputs.

The program gives all possible solutions to each set of input
numbers. The program makes use of reverse polish notation to
enumerate any combination of numbers and operations, without
the concern of parenthesis.

The solver can not eliminate repeat such as 1 + 2 and 2 + 1 as
for now, but will not include repeat as 1 + 1 twice.

The time complexity for the solution is O(N! * M**(N-1) * N**2)
where N is the number of inputs and M is the number of allowed
operations. Therefore, the execution time is going to increase
dramatically as number of inputs increases.
"""
__author__ = 'yxy'


from time import time
from itertools import product
import operator
from fractions import Fraction


target = 24
set_of_operators = {operator.add, operator.sub, operator.mul, operator.truediv}
rp_pattern_cache = {4: [['num', 'num', 'num', 'num',  'op',  'op',  'op'],
                        ['num', 'num', 'num',  'op', 'num',  'op',  'op'],
                        ['num', 'num', 'num',  'op',  'op', 'num',  'op'],
                        ['num', 'num',  'op', 'num', 'num',  'op',  'op'],
                        ['num', 'num',  'op', 'num',  'op', 'num',  'op']]
                    }


def solve24(numbers):
    for i in permutation_formatted(numbers):  # number_patterns
        for j in product(set_of_operators, repeat=len(numbers)-1):  # operator_patterns
            for k in reverse_polish_pattern(len(numbers)):  # combination_patterns
                notation = reverse_polish_notation(i, j, k)
                if reverse_polish_eval(notation) == target:
                    yield notation


def pretty_print(results, input_numbers):
    print()
    results = list(results)
    for result in results:
        print(' '.join([str(num_or_op) if isinstance(num_or_op, int) else num_or_op.__name__ for num_or_op in result]))
    print('===', len(results), "solution(s) for", sorted(input_numbers), '===')


def reverse_polish_eval(stack):
    assert len([i for i in stack if isinstance(i, int)]) * 2 - len(stack) - 1 == 0

    if operator.pow in stack:
        return NotImplemented

    result_stack = []
    for num_or_op in stack:
        if isinstance(num_or_op, int):
            result_stack.append(num_or_op)
        else:
            x = result_stack.pop()
            y = result_stack.pop()
            try:
                result_stack.append(num_or_op(y, x))
            except ZeroDivisionError:
                return ZeroDivisionError

    return result_stack[0]


def permutation(numbers):
    """
    input: a list of numbers, repeat allowed
    output: all possible permutations of the given list
    """
    if len(numbers) == 1:
        return [numbers]

    result = []
    for i in range(len(numbers)):
        result.extend([j + [numbers[i]] for j in permutation(numbers[:i] + numbers[i+1:])])

    return result


def permutation_formatted(numbers):
    result = permutation(numbers)
    return sorted(set([tuple(i) for i in result]))


def reverse_polish_pattern(input_count):
    """
    Matching pattern: the number of numbers is larger than the number of operators at each point

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


def reverse_polish_notation(number_pattern, operator_pattern, combination_pattern):
    assert len(number_pattern) + len(operator_pattern) == len(combination_pattern)
    number_pattern_local, operator_pattern_local = list(number_pattern), list(operator_pattern)
    return [number_pattern_local.pop(0) if num_or_op == 'num' else operator_pattern_local.pop(0) for num_or_op in combination_pattern]


def main():
    input_numbers = []
    while True:
        try:
            input_numbers.append(int(input('Number please: ')))
        except ValueError:
            # print(input_numbers)
            start = time()
            pretty_print(solve24(input_numbers), input_numbers)
            print('Execution time:', time() - start, '\n')
            input_numbers = []


if __name__ == '__main__':
    # starting_time = time()
    main()
    # print('Total running time:', time() - starting_time)
