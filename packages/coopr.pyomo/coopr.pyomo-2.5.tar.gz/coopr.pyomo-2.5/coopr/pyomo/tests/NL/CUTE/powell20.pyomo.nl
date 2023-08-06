g3 1 1 0	# problem unknown
 10 10 1 0 0	# vars, constraints, objectives, general inequalities, equalities
 0 1	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 0 10 0	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0 	# discrete variables: binary, integer, nonlinear (b,c,o)
 20 10	# nonzeros in Jacobian, obj. gradient
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1
C0	#cons1[1]
n0
C1	#cons1[2]
n0
C2	#cons1[3]
n0
C3	#cons1[4]
n0
C4	#cons1[5]
n0
C5	#cons1[6]
n0
C6	#cons1[7]
n0
C7	#cons1[8]
n0
C8	#cons1[9]
n0
C9	#cons2[None]
n0
O0 0	#f[None]
o0  #+
o2  #*
n0.5
o5  #^
v1 #x[1]
n2 # numeric constant
o0  #+
o2  #*
n0.5
o5  #^
v2 #x[2]
n2 # numeric constant
o0  #+
o2  #*
n0.5
o5  #^
v3 #x[3]
n2 # numeric constant
o0  #+
o2  #*
n0.5
o5  #^
v4 #x[4]
n2 # numeric constant
o0  #+
o2  #*
n0.5
o5  #^
v5 #x[5]
n2 # numeric constant
o0  #+
o2  #*
n0.5
o5  #^
v6 #x[6]
n2 # numeric constant
o0  #+
o2  #*
n0.5
o5  #^
v7 #x[7]
n2 # numeric constant
o0  #+
o2  #*
n0.5
o5  #^
v8 #x[8]
n2 # numeric constant
o0  #+
o2  #*
n0.5
o5  #^
v9 #x[9]
n2 # numeric constant
o2  #*
n0.5
o5  #^
v0 #x[10]
n2 # numeric constant
x10
0 -10.5 # x[10] initial
1 0 # x[1] initial
2 -2.5 # x[2] initial
3 0 # x[3] initial
4 -4.5 # x[4] initial
5 0 # x[5] initial
6 -6.5 # x[6] initial
7 0 # x[7] initial
8 -8.5 # x[8] initial
9 0 # x[9] initial
r
2 -1.5  # c0  cons1[1]
2 1.5  # c1  cons1[2]
2 -3.5  # c2  cons1[3]
2 3.5  # c3  cons1[4]
2 -5.5  # c4  cons1[5]
2 5.5  # c5  cons1[6]
2 -7.5  # c6  cons1[7]
2 7.5  # c7  cons1[8]
2 -9.5  # c8  cons1[9]
2 9.5  # c9  cons2
b
3  # v0  x[10]
3  # v1  x[1]
3  # v2  x[2]
3  # v3  x[3]
3  # v4  x[4]
3  # v5  x[5]
3  # v6  x[6]
3  # v7  x[7]
3  # v8  x[8]
3  # v9  x[9]
k9
2
4
6
8
10
12
14
16
18
J0 2  #  cons1[1]
1   -1.0
2   1.0
J1 2  #  cons1[2]
2   -1.0
3   1.0
J2 2  #  cons1[3]
3   -1.0
4   1.0
J3 2  #  cons1[4]
4   -1.0
5   1.0
J4 2  #  cons1[5]
5   -1.0
6   1.0
J5 2  #  cons1[6]
6   -1.0
7   1.0
J6 2  #  cons1[7]
7   -1.0
8   1.0
J7 2  #  cons1[8]
8   -1.0
9   1.0
J8 2  #  cons1[9]
0   1.0
9   -1.0
J9 2  #  cons2
0   -1.0
1   1.0
G0 10
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
