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
#
#
#
#
#
#
#
#
#


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
asm = open('asm/Max.asm', 'r')
lines = asm.readlines()


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


    # line.strip removes spaces at the beginning and at the end of the string
    #   likely equivalent to JavaScript's .trim()
    print(f'{line.strip()}')


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

'''
# decToBin tests
for i in range(0, 17):
    print(f'{decToBin(i)} → {i} 🐳')
'''