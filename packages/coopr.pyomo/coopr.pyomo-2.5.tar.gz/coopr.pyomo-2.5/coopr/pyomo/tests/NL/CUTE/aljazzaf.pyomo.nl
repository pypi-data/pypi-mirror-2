g3 1 1 0	# problem unknown
 3 1 1 0 1	# vars, constraints, objectives, general inequalities, equalities
 1 1	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 2 3 2	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0 	# discrete variables: binary, integer, nonlinear (b,c,o)
 3 3	# nonzeros in Jacobian, obj. gradient
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1
C0	#cons1[None]
o0  #+
o2  #*
n5000.5
o5  #^
v1 #x[2]
n2 # numeric constant
o2  #*
n10000.0
o5  #^
o0  #+
n-1.0
v2 #x[3]
n2 # numeric constant
O0 0	#f[None]
o0  #+
o2  #*
n100.0
o5  #^
o0  #+
n-0.5
v0 #x[1]
n2 # numeric constant
o0  #+
o2  #*
n50.005
o5  #^
o0  #+
n1.0
v1 #x[2]
n2 # numeric constant
o2  #*
n0.01
o5  #^
o0  #+
n-1.0
v2 #x[3]
n2 # numeric constant
x3
0 0.0 # x[1] initial
1 0.0 # x[2] initial
2 0.0 # x[3] initial
r
4 -1.0  # c0  cons1
b
2 0  # v0  x[1]
2 0  # v1  x[2]
2 0  # v2  x[3]
k2
1
2
J0 3  #  cons1
0   -1.0
1   0
2   0
G0 3
0   0
1   0
2   0
