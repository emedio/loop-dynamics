#!/usr/bin/env python
import sys
from enlighten2.pdb_utils import Pdb
from enlighten2.wrappers import Pdb4AmberReduceWrapper, PropkaWrapper

with open(sys.argv[1], 'r') as f:
    pdb = Pdb(f)

pdb4amber_pdb = Pdb4AmberReduceWrapper(pdb).pdb
PropkaWrapper(pdb4amber_pdb, ph=7.0).pdb.to_filename(sys.argv[2])

