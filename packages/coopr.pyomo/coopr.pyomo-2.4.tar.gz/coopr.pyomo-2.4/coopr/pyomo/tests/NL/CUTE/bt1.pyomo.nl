g3 1 1 0	# problem unknown
 2 1 1 0 1	# vars, constraints, objectives, general inequalities, equalities
 1 1	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 2 2 2	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0 	# discrete variables: binary, integer, nonlinear (b,c,o)
 2 2	# nonzeros in Jacobian, obj. gradient
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1
C0	#cons1[None]
o0  #+
o5  #^
v0 #x[1]
n2 # numeric constant
o5  #^
v1 #x[2]
n2 # numeric constant
O0 0	#f[None]
o0  #+
n-100.0
o0  #+
o2  #*
n100
o5  #^
v0 #x[1]
n2 # numeric constant
o2  #*
n100
o5  #^
v1 #x[2]
n2 # numeric constant
x0
r
4 1.0  # c0  cons1
b
3  # v0  x[1]
3  # v1  x[2]
k1
1
J0 2  #  cons1
0   0
1   0
G0 2
0   -1.0
1   0
