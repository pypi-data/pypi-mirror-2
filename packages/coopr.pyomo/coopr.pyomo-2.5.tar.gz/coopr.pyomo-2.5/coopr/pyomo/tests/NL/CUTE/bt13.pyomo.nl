g3 1 1 0	# problem unknown
 5 2 1 0 1	# vars, constraints, objectives, general inequalities, equalities
 1 0	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 5 0 0	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0 	# discrete variables: binary, integer, nonlinear (b,c,o)
 6 1	# nonzeros in Jacobian, obj. gradient
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1
C0	#cons1[None]
o0  #+
o5  #^
v0 #x[1]
n2 # numeric constant
o0  #+
o5  #^
o0  #+
v0 #x[1]
o2  #*
n-2
v1 #x[2]
n2 # numeric constant
o0  #+
o5  #^
o0  #+
v1 #x[2]
o2  #*
n-3
v2 #x[3]
n2 # numeric constant
o0  #+
o5  #^
o0  #+
v2 #x[3]
o2  #*
n-4
v3 #x[4]
n2 # numeric constant
o2  #*
n-1
o5  #^
v4 #x[5]
n2 # numeric constant
C1	#cons2[None]
n0
O0 0	#f[None]
n0
x5
0 1.0 # x[1] initial
1 2.0 # x[2] initial
2 3.0 # x[3] initial
3 3.0 # x[4] initial
4 228.0 # x[5] initial
r
4 0.0  # c0  cons1
2 0  # c1  cons2
b
3  # v0  x[1]
3  # v1  x[2]
3  # v2  x[3]
3  # v3  x[4]
3  # v4  x[5]
k4
1
2
3
4
J0 5  #  cons1
0   0
1   0
2   0
3   0
4   0
J1 1  #  cons2
4   1.0
G0 1
4   1.0
