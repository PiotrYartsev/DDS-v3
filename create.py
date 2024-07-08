#open txt file rsedump/
#Remove about 20% of the lines at random
#Change about 20% of the lines by putting a random character in a random position in the line
#Add about 20% of the lines by duplicating a random line
#Save the modified file

import os
import random
import string


file='rsedump/LUND_GRIDFTP-RSE-2023_10_06.txt'

open_file = open(file, 'r')
lines = open_file.readlines()

#Remove about 20% of the lines at random
lines = [line for line in lines if random.random() > 0.2]

#Change about 20% of the lines by putting a random character in a random position in the line
def change_line(line):
    line = list(line)
    line[random.randint(0, len(line)-1)] = random.choice(string.ascii_letters)
    return ''.join(line)

lines = [change_line(line) if random.random() > 0.2 else line for line in lines]


open_file.close()
file2='ruciodump/LUND_GRIDFTP-RUCIO-2023_10_06.txt'

open_file = open(file2, 'w')
open_file.writelines(lines)
open_file.close
print('done')
