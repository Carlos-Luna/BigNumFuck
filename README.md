# BigNumFuck

**BigNumFuck** is a dialect of the **brainfuck programming language**<sup>(1)</sup> that uses the same 8 simple commands (```+-<>[],.```) but works with numbers instead of ASCII characters. This simplifies the input/output of many programs without changing the basic language idioms that characterize **brainfuck**.

I provide an unoptimized interpreter of **BigNumFuck** implemented as a lazy generator function writen in Python 2/3 compatible code. It is able to deal with non-negative integers of arbitrary size and it will dinamically adapt the length of the tape as soon as its right end is reached.

## Implementation Details:

**Syntax:** ```BigNumFuck(PROGRAM, INPUT, DEBUG = False)```
* The ```PROGRAM``` is parsed in advance to remove all non valid tokens and to check for matching brackets integrity.
* The ```INPUT``` and the ```OUTPUT``` are formated as a stream of non-negative integers that are lazily consumed/produced using the Python's iterator protocol. Reading from an exhausted ```INPUT``` buffer does nothing in the current cell.
* Each cell is initialized with a '```0```' and may contain any positive integer (of arbitrary size). A '```-```' does nothing in a cell already containing a '```0```'. 
* The ```TAPE``` grows dinamically each time a '```>```' reaches the right end. A '```<```' does nothing if the ```TAPE_PTR``` is in the origin (```TAPE[0]```).
* Set ```DEBUG = True``` to get a really verbose output.

----

<sup>(1)</sup> https://en.wikipedia.org/wiki/Brainfuck
