g3 1 1 0	# problem unknown
 9 13 1 0 0	# vars, constraints, objectives, general inequalities, equalities
 13 1	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 9 9 9	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0 	# discrete variables: binary, integer, nonlinear (b,c,o)
 39 9	# nonzeros in Jacobian, obj. gradient
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1
C0	#c13[None]
o2 # *
n-1
o2  #*
v4 #x5
v8 #x9
C1	#c9[None]
o0  #+
o2  #*
v6 #x7
v6 #x7
o2  #*
v7 #x8
v8 #x9
C2	#c8[None]
o0  #+
o2  #*
o0  #+
v2 #x3
o2  #*
n-1
v6 #x7
o0  #+
v2 #x3
o2  #*
n-1
v6 #x7
o2  #*
o0  #+
v3 #x4
o2  #*
n-1
v7 #x8
o0  #+
v3 #x4
o2  #*
n-1
v7 #x8
C3	#c1[None]
o0  #+
o2  #*
v2 #x3
v2 #x3
o2  #*
v3 #x4
v3 #x4
C4	#c12[None]
o0  #+
o2  #*
v0 #x1
v3 #x4
o2  #*
n-1
o2  #*
v1 #x2
v2 #x3
C5	#c3[None]
o2  #*
v8 #x9
v8 #x9
C6	#c2[None]
o0  #+
o2  #*
v4 #x5
v4 #x5
o2  #*
v5 #x6
v5 #x6
C7	#c11[None]
o0  #+
o2  #*
v4 #x5
v7 #x8
o2  #*
n-1
o2  #*
v5 #x6
v6 #x7
C8	#c10[None]
o2  #*
v7 #x8
v8 #x9
C9	#c7[None]
o0  #+
o2  #*
o0  #+
v2 #x3
o2  #*
n-1
v4 #x5
o0  #+
v2 #x3
o2  #*
n-1
v4 #x5
o2  #*
o0  #+
v3 #x4
o2  #*
n-1
v5 #x6
o0  #+
v3 #x4
o2  #*
n-1
v5 #x6
C10	#c6[None]
o0  #+
o2  #*
o0  #+
v0 #x1
o2  #*
n-1
v6 #x7
o0  #+
v0 #x1
o2  #*
n-1
v6 #x7
o2  #*
o0  #+
v1 #x2
o2  #*
n-1
v7 #x8
o0  #+
v1 #x2
o2  #*
n-1
v7 #x8
C11	#c5[None]
o0  #+
o2  #*
o0  #+
v0 #x1
o2  #*
n-1
v4 #x5
o0  #+
v0 #x1
o2  #*
n-1
v4 #x5
o2  #*
o0  #+
v1 #x2
o2  #*
n-1
v5 #x6
o0  #+
v1 #x2
o2  #*
n-1
v5 #x6
C12	#c4[None]
o0  #+
o2  #*
v0 #x1
v0 #x1
o2  #*
o0  #+
v1 #x2
o2  #*
n-1
v8 #x9
o0  #+
v1 #x2
o2  #*
n-1
v8 #x9
O0 0	#obj[None]
o0  #+
o2  #*
n-0.5
o2  #*
v0 #x1
v3 #x4
o0  #+
o2  #*
n0.5
o2  #*
v1 #x2
v2 #x3
o0  #+
o2  #*
n-0.5
o2  #*
v2 #x3
v8 #x9
o0  #+
o2  #*
n0.5
o2  #*
v4 #x5
v8 #x9
o0  #+
o2  #*
n-0.5
o2  #*
v4 #x5
v7 #x8
o2  #*
n0.5
o2  #*
v5 #x6
v6 #x7
x9
0 1.0 # x1 initial
1 1.0 # x2 initial
2 1.0 # x3 initial
3 1.0 # x4 initial
4 1.0 # x5 initial
5 1.0 # x6 initial
6 1.0 # x7 initial
7 1.0 # x8 initial
8 1.0 # x9 initial
r
1 0.0  # c0  c13
1 1.0  # c1  c9
1 1.0  # c2  c8
1 1.0  # c3  c1
2 0.0  # c4  c12
1 1.0  # c5  c3
1 1.0  # c6  c2
2 0.0  # c7  c11
2 0.0  # c8  c10
1 1.0  # c9  c7
1 1.0  # c10  c6
1 1.0  # c11  c5
1 1.0  # c12  c4
b
3  # v0  x1
3  # v1  x2
3  # v2  x3
3  # v3  x4
3  # v4  x5
3  # v5  x6
3  # v6  x7
3  # v7  x8
2 0  # v8  x9
k8
4
8
12
16
21
25
29
34
J0 2  #  c13
4   0
8   0
J1 3  #  c9
6   0
7   0
8   0
J2 4  #  c8
2   0
3   0
6   0
7   0
J3 2  #  c1
2   0
3   0
J4 4  #  c12
0   0
1   0
2   0
3   0
J5 1  #  c3
8   0
J6 2  #  c2
4   0
5   0
J7 4  #  c11
4   0
5   0
6   0
7   0
J8 2  #  c10
7   0
8   0
J9 4  #  c7
2   0
3   0
4   0
5   0
J10 4  #  c6
0   0
1   0
6   0
7   0
J11 4  #  c5
0   0
1   0
4   0
5   0
J12 3  #  c4
0   0
1   0
8   0
G0 9
0   0
1   0
2   0
3   0
4   0
5   0
6   0
7   0
8   0
