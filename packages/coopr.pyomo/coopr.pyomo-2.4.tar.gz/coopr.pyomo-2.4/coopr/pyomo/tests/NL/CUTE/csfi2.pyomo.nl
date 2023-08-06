g3 1 1 0	# problem unknown
 5 4 1 0 2	# vars, constraints, objectives, general inequalities, equalities
 4 0	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 4 0 0	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0 	# discrete variables: binary, integer, nonlinear (b,c,o)
 11 1	# nonzeros in Jacobian, obj. gradient
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1
C0	#cons1[None]
o2  #*
n117.370892
o3 # /
v3 #tph
o2  #*
v4 #wid
v2 #thick
C1	#cons2[None]
o2  #*
n0.0208333333333
o2  #*
o5  #^
v2 #thick
n2 # numeric constant
v0 #ipm
C2	#cons3[None]
o3 # /
v4 #wid
v2 #thick
C3	#cons4[None]
o2  #*
v2 #thick
v4 #wid
O0 0	#f[None]
n0
x5
0 0.5 # ipm initial
1 0.5 # len initial
2 0.5 # thick initial
3 0.5 # tph initial
4 0.5 # wid initial
r
4 0.0  # c0  cons1
4 0.0  # c1  cons2
1 2.0  # c2  cons3
1 250.0  # c3  cons4
b
2 0.0  # v0  ipm
2 0.0  # v1  len
2 7.0  # v2  thick
2 45.0  # v3  tph
2 0.0  # v4  wid
k4
2
3
7
8
J0 4  #  cons1
0   -1.0
2   0
3   0
4   0
J1 3  #  cons2
0   0
1   -1.0
2   0
J2 2  #  cons3
2   0
4   0
J3 2  #  cons4
2   0
4   0
G0 1
1   1.0
