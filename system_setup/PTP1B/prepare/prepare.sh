#/bin/bash
for name in closed open; do
    mkdir $name
    cd $name
    ../enlighten_prep.py ../../clean_pdb/${name}_raw.pdb propka/${name}_propka.pdb
    mkdir tleap
    cd tleap
    sed "/HG  CYS A 214/d" ../propka/${name}_propka.pdb > ${name}_for_tleap.pdb
    sed -i "s/CYS A 214/CYX A 214/g" ${name}_for_tleap.pdb
    sed "s/__NAME__/$name/g" ../../tleap.template > tleap.in
    tleap -f tleap.in
    cd ../..
done
./postprocess.py
cp closed/closed.parm7 ptp1b.parm7
sed -i "s/CTITLE/TITLE/g" ptp1b.parm7 # If old parmed is used
