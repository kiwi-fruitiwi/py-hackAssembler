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