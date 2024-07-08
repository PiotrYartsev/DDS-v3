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
for line in lines[-10:]:
        #add an extra letter a at a random position
        position = random.randint(0, len(line))
        line = line[:position] + 'a' + line[position:]
        lines.append(line)



open_file.close()
file2='ruciodump/LUND_GRIDFTP-RUCIO-2023_10_06.txt'

open_file = open(file2, 'w')
open_file.writelines(lines)
open_file.close
print('done')
