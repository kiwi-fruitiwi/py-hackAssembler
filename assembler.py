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
#
#
#
#
#
#
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


# convert a non-negative integer into a 15-bit binary number
def decToBin(n):
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


# open the file and separate into lines of an array of strings
asm = open('asm/RectL.asm', 'r')
lines = asm.readlines()


# process assembly file; initialize accumulator string to hold all instructions
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
        machineCode = '0'  # all a-instructions begin with '0'; c- with '111'
        # line[1:] gives the decimal value
        machineCode += decToBin(int(line[1:]))
    elif detection == 'c':  # parse c-instructions here
        # always in the form dest=comp;jump, where dest and jump are optional
        #   check existence of dest: '=' exists
        #   check existence of jump: ';' exists
        # the .index function in python throws ValueError if arg not found
        #
        machineCode = '111'
        dest = ''
        comp = ''
        jump = ''
        eqIndex = 0  # default value if '=' is not found
        scIndex = len(line)  # default value if ';' is not found


        # translated machine code values for dest, comp, jump
        destBits = ''
        compBits = ''
        jumpBits = ''

        try:
            eqIndex = line.index('=')
            dest = line[:eqIndex]
            destBits = destDict[dest]
        except ValueError:
            # we add 1 to make eqIndex 0 later to account for '=' in comp
            # otherwise, our comp is missing its first character when dest is
            # missing
            eqIndex = -1
            destBits = '000'
        # print(f'dest={dest} → {destBits}')

        try:
            scIndex = line.index(';')
            jump = line[scIndex+1:]
            jumpBits = jumpDict[jump]
        except ValueError:
            jumpBits = '000'
        # print(f'jump={jump} → {jumpBits}')

        # if neither '=' nor ';' were found, comp is just the entire line!
        comp = line[eqIndex+1:scIndex]
        compBits = compDict[comp]
        # print(f'comp={comp} → {compBits}')


        # assemble machine code from 4 components: '111', dest, comp, jump
        machineCode += compBits + destBits + jumpBits
        # print(f'c-ins: {machineCode}')

    output += machineCode + '\n'

    # print(f'{line} → {machineCode}')  # .strip is python's .trim

print(f'{output}')



'''
# decToBin tests
for i in range(0, 17):
    print(f'{decToBin(i)} → {i} 🐳')
'''