#!/usr/bin/env python

a_6b90 = open('6B90_A.pdb', 'w')
b_6b90 = open('6B90_B.pdb', 'w')

with open('6B90.pdb') as f:
    for line in f:
        if not any(map(line.startswith, ('ATOM', 'HETATM', 'TER'))):
            continue
        if any(map(line.__contains__, ('GOL', 'TRS'))):
            continue
        if line[16] == 'C':
            continue
        if line[16] == 'A':
            a_6b90.write(line[:16] + ' ' + line[17:])
        elif line[16] == 'B':
            b_6b90.write(line[:16] + ' ' + line[17:])
        else:
            a_6b90.write(line)
            b_6b90.write(line)

a_6b90.close()
b_6b90.close()
