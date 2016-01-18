# solve24

24 GAME:
With 4 numbers, use addition, subtraction, multiplication and
division and parenthesis to achieve 24.

Note: this is an extended version of 24 solver, allowing more
than 4 numbers as input, and targets other than 24. Also,
operators other than addition, subtraction, multiplication and
division can be supported. To add a new operator, add the
function of the operator into global variable 'set_of_operators',
and its representation into global variable 'op_repr'.
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
