# @author Kiwi
# @date 2022.03.06
#   a port of our JavaScript hack assembler in Python
#
# coding plan
#   read files, output file contents
#       remove starting comments → look for '//' start
#       remove whitespace → newlines ignored
#       remove midline comments → index for '//', slice
#   decimal to binary conversion
#   add dictionaries for c-instructions
#   a-instruction vs c-instruction detection
#   convert a-instructions to 15-bit binary value
#       parse the decimal value following @
#   convert c-instructions
#       detect component existence
#       tokenize dest=comp;jump
#       assemble machineCode translations
#   pass RectL, MaxL symbol-less translation
#       → REFACTOR
#
#   1st pass for symbol assembler: build symbolTable
#       iterate through every line in the asm file
#       if comment or whitespace → skip
#       add label symbols to symbolTable, minding lineNumbers
#           labels are not instructions, so their line number is next line
#       fill firstPassResults, a string array used in the second pass ↓
#
#   2nd pass for symbol assembler:
#       set n to 16
#       scan entire asm file again using firstPassResults
#       if instruction is @symbol, look it up in symbolTable
#           if (symbol, value) is found, use value to complete translation
#           if not found:
#               add (symbol, n) to symbolTable
#               use n to complete the instruction's translation
#                   @symbol becomes 0 decToBin(int(n))
#                   n++
#       if instruction is a c-instruction, translate normally
#           encapsulate c-instruction translation as a function
#


# dictionaries for translating c-instructions
compDict = {
    "0":    "0101010",
    "1":    "0111111",
    "-1":   "0111010",
    "D":    "0001100",
    "A":    "0110000",
    "M":    "1110000",
    "!D":   "0001101",
    "!A":   "0110001",
    "!M":   "1110001",
    "-D":   "0001111",
    "-A":   "0110011",
    "-M":   "1110011",
    "D+1":  "0011111",
    "A+1":  "0110111",
    "M+1":  "1110111",
    "D-1":  "0001110",
    "A-1":  "0110010",
    "M-1":  "1110010",
    "D+A":  "0000010",
    "D+M":  "1000010",
    "D-A":  "0010011",
    "D-M":  "1010011",
    "A-D":  "0000111",
    "M-D":  "1000111",
    "D&A":  "0000000",
    "D&M":  "1000000",
    "D|A":  "0010101",
    "D|M":  "1010101"
}
destDict = {
    "null":  "000",
    "M":     "001",
    "D":     "010",
    "MD":    "011",
    "A":     "100",
    "AM":    "101",
    "AD":    "110",
    "AMD":   "111",
}
jumpDict = {
    "null":  "000",
    "JGT":   "001",
    "JEQ":   "010",
    "JGE":   "011",
    "JLT":   "100",
    "JNE":   "101",
    "JLE":   "110",
    "JMP":   "111",
}


# symbolTable initialization for 1st pass
symbolTable = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
}


def decToBin(n: int) -> str:
    """
    convert a non-negative integer into a 15-bit binary number
    :param n:
    :return:
    """
    # construct a string of 0's and 1's up to 15 bits
    power = 14
    result = ""

    # build a 15-bit binary number by seeing what powers of 2 divide into input
    while power >= 0:
        if n - 2**power >= 0:
            result = result + "1"
            n -= 2**power
        else:
            result = result + "0"

        power -= 1
    return result


def translateC(asm_line: str) -> str:
    """
    translates a c-instruction in the form of dest=comp;jump into binary
    in machine language, c-instructions are in the format 111 acccccc ddd jjj
    identify if we have all three parts: dest=comp;jump
    :param asm_line: the line of assembly we want to translate
    :return: 16-bit machine code
    """
    # always in the form dest=comp;jump, where dest and jump are optional
    #   check existence of dest: '=' exists
    #   check existence of jump: ';' exists
    # the .index function in python throws ValueError if arg not found
    #
    scIndex = len(asm_line)  # default value if ';' is not found

    try:
        eqIndex = asm_line.index('=')
        dest = asm_line[:eqIndex]
        dest_bits = destDict[dest]
    except ValueError:
        # we add 1 to make eqIndex 0 later to account for '=' in comp
        # otherwise, our comp is missing its first character when dest is
        # missing
        eqIndex = -1
        dest_bits = '000'
    # print(f' dest={dest} → {dest_bits}')

    try:
        scIndex = asm_line.index(';')
        jump = asm_line[scIndex + 1:]
        jump_bits = jumpDict[jump]
    except ValueError:
        jump_bits = '000'

    # if neither '=' nor ';' were found, comp is just the entire line!
    comp = asm_line[eqIndex + 1:scIndex]
    comp_bits = compDict[comp]

    # assemble machine code from 4 components: '111', dest, comp, jump
    return '111' + comp_bits + dest_bits + jump_bits


def assembleL(file: str) -> None:
    """
    translates assembly language in a .asm file and outputs the result as
    machine code. only works for symbol-Less .asm files.
    :param file: the .asm file we are reading from
    """
    # open the file and separate into lines of an array of strings
    asm = open(file, 'r')
    lines = asm.readlines()
    output = ''

    for line in lines:
        # ignore whitespace
        if line == '\n':
            continue

        # ignore entire-line comments
        if line[0] == '/' and line[1] == '/':
            continue

        # ignore mid-line comments
        try:
            index = line.index('//')
            line = line[0:index]
        except ValueError:
            # '//' wasn't found!
            pass


        # strip whitespace
        line = line.strip()


        # detect a- vs c-instruction based on first character
        detection = 'a' if line[0] == '@' else 'c'


        # initialize machine code translation
        machineCode = '0'


        # find the decimal value following @ in an a-instruction
        if detection == 'a':
            machineCode = '0'  # all a-instructions begin with '0'; c with '111'
            # line[1:] gives the decimal value
            machineCode += decToBin(int(line[1:]))
        elif detection == 'c':  # parse c-instructions here
            machineCode = translateC(line)

        output += machineCode + '\n'

    print(f'{output}')


assembleL('asm/RectL.asm')