g3 1 1 0	# problem unknown
 14 9 1 0 9	# vars, constraints, objectives, general inequalities, equalities
 2 1	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 7 14 7	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0 	# discrete variables: binary, integer, nonlinear (b,c,o)
 21 14	# nonzeros in Jacobian, obj. gradient
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1
C0	#cons1[None]
o0  #+
o46  #cos
v7 #TH[1]
o0  #+
o46  #cos
v8 #TH[2]
o0  #+
o46  #cos
v9 #TH[3]
o0  #+
o46  #cos
v10 #TH[4]
o0  #+
o46  #cos
v11 #TH[5]
o0  #+
o46  #cos
v12 #TH[6]
o2  #*
n0.5
o46  #cos
v13 #TH[7]
C1	#cons2[None]
o0  #+
o41  #sin
v7 #TH[1]
o0  #+
o41  #sin
v8 #TH[2]
o0  #+
o41  #sin
v9 #TH[3]
o0  #+
o41  #sin
v10 #TH[4]
o0  #+
o41  #sin
v11 #TH[5]
o0  #+
o41  #sin
v12 #TH[6]
o2  #*
n0.5
o41  #sin
v13 #TH[7]
C2	#cons3[1]
n0
C3	#cons3[2]
n0
C4	#cons3[3]
n0
C5	#cons3[4]
n0
C6	#cons3[5]
n0
C7	#cons3[6]
n0
C8	#cons3[7]
n0
O0 0	#f[None]
o0  #+
o5  #^
o0  #+
v7 #TH[1]
o2  #*
n-1
v0 #THI[1]
n2 # numeric constant
o0  #+
o5  #^
o0  #+
v8 #TH[2]
o2  #*
n-1
v1 #THI[2]
n2 # numeric constant
o0  #+
o5  #^
o0  #+
v9 #TH[3]
o2  #*
n-1
v2 #THI[3]
n2 # numeric constant
o0  #+
o5  #^
o0  #+
v10 #TH[4]
o2  #*
n-1
v3 #THI[4]
n2 # numeric constant
o0  #+
o5  #^
o0  #+
v11 #TH[5]
o2  #*
n-1
v4 #THI[5]
n2 # numeric constant
o0  #+
o5  #^
o0  #+
v12 #TH[6]
o2  #*
n-1
v5 #THI[6]
n2 # numeric constant
o5  #^
o0  #+
v13 #TH[7]
o2  #*
n-1
v6 #THI[7]
n2 # numeric constant
x0
r
4 4.0  # c0  cons1
4 4.0  # c1  cons2
4 0.0  # c2  cons3[1]
4 0.0  # c3  cons3[2]
4 0.0  # c4  cons3[3]
4 0.0  # c5  cons3[4]
4 0.0  # c6  cons3[5]
4 0.0  # c7  cons3[6]
4 0.0  # c8  cons3[7]
b
3  # v0  THI[1]
3  # v1  THI[2]
3  # v2  THI[3]
3  # v3  THI[4]
3  # v4  THI[5]
3  # v5  THI[6]
3  # v6  THI[7]
3  # v7  TH[1]
3  # v8  TH[2]
3  # v9  TH[3]
3  # v10  TH[4]
3  # v11  TH[5]
3  # v12  TH[6]
3  # v13  TH[7]
k13
1
2
3
4
5
6
7
9
11
13
15
17
19
J0 7  #  cons1
7   0
8   0
9   0
10   0
11   0
12   0
13   0
J1 7  #  cons2
7   0
8   0
9   0
10   0
11   0
12   0
13   0
J2 1  #  cons3[1]
0   1.0
J3 1  #  cons3[2]
1   1.0
J4 1  #  cons3[3]
2   1.0
J5 1  #  cons3[4]
3   1.0
J6 1  #  cons3[5]
4   1.0
J7 1  #  cons3[6]
5   1.0
J8 1  #  cons3[7]
6   1.0
G0 14
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
