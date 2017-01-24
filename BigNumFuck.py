#!/usr/bin/env python


##############
# BigNumFuck #
##############


### DIALECT SPECIFICATION ######################################################
#                                                                              #
# BigNumFuck is a numeric dialect of the brainfuck programming language.       #
#                                                                              #
# The PROGRAM is parsed in advance to remove all non valid tokens and to check #
# for matching brackets integrity.                                             #
#                                                                              #
# The INPUT and the OUTPUT are formated as a stream of non-negative integers   #
# that are lazily consumed/produced using the Python's iterator protocol.      #
# Reading from an exhausted INPUT buffer does nothing in the current cell.     #
#                                                                              #
# Each cell is initialized with a '0' and may contain any positive integer     #
# (of arbitrary size). A '-' does nothing in a cell already containing a '0'.  #
#                                                                              #
# The TAPE grows dinamically each time a '>' reaches the right end.            #
# A '<' does nothing if the TAPE_POINTER is in the origin (TAPE[0]).           #
#                                                                              #
################################################################################


### THE BIGNUMFUCK INTERPRETER #################################################
def BigNumFuck(PROGRAM, INPUT, DEBUG=False):                                   #
                                                                               #
    ### INITIALIZE THE BIGNUMFUCK VIRTUAL MACHINE ###############              #
    TOKENS   = '<>+-[].,'                                       #              #
    PROGRAM  = "".join(c for c in PROGRAM if c in TOKENS)       #              #
    INPUT    = iter(INPUT)                                      #              #
    TAPE     = [0]                                              #              #
    TAPE_PTR = 0                                                #              #
    PROG_PTR = 0                                                #              #
    if DEBUG: print(' TOKEN   TAPE\n        [0]')               #              #
    #############################################################              #
                                                                               #
                                                                               #
    ### PRECOMPUTE BRACKET PAIRS ################################              #
    stack = []                                                  #              #
    TWIN  = dict()                                              #              #
    for ptr, token in enumerate(PROGRAM):                       #              #
        if token == "[": stack.append(ptr)                      #              #
        if token == "]":                                        #              #
            if stack:                                           #              #
                start = stack.pop()                             #              #
                TWIN[start] = ptr                               #              #
                TWIN[ptr] = start                               #              #
            else: raise SyntaxError("Unmached ']' bracket!")    #              #
    if stack: raise SyntaxError("Unmached '[' bracket!")        #              #
    #############################################################              #
                                                                               #
                                                                               #
    ### MAIN LOOP ###############################################              #
    while PROG_PTR < len(PROGRAM):                              #              #
        command = PROGRAM[PROG_PTR]                             #              #
                                                                #              #
        if command == '>':                                      #              #
            TAPE_PTR += 1                                       #              #
            if TAPE_PTR == len(TAPE): TAPE.append(0)            #              #
                                                                #              #
        elif command == '<':                                    #              #
            TAPE_PTR = max(TAPE_PTR-1, 0)                       #              #
                                                                #              #
        elif command == '+':                                    #              #
            TAPE[TAPE_PTR] += 1                                 #              #
                                                                #              #
        elif command == '-':                                    #              #
            TAPE[TAPE_PTR] = max(TAPE[TAPE_PTR]-1, 0)           #              #
                                                                #              #
        elif command == '[':                                    #              #
            if TAPE[TAPE_PTR] == 0:                             #              #
                PROG_PTR = TWIN[PROG_PTR]                       #              #
                                                                #              #
        elif command == ']':                                    #              #
            if TAPE[TAPE_PTR] != 0:                             #              #
                PROG_PTR = TWIN[PROG_PTR]                       #              #
                                                                #              #
        elif command == '.':                                    #              #
            yield TAPE[TAPE_PTR]                                #              #
                                                                #              #
        elif command == ',':                                    #              #
            try: TAPE[TAPE_PTR] = max(INPUT.next(), 0)          #              #
            except AttributeError:                              #              #
                try: TAPE[TAPE_PTR] = max(next(INPUT), 0)       #              #
                except StopIteration: pass                      #              #
            except StopIteration: pass                          #              #
                                                                #              #
        if DEBUG and command in '<>+-,.':                       #              #
            D1 = '   '+command+' '*(3+2*min(1,TAPE_PTR))        #              #
            D2 = '  '.join([str(n) for n in TAPE[:TAPE_PTR]])   #              #
            D3 = ' ['+str(TAPE[TAPE_PTR])+'] '                  #              #
            D4 = '  '.join([str(n) for n in TAPE[TAPE_PTR+1:]]) #              #
            print(D1+D2+D3+D4)                                  #              #
                                                                #              #
        PROG_PTR += 1                                           #              #
    #############################################################              #
                                                                               #
################################################################################



### MAIN FUNCTION ##############################################################
                                                                               #
if __name__ == "__main__":                                                     #
                                                                               #
                                                                               #
    # Simple aplication of the interpreter:                                    #
    print("\nPrints the first N Fibonacci numbers:")                           #
    PROGRAM = ",>>+<<[->.[->>+<<]>[-<+>>+<]>[-<+>]<<<]"                        #
    INPUT   = [10]                                                             #
    for n in BigNumFuck(PROGRAM, INPUT): print(n)                              #
                                                                               #
                                                                               #
    # Storing the output in a list:                                            #     
    print("\nPrints 2**N in binary")                                           #
    PROGRAM = ">,[[->+<]+>-]+.<[-.<]"                                          #
    INPUT   = [4]                                                              #
    OUTPUT  = list(BigNumFuck(PROGRAM, INPUT))                                 #
    print("".join(str(bit) for bit in OUTPUT))                                 #
                                                                               #
                                                                               #
    # Truncating an infinite stream of bits:                                   #
    print("\nPrints the infinite Thue-Morse Sequence")                         #
    PROGRAM = ">>+>+<[[>-.+[>]+<<[->-<<<]>[>+<<]>]>++<++]"                     #
    INPUT   = []                                                               #
    OUTPUT  = []                                                               #
    for n,bit in enumerate(BigNumFuck(PROGRAM, INPUT)):                        #
        if n == 2**5: break                                                    #
        OUTPUT.append(str(bit))                                                #
    print("".join(OUTPUT)+'...')                                               #
                                                                               #
                                                                               #
    # Chaining streams functional-programming-style:                           #
    from itertools import chain                                                #
    print("\nPrints the first N odd numbers")                                  #    
    COUNT  = "+.[+.]"                                                          #
    IF_ODD = ">>>+<,[[<+<+>>-]<[->[->-]>[<+>->]<+<<]>[-<<.>>]<<[-]>>,]"        #
    ODDS   = BigNumFuck(IF_ODD, BigNumFuck(COUNT, []))                         #
    TAKE_N = ",[->,.<]"                                                        #
    INPUT  = [4]                                                               #
    for n in BigNumFuck(TAKE_N, chain(INPUT, ODDS)): print(n)                  #
                                                                               #
################################################################################

