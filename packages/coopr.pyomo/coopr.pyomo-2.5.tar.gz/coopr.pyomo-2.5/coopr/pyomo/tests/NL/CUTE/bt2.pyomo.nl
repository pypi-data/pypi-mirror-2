g3 1 1 0	# problem unknown
 3 1 1 0 1	# vars, constraints, objectives, general inequalities, equalities
 1 1	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 3 3 3	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0 	# discrete variables: binary, integer, nonlinear (b,c,o)
 3 3	# nonzeros in Jacobian, obj. gradient
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1
C0	#cons1[None]
o0  #+
o2  #*
v0 #x[1]
o0  #+
n1.0
o5  #^
v1 #x[2]
n2 # numeric constant
o5  #^
v2 #x[3]
n4 # numeric constant
O0 0	#f[None]
o0  #+
o5  #^
o0  #+
n-1.0
v0 #x[1]
n2 # numeric constant
o0  #+
o5  #^
o0  #+
v0 #x[1]
o2  #*
n-1
v1 #x[2]
n2 # numeric constant
o5  #^
o0  #+
v1 #x[2]
o2  #*
n-1
v2 #x[3]
n4 # numeric constant
x3
0 10.0 # x[1] initial
1 10.0 # x[2] initial
2 10.0 # x[3] initial
r
4 8.2426407  # c0  cons1
b
3  # v0  x[1]
3  # v1  x[2]
3  # v2  x[3]
k2
1
2
J0 3  #  cons1
0   0
1   0
2   0
G0 3
0   0
1   0
2   0
