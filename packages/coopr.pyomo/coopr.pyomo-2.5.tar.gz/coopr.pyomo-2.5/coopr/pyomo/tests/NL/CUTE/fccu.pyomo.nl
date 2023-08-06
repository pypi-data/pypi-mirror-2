g3 1 1 0	# problem unknown
 19 8 1 0 8	# vars, constraints, objectives, general inequalities, equalities
 0 1	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 0 19 0	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0 	# discrete variables: binary, integer, nonlinear (b,c,o)
 28 19	# nonzeros in Jacobian, obj. gradient
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1
C0	#cons1[None]
n0
C1	#cons2[None]
n0
C2	#cons3[None]
n0
C3	#cons4[None]
n0
C4	#cons5[None]
n0
C5	#cons6[None]
n0
C6	#cons7[None]
n0
C7	#cons8[None]
n0
O0 0	#f[None]
o0  #+
o2  #*
n5.0
o5  #^
o0  #+
n-31
v8 #Feed
n2 # numeric constant
o0  #+
o5  #^
o0  #+
n-36
v7 #Effluent
n2 # numeric constant
o0  #+
o5  #^
o0  #+
n-20
v16 #MF_ohd
n2 # numeric constant
o0  #+
o2  #*
n3.00000003
o5  #^
o0  #+
n-3
v9 #HCN
n2 # numeric constant
o0  #+
o2  #*
n3.00000003
o5  #^
o0  #+
n-5
v12 #LCO
n2 # numeric constant
o0  #+
o2  #*
n3.00000003
o5  #^
o0  #+
n-3.5
v10 #HCO
n2 # numeric constant
o0  #+
o5  #^
o0  #+
n-4.2
v15 #MF_btms
n2 # numeric constant
o0  #+
o5  #^
o0  #+
n-0.9
v6 #Decant
n2 # numeric constant
o0  #+
o5  #^
o0  #+
n-3.9
v5 #Dec_recy
n2 # numeric constant
o0  #+
o5  #^
o0  #+
n-2.2
v17 #Off_gas
n2 # numeric constant
o0  #+
o5  #^
o0  #+
n-22.8
v4 #DC4_feed
n2 # numeric constant
o0  #+
o5  #^
o0  #+
n-6.8
v2 #DC3_feed
n2 # numeric constant
o0  #+
o5  #^
o0  #+
n-19
v3 #DC4_btms
n2 # numeric constant
o0  #+
o5  #^
o0  #+
n-8.5
v13 #Lean_oil
n2 # numeric constant
o0  #+
o2  #*
n3.00000003
o5  #^
o0  #+
n-2.2
v18 #Propane
n2 # numeric constant
o0  #+
o2  #*
n3.00000003
o5  #^
o0  #+
n-2.5
v0 #Butane
n2 # numeric constant
o0  #+
o5  #^
o0  #+
n-10.8
v1 #C8spl_fd
n2 # numeric constant
o0  #+
o2  #*
n3.00000003
o5  #^
o0  #+
n-6.5
v11 #LCN
n2 # numeric constant
o2  #*
n3.00000003
o5  #^
o0  #+
n-6.5
v14 #MCN
n2 # numeric constant
x19
0 1 # Butane initial
1 1 # C8spl_fd initial
2 1 # DC3_feed initial
3 1 # DC4_btms initial
4 1 # DC4_feed initial
5 1 # Dec_recy initial
6 1 # Decant initial
7 1 # Effluent initial
8 1 # Feed initial
9 1 # HCN initial
10 1 # HCO initial
11 1 # LCN initial
12 1 # LCO initial
13 1 # Lean_oil initial
14 1 # MCN initial
15 1 # MF_btms initial
16 1 # MF_ohd initial
17 1 # Off_gas initial
18 1 # Propane initial
r
4 0.0  # c0  cons1
4 0.0  # c1  cons2
4 0.0  # c2  cons3
4 0.0  # c3  cons4
4 0.0  # c4  cons5
4 0.0  # c5  cons6
4 0.0  # c6  cons7
4 0.0  # c7  cons8
b
3  # v0  Butane
3  # v1  C8spl_fd
3  # v2  DC3_feed
3  # v3  DC4_btms
3  # v4  DC4_feed
3  # v5  Dec_recy
3  # v6  Decant
3  # v7  Effluent
3  # v8  Feed
3  # v9  HCN
3  # v10  HCO
3  # v11  LCN
3  # v12  LCO
3  # v13  Lean_oil
3  # v14  MCN
3  # v15  MF_btms
3  # v16  MF_ohd
3  # v17  Off_gas
3  # v18  Propane
k18
1
3
5
7
9
11
12
14
15
16
17
18
19
21
22
24
26
27
J0 3  #  cons1
5   1.0
7   -1.0
8   1.0
J1 6  #  cons2
7   1.0
9   -1.0
10   -1.0
12   -1.0
15   -1.0
16   -1.0
J2 3  #  cons3
5   -1.0
6   -1.0
15   1.0
J3 4  #  cons4
4   -1.0
13   1.0
16   1.0
17   -1.0
J4 3  #  cons5
2   -1.0
3   -1.0
4   1.0
J5 3  #  cons6
1   -1.0
3   1.0
13   -1.0
J6 3  #  cons7
0   -1.0
2   1.0
18   -1.0
J7 3  #  cons8
1   1.0
11   -1.0
14   -1.0
G0 19
0   0
1   0
2   0
3   0
4   0
5   0
6   0
7   0
8   0
9   0
10   0
11   0
12   0
13   0
14   0
15   0
16   0
17   0
18   0
