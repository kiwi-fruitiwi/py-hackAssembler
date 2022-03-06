# @author Kiwi
# @date 2022.03.06
#   a port of our JavaScript hack assembler in Python


# open the file and separate into lines of an array of strings
asm = open('asm/Add.asm', 'r')
lines = asm.readlines()

for line in lines:
    # line.strip removes spaces at the beginning and at the end of the string
    #   likely equivalent to JavaScript's .trim()
    print(f'{line.strip()}')