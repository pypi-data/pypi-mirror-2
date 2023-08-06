g3 1 1 0	# problem unknown
 5 1 1 0 0	# vars, constraints, objectives, general inequalities, equalities
 1 0	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 5 0 0	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0 	# discrete variables: binary, integer, nonlinear (b,c,o)
 5 5	# nonzeros in Jacobian, obj. gradient
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1
C0	#cons1[None]
o0  #+
o2  #*
n61.0
o3 # /
n1
o5  #^
v0 #x[1]
n3 # numeric constant
o0  #+
o2  #*
n37.0
o3 # /
n1
o5  #^
v1 #x[2]
n3 # numeric constant
o0  #+
o2  #*
n19.0
o3 # /
n1
o5  #^
v2 #x[3]
n3 # numeric constant
o0  #+
o2  #*
n7.0
o3 # /
n1
o5  #^
v3 #x[4]
n3 # numeric constant
o3 # /
n1
o5  #^
v4 #x[5]
n3 # numeric constant
O0 0	#f[None]
n0.0
x5
0 1.0 # x[1] initial
1 1.0 # x[2] initial
2 1.0 # x[3] initial
3 1.0 # x[4] initial
4 1.0 # x[5] initial
r
1 1.0  # c0  cons1
b
2 1e-06  # v0  x[1]
2 1e-06  # v1  x[2]
2 1e-06  # v2  x[3]
2 1e-06  # v3  x[4]
2 1e-06  # v4  x[5]
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
G0 5
0   0.0624
1   0.0624
2   0.0624
3   0.0624
4   0.0624
