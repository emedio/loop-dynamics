#!/usr/bin/env python
import parmed as pmd

open_parm = pmd.load_file('open/tleap/open_tleap.parm7', 
                          xyz='open/tleap/open_tleap.inpcrd')
pmd.tools.addPDB(open_parm, 'open/tleap/open_tleap.pdb').execute()

closed_parm = pmd.load_file('closed/tleap/closed_tleap.parm7', 
                            xyz='closed/tleap/closed_tleap.inpcrd')
pmd.tools.addPDB(closed_parm, 'closed/tleap/closed_tleap.pdb').execute()


# Remove some waters from closed to make sure both systems have 
# the same topology

def res_max_z(res):
    '''Returns largest z coordinate of any atom in the residue'''
    return max(a.xz for a in res.atoms)

def is_water(res):
    return res.name == 'WAT'

n_wat_to_remove = len(closed_parm.residues) - len(open_parm.residues)

# Remove the waters that have the largest z coordinate
closed_waters = filter(is_water, closed_parm.residues)
res_to_remove = sorted(closed_waters, key=res_max_z)[-n_wat_to_remove:]
remove_selection = ':' + ','.join(str(res.number + 1) for res in res_to_remove)
closed_parm.strip(remove_selection)


# Assign chains/residue numbers

for parm in (closed_parm, open_parm):

    for res in parm.residues:
        res.insertion_code = ''    

    # Start from 187
    for i, res in enumerate(parm.residues[:282]):
        res.chain = 'A'
        res.number = i + 187

    # Separate chain for ions
    for i, res in enumerate(parm.residues[282:286]):
        res.chain = 'S'
        res.number = i + 1

    # Split waters into chains of max 9999 residues to avoid problems
    # when loading pdb
    for i, res in enumerate(parm.residues[286:]):
        res.chain = 'XYZ'[i // 9999]
        res.number = i % 9999 + 1


open_parm.save('open/open.parm7', overwrite=True)
open_parm.write_rst7('open/open.rst7')
open_parm.write_pdb('open/open.pdb', renumber=False)

closed_parm.save('closed/closed.parm7', overwrite=True)
closed_parm.write_rst7('closed/closed.rst7')
closed_parm.write_pdb('closed/closed.pdb', renumber=False)
