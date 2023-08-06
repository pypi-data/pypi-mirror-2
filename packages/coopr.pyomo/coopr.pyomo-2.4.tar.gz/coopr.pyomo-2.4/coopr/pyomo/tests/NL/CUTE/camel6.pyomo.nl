g3 1 1 0	# problem unknown
 2 2 1 2 0	# vars, constraints, objectives, general inequalities, equalities
 0 1	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 0 2 0	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0 	# discrete variables: binary, integer, nonlinear (b,c,o)
 2 2	# nonzeros in Jacobian, obj. gradient
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1
C0	#cons1[None]
n0
C1	#cons2[None]
n0
O0 0	#f[None]
o0  #+
o2  #*
n4
o5  #^
v0 #x[1]
n2 # numeric constant
o0  #+
o2  #*
n-2.1
o5  #^
v0 #x[1]
n4 # numeric constant
o0  #+
o2  #*
n0.333333333333
o5  #^
v0 #x[1]
n6 # numeric constant
o0  #+
o2  #*
v0 #x[1]
v1 #x[2]
o0  #+
o2  #*
n-4
o5  #^
v1 #x[2]
n2 # numeric constant
o2  #*
n4
o5  #^
v1 #x[2]
n4 # numeric constant
x2
0 1.1 # x[1] initial
1 1.1 # x[2] initial
r
0 -3.0 3.0  # c0  cons1
0 -1.5 1.5  # c1  cons2
b
3  # v0  x[1]
3  # v1  x[2]
k1
1
J0 1  #  cons1
0   1.0
J1 1  #  cons2
1   1.0
G0 2
0   0
1   0
