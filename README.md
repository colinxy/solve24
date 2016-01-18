# solve24

24 GAME:
With 4 numbers, use addition, subtraction, multiplication and
division and parenthesis to achieve 24.

Note: this is an extended version of 24 solver, allowing more
than 4 numbers as input, and any number as target. Also,
operators other than addition, subtraction, multiplication and
division can be supported. To add a new operator, add the
function of the operator into the global variable 'set_of_operators',
and its string representation into global variable 'op_repr'.
The operator is assumed to be binary and operator precedence is
irrelevant in this case.

The program gives all possible solutions to each set of input
numbers. The program makes use of reverse polish (postfix)
notation to enumerate any combination of numbers and operations,
without the concern of parenthesis.

The program make use of brute force enumeration, so it runs very
slow with more than 5 numbers as input. To make it run faster,
turn on quick mode with the option '-q', which finds the first
solution available.


usage: solve24.py [-h] [-t TARGET] [-q]

Solve the 24 game

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        specify target (default 24)
  -q, --quick           turn on quick mode (find the first solution available)
