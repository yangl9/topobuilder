# topobuilder
a py script which helps build topology file for LAMMPS from *.pdb (currently only available for CHARMM-gen ff)

The example shows how to build the topology file of a molecule with a 6-member ring, a 5-member ring, and a chain with a certain length.
Most of the force field parameters can be found in the par* file by searching ff of atoms specified previously in atom.ff. But there are
some missing, e.g. the bond connecting the 6-member ring and the 5-member ring (CG2R51-CG2R67). In this case we use CG2R67-CG2R67 instead,
assuming the parameters of CG2R67-CG2R67 whould be similar to that of CG2R51-CG2R67 bond. 

Further, angles will be built in the same way. If some information is missing, we enter it manually. The entered information of the missing
bonds will also be used when searching for force field parameters of angles, and that of the missing angles will be used when searching for 
force field parameters of dihedrals.

Sorry that the pair and improper sections do not work correctly at present. 

HOW TO RUN:

 USE ipython topobuilder_CHARMM-gen.py *.pdb
 
 par_all36_cgenff.prm and atom.ff have to be in the same directory.
 
 If you do not like typing in lost info every time, put it in the "input" file instead.
 
 But once "input" does exist, the lost info would be read from it.
 
 You need to build the atom.ff file by your own first, which contains
 
  column 1,          column 2
  
  atom number,       ff type e.g. CG321
  
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
