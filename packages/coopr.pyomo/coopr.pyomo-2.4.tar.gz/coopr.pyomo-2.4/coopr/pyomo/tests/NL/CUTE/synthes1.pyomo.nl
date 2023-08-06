g3 1 1 0	# problem unknown
 6 6 1 0 0	# vars, constraints, objectives, general inequalities, equalities
 2 1	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 2 2 2	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0 	# discrete variables: binary, integer, nonlinear (b,c,o)
 16 6	# nonzeros in Jacobian, obj. gradient
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1
C0	#l6[None]
n0
C1	#l4[None]
n0
C2	#l5[None]
n0
C3	#l3[None]
n0
C4	#n1[None]
o0  #+
o2  #*
n0.8
o43  #log
o0  #+
n1.0
v1 #x2
o2  #*
n0.96
o43  #log
o0  #+
n1.0
o0  #+
v0 #x1
o2  #*
n-1
v1 #x2
C5	#n2[None]
o0  #+
o43  #log
o0  #+
n1.0
v1 #x2
o2  #*
n1.2
o43  #log
o0  #+
n1.0
o0  #+
v0 #x1
o2  #*
n-1
v1 #x2
O0 0	#obj[None]
o0  #+
n10.0
o0  #+
o2  #*
n-18.0
o43  #log
o0  #+
n1.0
v1 #x2
o2  #*
n-19.2
o43  #log
o0  #+
n1.0
o0  #+
v0 #x1
o2  #*
n-1
v1 #x2
x0
r
1 1.0  # c0  l6
1 0.0  # c1  l4
1 0.0  # c2  l5
1 0.0  # c3  l3
2 0.0  # c4  n1
2 -2.0  # c5  n2
b
0 0.0 2.0  # v0  x1
0 0.0 2.0  # v1  x2
0 0.0 1.0  # v2  x3
0 0.0 1.0  # v3  y1
0 0.0 1.0  # v4  y2
0 0.0 1.0  # v5  y3
k5
4
9
11
13
15
J0 2  #  l6
3   1.0
4   1.0
J1 2  #  l4
1   1.0
3   -2.0
J2 3  #  l5
0   1.0
1   -1.0
4   -2.0
J3 2  #  l3
0   -1.0
1   1.0
J4 3  #  n1
0   0
1   0
2   -0.8
J5 4  #  n2
0   0
1   0
2   -1.0
5   -2.0
G0 6
0   10.0
1   0
2   -7.0
3   5.0
4   6.0
5   8.0
