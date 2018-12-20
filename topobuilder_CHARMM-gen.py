# -*- coding: utf-8 -*-
# github SINgroup
#L.Yang: yangjinlei1988@163.com
from __future__ import print_function
from sys import argv
import itertools
import sys
import re

print("# USE ipython topobuilder_CHARMM-gen.py *.pdb")
print("# par_all36_cgenff.prm and atom.ff have to be in the same directory.")
print('# If you do not like typing in lost info every time, put it in the "input" file instead.')
print('# But once "input" does exist, the lost info would be read from it.')

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		pass
	try:
		import unicodedata
		unicodedata.numeric(s)
		return True
	except (TypeError, ValueError):
		pass
	return False

pdb = argv[1]
par = "par_all36_cgenff.prm"

isfi = 1
try:
	fi0 = open("input", mode='r')
except IOError:
	isfi = 0

with open(pdb, "r") as fi1:
	content = fi1.readlines()
content = [x.strip() for x in content]
content = [x.split() for x in content]
nline = len(content)
nat = 0
for line in range(nline):
	if content[line][0] == 'ATOM':
		nat += 1

with open(par, "r") as fi2:
    ffinfo = fi2.readlines()
ffinfo = [x.strip() for x in ffinfo]

with open("atom.ff", "r") as fi3:
    atomffinfo = fi3.readlines()
atomff = [x.strip() for x in atomffinfo]
atomff = [x.split() for x in atomffinfo]
nlinea = len(atomff)
for line in range(nlinea):
	atomff[line][1] = atomff[line][1].ljust(7)

#! atom
print ("# You need to build the atom.ff file by your own first, which contains")
print ("#  column 1          column 2")
print ("#  atom number       ff type e.g. CG321")
print ("# the sequence of which should be the same as *.pdb.")
print ("# Do not forget enter the charges for atoms, which can be found in top_all36_cgenff.rtf or calculated by ab initio.")

fo0 = []
for line in range(nat):
	s = atomff[line][1]
	so = []
	for lnff in range (110,285): #! search s in atoms section of par 
		if s != "" and re.search(s, ffinfo[lnff]):
			so = ffinfo[lnff].strip().split()
	fo0.append(line)
	fo0[line] = str(line+1) + " " + str(so[3]) + "\n"

coor = []
for line in range(nat):
	coor.append(line)
	coor[line] = str(line+1) + "   1   " + str(line+1) + '   ' + content[line+1][6].ljust(8) + ' ' + content[line+1][7].ljust(8) + ' ' + content[line+1][8].ljust(8) + '\n'

#! pairs
fopair = []
for line in range(nat):
	s = atomff[line][1]
	so = ""
	for lnff in range (6375,6912): #! search s in nonbonded section of par 
		if s != "" and re.search(s, ffinfo[lnff]):
			so = ffinfo[lnff]
			lso = so.strip().split()
	eps = abs(float(lso[2]))
	sig = float(lso[3])*2**(-1/6)
	fopair.append(line)
	fopair[line] = str(line+1) + " " + str(eps) + "  " + str(sig) + "  #" + so + "\n"

#! bond
print ('\n # Now you are searching ff of: bonds\n')
fo1 = []
fo2 = []

cb = 0
cb2 = 0
ub = 0
markb = [] #! Who tells that py does not need pre-define ???
markb1 = [] #! I hate .append.
markb2 = []
inb1 = []
inb2 = []

for line in range(nat+1,2*nat+1):
	nele = len(content[line])
	cb2 += 1
	if nele > 2:
#!      put the connecting atoms of the line_th atom to an list
		for nag in range(2,nele):
			s = ""
			sr = ""
			if int(content[line][nag]) > cb2: #! avoid double-counted
				i1 = int(content[line][1])
				i2 = int(content[line][nag])
				s = atomff[i1-1][1] + atomff[i2-1][1] 
				sr = atomff[i2-1][1] + atomff[i1-1][1] 
				so = ""
				for lnff in range (287,814): #! search s in bond section of par
					if s != "" and re.search(s, ffinfo[lnff]):
						so = ffinfo[lnff]
					elif sr != "" and re.search(sr, ffinfo[lnff]):
						so = ffinfo[lnff]
				fo1.append(cb)
				fo1[cb] = str(cb+1) + ' ' + str(cb+1) + ' ' + content[line][1] + ' ' + content[line][nag] + '\n'
				fo2.append(cb)
				if so != '':
					lso = so.strip().split()
					fo2[cb] = str(cb+1) + ' ' + lso[2] + ' ' + lso[3] + ' #' + so + '\n'
				if so == '': #! mark the unfound
					markb.append(ub)
					markb[ub] = cb + 1 #! bond list line number
					markb1.append(ub) 
					markb1[ub] = i1 #! atom number 1
					markb2.append(ub)
					markb2[ub] = i2 #! atom number 2
					ub += 1
					print ('unfound bond ',cb+1,', atomff_type:',s,', atoms number:',i1,i2)
				cb += 1
print ('# number of unfound bonds:',ub)
print ('# Now please enter the bond types, which do exist in par file,')
print ('# and can be used as a substitute of the unfound one.')
print ('# e.g. CG2R61 CG2R61 (new)-> CG2R51 CG2R61(unfound)')
print ('# STRICT Format: CG2R61 CG2R61')
for j in range(ub):
	print ('bond ',markb[j])
	inb1.append(j)
	inb2.append(j)
	if isfi == 0:
		inb1[j] = input('atom1:  ')
		inb2[j] = input('atom2:  ')
	if isfi == 1:
		inb1[j] = fi0.readline().strip()
		inb2[j] = fi0.readline().strip()
	inb1[j] = inb1[j].ljust(7)
	inb2[j] = inb2[j].ljust(7)
	print ("Make sure again what you typed in: ",inb1[j],inb2[j])
	s = inb1[j] + inb2[j]
	sr = inb2[j] + inb1[j]
	so = ''
	for lnff in range (287,814):
		if s != "" and re.search(s, ffinfo[lnff]):
			so = ffinfo[lnff]
		elif sr != "" and re.search(sr, ffinfo[lnff]):
			so = ffinfo[lnff]
	if so != '':
		lso = so.strip().split()
		fo2[markb[j]-1] = str(markb[j]) + ' ' + lso[2] + ' ' + lso[3] + ' #' + so + '                             ??? SATISFIED ??? ' + '\n'

#! angle
print ('\n # Now you are searching ff of: angles\n')
fo4 = []
fo5 = []

ca = 0
ua = 0
marka = []
marka0 = []
marka1 = []
marka2 = []
ina1 = []
ina2 = []
ina3 = []
l = []

for line in range(nat+1,2*nat+1):
	rest = []
	nele = len(content[line])
	if nele > 3:
#!	put the connecting atoms of the line_th atom to an list
		for nag in range(2,nele):
			tmp = nag-2
			rest.append(nag)
			rest[tmp] = content[line][nag]
		ls = itertools.combinations(rest, 2) 
		#! create a list of 2,1,3 angles, 
		#! where atom2 and atom3 are connected to atom1

		for le in ls:
			l.append(ca)
			l[ca] = list(le)
			l[ca].insert(1, content[line][1])
			l[ca] = list(map(int, l[ca])) #! convert it back into integers
			s = ""
			sr = ""
			for i in l[ca]:
				s += atomff[i-1][1]
			for i in l[ca][::-1]:
				sr += atomff[i-1][1]
			so = ""
			for lnff in range (816,2457):
				if s != "" and re.search(s, ffinfo[lnff]):
					so = ffinfo[lnff]
				elif sr != "" and re.search(sr, ffinfo[lnff]):
					so = ffinfo[lnff]
			if so == '': #! use the artificial bond info instead
				for j in range(ub):
					if markb1[j] == l[ca][1]: 
						s2 = ""
						sr2 = ""
						if l[ca][0] == markb2[j]:
							s2 = inb2[j] + inb1[j] + atomff[l[ca][2]-1][1]
							sr2 = atomff[l[ca][2]-1][1] + inb1[j] + inb2[j]
						elif l[ca][2] == marka2[j]:
							s2 = atomff[l[ca][0]-1][1] + inb1[j] + inb2[j]
							sr2 = inb2[j] + inb1[j] + atomff[l[ca][0]-1][1]
#						if so == '': #! if even this does not help, use two artificial bonds
					elif markb2[j] == l[ca][1]:
						if l[ca][0] == markb1[j]:
							s2 = inb1[j] + inb2[j] + atomff[l[ca][2]-1][1]
							sr2 = atomff[l[ca][2]-1][1] + inb2[j] + inb1[j]
						elif l[ca][2] == markb1[j]:
							s2 = atomff[l[ca][0]-1][1] + inb2[j] + inb1[j]
							sr2 = inb1[j] + inb2[j] + atomff[l[ca][0]-1][1]
					for lnff in range (816,2457):
							if s2 != "" and re.search(s2, ffinfo[lnff]):
								so = ffinfo[lnff] + "                           ??? SATISFIED ??? "
							elif sr2 != "" and re.search(sr2, ffinfo[lnff]):
								so = ffinfo[lnff] + "                           ??? SATISFIED ??? "
			fo4.append(ca)
			fo4[ca] = str(ca+1) + ' ' + str(ca+1) + ' ' + str(l[ca][0]) + ' ' + str(l[ca][1]) + ' ' + str(l[ca][2]) + '\n' #! Sequence may differ from ff file
			fo5.append(ca)
			if so != '':
				lso = so.strip().split()
				if not is_number(lso[5]):
					lso[5] = "0"
					lso[6] = "0"
				fo5[ca] = str(ca+1) + ' ' + lso[3] + ' ' + lso[4] + ' ' + lso[5] + ' ' + lso[6] + ' #' + so + '\n'
			if so == '': #! mark the unfound
				marka.append(ua)
				marka[ua] = ca+1 #! angle list line number
				marka0.append(ua) 
				marka0[ua] = l[ca][0] #! atom number 1
				marka1.append(ua)
				marka1[ua] = l[ca][1] #! atom number 2
				marka2.append(ua)
				marka2[ua] = l[ca][2] #! atom number 3
				ua += 1
				print ('unfound angle ',ca+1,', atomff_type:',s,', atoms number:',l[ca][0],l[ca][1],l[ca][2])
			ca += 1
print ('# number of unfound angles:',ua)
print ('# Now please enter the angle types, which do exist in par file,')
print ('# and can be used as a substitute of the unfound one.')
print ('# e.g. CG2R61 CG2R61 CG2R61 (new)-> CG2R51 CG2R61 CG2R61 (unfound)')
print ('# STRICT Format: CG2R61 CG2R61 CG2R61')
for j in range(ua):
	print ('angle ',marka[j])
	ina1.append(j)
	ina2.append(j)
	ina3.append(j)
	if isfi == 0:
		ina1[j] = input('atom1:  ')
		ina2[j] = input('atom2:  ')
		ina3[j] = input('atom3:  ')
	if isfi == 1:
		ina1[j] = fi0.readline().strip()
		ina2[j] = fi0.readline().strip()
		ina3[j] = fi0.readline().strip()
	ina1[j] = ina1[j].ljust(7)
	ina2[j] = ina2[j].ljust(7)
	ina3[j] = ina3[j].ljust(7)
	print ("Make sure again what you typed in: ",ina1[j],ina2[j],ina3[j])
	s = ina1[j] + ina2[j] + ina3[j]
	sr = ina3[j] + ina2[j] + ina1[j]
	so = ''
	for lnff in range (816,2457):
		if s != "" and re.search(s, ffinfo[lnff]):
			so = ffinfo[lnff]
		elif sr != "" and re.search(sr, ffinfo[lnff]):
			so = ffinfo[lnff]
	if so != '':
		lso = so.strip().split()
		if not is_number(lso[5]):
			lso[5] = "0"
			lso[6] = "0"
		fo5[marka[j]-1] = str(marka[j]) + ' ' + lso[3] + ' ' + lso[4] + ' ' + lso[5] + ' ' + lso[6] + ' #' + so + '               ??? SATISFIED ??? ' + '\n'

#! Dihedral
print ('\n # Now you are searching ff of: dihedrals\n')
fo6 = []
fo7 = []
fo8 = []
fo9 = []

cd = 0
ci = 0
 
for k in range(ca): 
	if l[k][0] > l[k][1]: #! avoid double-counted
		line = l[k][0] + nat
		nele = len(content[line])
		for nag in range(2,nele):
			d1 = int(content[line][nag])
			s = ""
			sr = ""
			if d1 != l[k][1]:
				s = atomff[d1-1][1] + atomff[l[k][0]-1][1] + atomff[l[k][1]-1][1] + atomff[l[k][2]-1][1]
				sr = atomff[l[k][2]-1][1] + atomff[l[k][1]-1][1] + atomff[l[k][0]-1][1] + atomff[d1-1][1]
				so = ""
				for lnff in range (2458,6594):
					if s != "" and re.search(s, ffinfo[lnff]):
						so = ffinfo[lnff]
					elif sr != "" and re.search(sr, ffinfo[lnff]):
						so = ffinfo[lnff]
				if so == '': #! use the artificial bond info instead
					for j in range(ua):
						s2 = ""
						sr2 = ""
						if marka0[j] == l[k][0] and marka1[j] == l[k][1] and marka2[j] == l[k][2]:
							s2 = atomff[d1-1][1] + ina1[j] + ina2[j] + ina3[j]
							sr2 = ina3[j] + ina2[j] + ina1[j] + atomff[d1-1][1]
						for lnff in range (2458,6594):
								if s2 != "" and re.search(s2, ffinfo[lnff]):
									so = ffinfo[lnff] + "                 ??? SATISFIED ??? "
								elif sr2 != "" and re.search(sr2, ffinfo[lnff]):
									so = ffinfo[lnff] + "                 ??? SATISFIED ??? "
						if so == '':
							if marka0[j] == d1 and marka1[j] == l[k][0] and marka2[j] == l[k][1]:
								s2 = ina1[j] + ina2[j] + ina3[j] + atomff[l[k][2]-1][1]
								sr2 = atomff[l[k][2]-1][1] + ina3[j] + ina2[j] + ina1[j]
							elif marka0[j] == l[k][1] and marka1[j] == l[k][0] and marka2[j] == d1:
								s2 = ina3[j] + ina2[j] + ina1[j] + atomff[l[k][2]-1][1]
								sr2 = atomff[l[k][2]-1][1] + ina1[j] + ina2[j] + ina3[j]
							for lnff in range (2458,6594):
								if s2 != "" and re.search(s2, ffinfo[lnff]):
									so = ffinfo[lnff] + "                  ??? SATISFIED ??? "
								elif sr2 != "" and re.search(sr2, ffinfo[lnff]):
									so = ffinfo[lnff] + "                  ??? SATISFIED ??? "
				if so == '': #! mark the unfound
					print ('unfound dihedral ',cd+1,', atomff_type:',s,', atoms number:',d1,l[k][0],l[k][1],l[k][2])
				fo6.append(cd)
				fo6[cd] = str(cd+1) + ' ' + str(cd+1) + ' ' + str(d1) + ' ' + str(l[k][0]) + ' ' + str(l[k][1]) + ' ' + str(l[k][2]) + '\n'
				fo7.append(str(cd+1)+'\n')
				if so != '':
					lso = so.strip().split()
					fo7[cd] = str(cd+1) + ' ' + lso[4] + ' ' + lso[5] + ' ' + lso[6] + '  0.0  #' + so + '\n'
				cd += 1
	if l[k][2] > l[k][1]:
		line = l[k][2] + nat 
		nele = len(content[line])
		for nag in range(2,nele):
			d4 = int(content[line][nag])
			if d4 != l[k][1]:
				s = atomff[l[k][0]-1][1] + atomff[l[k][1]-1][1] + atomff[l[k][2]-1][1] + atomff[d4-1][1]
				sr = atomff[d4-1][1] + atomff[l[k][2]-1][1] + atomff[l[k][1]-1][1] + atomff[l[k][0]-1][1]
				so = ""
				for lnff in range (2458,6594):
					if s != "" and re.search(s, ffinfo[lnff]):
						so = ffinfo[lnff]
					elif sr != "" and re.search(sr, ffinfo[lnff]):
						so = ffinfo[lnff]
				if so == '': #! use the artificial bond info instead
					for j in range(ua):
						s2 = ""
						sr2 = ""
						if marka0[j] == l[k][0] and marka1[j] == l[k][1] and marka2[j] == l[k][2]:
							s2 = ina1[j] + ina2[j] + ina3[j] + atomff[d4-1][1]
							sr2 = atomff[d4-1][1] + ina3[j] + ina2[j] + ina1[j]
						for lnff in range (2458,6594):
								if s2 != "" and re.search(s2, ffinfo[lnff]):
									so = ffinfo[lnff] + "                   ??? SATISFIED ??? "
								elif sr2 != "" and re.search(sr2, ffinfo[lnff]):
									so = ffinfo[lnff] + "                   ??? SATISFIED ??? "
						if so == '':
							if marka0[j] == l[k][1] and marka1[j] == l[k][2] and marka2[j] == d4:
								s2 = atomff[l[k][0]-1][1] + ina1[j] + ina2[j] + ina3[j]
								sr2 = ina3[j] + ina2[j] + ina1[j] + atomff[l[k][0]-1][1]
							elif marka0[j] == d4 and marka1[j] == l[k][2] and marka2[j] == l[k][1]:
								s2 = atomff[l[k][0]-1][1] + ina3[j] + ina2[j] + ina1[j]
								sr2 = ina1[j] + ina2[j] + ina3[j] + atomff[l[k][0]-1][1]
							for lnff in range (2458,6594):
								if s2 != "" and re.search(s2, ffinfo[lnff]):
									so = ffinfo[lnff] + "                   ??? SATISFIED ??? "
								elif sr2 != "" and re.search(sr2, ffinfo[lnff]):
									so = ffinfo[lnff] + "                   ??? SATISFIED ??? "
				fo6.append(cd)
				fo6[cd] = str(cd+1) + ' ' + str(cd+1) + ' ' + str(d1) + ' ' + str(l[k][0]) + ' ' + str(l[k][1]) + ' ' + str(l[k][2]) + '\n'
				fo7.append(str(cd+1)+'\n')
				if so != '':
					lso = so.strip().split()
					fo7[cd] = str(cd+1) + ' ' + lso[4] + ' ' + lso[5] + ' ' + lso[6] + '  0.0  #' + so + '\n'
				if so == '': #! mark the unfound
					print ('unfound dihedral ',cd+1,', atomff_type:',s,', atoms number:',l[k][0],l[k][1],l[k][2],d4)
				cd += 1
#! Improper
print ('\n # Now you are searching ff of: impropers\n')
for k in range(ca): #! repeating
	line = l[k][1] + nat
	nele = len(content[line])
	for nag in range(2,nele):
		im4 = int(content[line][nag])
		s = ""
		sr = ""
		if im4 > l[k][0] and im4 > l[k][2]: #! avoid double-counted, s=1234 sr=1324
			s = atomff[l[k][0]-1][1] + atomff[l[k][1]-1][1] + atomff[l[k][2]-1][1] + atomff[im4-1][1]
			sr = atomff[l[k][0]-1][1] + atomff[l[k][2]-1][1] + atomff[l[k][1]-1][1] + atomff[im4-1][1]
			so = ""
			for lnff in range (6606,6733):
				if s != "" and re.search(s, ffinfo[lnff]):
					so = ffinfo[lnff]
				elif sr != "" and re.search(sr, ffinfo[lnff]):
					so = ffinfo[lnff]
			if so == '': #! use the artificial bond info instead
				print ('unfound improper ',ci+1,', atomff_type:',s,', atoms number:',l[k][0],l[k][1],l[k][2],im4)
			fo8.append(ci)
			fo8[ci] = str(ci+1) + ' ' + str(ci+1) + ' ' + str(l[k][0]) + ' ' + str(l[k][1]) + ' ' + str(l[k][2]) + ' ' + str(im4) + '\n'
			fo9.append(str(ci+1) + '\n')
			if so != '':
				lso = so.strip().split()
				fo9[ci] = str(ci+1) + ' ' + lso[4] + ' ' + lso[5] + ' ' + lso[6] + '0.0  #' + so + '\n'
			ci += 1
			

#! Write *.top
ofn = argv[1][:-3] + "top"
print ('# Writing to ' + ofn + ' ... ')
fo = open(ofn, mode='w', encoding='utf-8')

fo.write ("system " + ofn + " created by topobuilder_CHARMM-gen.py \n\n")
fo.write (str(nat) + " atoms\n")
fo.write (str(cb) + " bonds\n")
fo.write (str(ca) + " angles\n")
fo.write (str(cd) + " dihedrals\n")
fo.write (str(ci) + " impropers\n")
fo.write (str(nat) + " atom types\n")
fo.write (str(cb) + " bond types\n")
fo.write (str(ca) + " angle types\n")
fo.write (str(cd) + " dihedral types\n")
fo.write (str(ci) + " improper types\n\n")
fo.write ("0 40.0 xlo xhi\n" + "0 40.0 ylo yhi\n" + "0 40.0 zlo zhi\n\n")
fo.write ("Masses\n\n")
for item in fo0:
	fo.write(item)
fo.write ("\nPair Coeffs\n\n")
for item in fopair:
	fo.write(item)
fo.write ("\nBond Coeffs\n\n")
for item in fo2:
	fo.write(item)
fo.write ("\nAngle Coeffs\n\n")
for item in fo5:
    fo.write(item)
fo.write ("\nDihedral Coeffs\n\n")
for item in fo7:
	fo.write(item)
fo.write ("\nImproper Coeffs\n\n")
for item in fo9:
    fo.write(item)
fo.write ("\nAtoms\n\n")
for item in coor:
	fo.write(item)
fo.write ("\nBonds\n\n")
for item in fo1:
	fo.write(item)
fo.write ("\nAngles\n\n")
for item in fo4:
	fo.write(item)
fo.write ("\nDihedrals\n\n")
for item in fo6:
	fo.write(item)
fo.write ("\nImpropers\n\n")
for item in fo8:
	fo.write(item)

print('# Done! But you need to further enter the lost info of dihedrals and impropers.')

