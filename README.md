# topobuilder
a py script which helps build topology file for LAMMPS from *.pdb (currently only available for CHARMM-gen ff)

HOW TO RUN:

 USE ipython topobuilder_CHARMM-gen.py *.pdb
 
 par_all36_cgenff.prm and atom.ff have to be in the same directory.
 
 If you do not like typing in lost info every time, put it in the "input" file instead.
 
 But once "input" does exist, the lost info would be read from it.
 
 You need to build the atom.ff file by your own first, which contains
 
  column 1          column 2
  
  atom number       ff type e.g. CG321
  
 the sequence of which should be the same as *.pdb.
 
 Do not forget enter the charges for atoms, which can be found in top_all36_cgenff.rtf or calculated by ab initio.


Step 1 # Now you are searching ff of: bonds

SCREEN OUTPUT

 number of unfound bonds: $somenumber
 
 Now please enter the bond types, which do exist in par file,
 
 and can be used as a substitute of the unfound one.
 
 e.g. CG2R61 CG2R61 (new)-> CG2R51 CG2R61(unfound)
 
 STRICT Format: CG2R61 CG2R61


Step 2  # Now you are searching ff of: angles

SCREEN OUTPUT

unfound angle $some...

unfound angle $some...

 number of unfound angles: $somenumber
 
 Now please enter the angle types, which do exist in par file,
 
 and can be used as a substitute of the unfound one.
 
 e.g. CG2R61 CG2R61 CG2R61 (new)-> CG2R51 CG2R61 CG2R61 (unfound)
 
 STRICT Format: CG2R61 CG2R61 CG2R61


Step3  # Now you are searching ff of: dihedrals

SCREEN OUTPUT

e.g. unfound dihedral  8 , atomff_type: CG321  CG321  NG2R51 NG2R50  , atoms number: 6 5 1 2

Step4  # Now you are searching ff of: impropers

e.g. unfound improper  1 , atomff_type: CG321  NG2R51 NG2R50 CG2R51  , atoms number: 5 1 2 22
 Writing to guest2.top ... 
 Done! But you need to further enter the lost info of dihedrals and impropers.
