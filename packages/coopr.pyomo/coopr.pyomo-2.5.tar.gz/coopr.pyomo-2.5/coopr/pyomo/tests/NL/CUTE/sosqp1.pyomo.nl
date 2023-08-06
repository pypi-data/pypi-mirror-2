g3 1 1 0	# problem unknown
 20 11 1 0 11	# vars, constraints, objectives, general inequalities, equalities
 0 1	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 0 20 0	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0 	# discrete variables: binary, integer, nonlinear (b,c,o)
 40 20	# nonzeros in Jacobian, obj. gradient
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
C9	#cons1[10]
n0
C10	#cons2[None]
n0
O0 0	#f[None]
o0  #+
o2  #*
v1 #x[1]
v11 #y[1]
o0  #+
o2  #*
v2 #x[2]
v12 #y[2]
o0  #+
o2  #*
v3 #x[3]
v13 #y[3]
o0  #+
o2  #*
v4 #x[4]
v14 #y[4]
o0  #+
o2  #*
v5 #x[5]
v15 #y[5]
o0  #+
o2  #*
v6 #x[6]
v16 #y[6]
o0  #+
o2  #*
v7 #x[7]
v17 #y[7]
o0  #+
o2  #*
v8 #x[8]
v18 #y[8]
o0  #+
o2  #*
v9 #x[9]
v19 #y[9]
o2  #*
v0 #x[10]
v10 #y[10]
x0
r
4 1.0  # c0  cons1[1]
4 1.0  # c1  cons1[2]
4 1.0  # c2  cons1[3]
4 1.0  # c3  cons1[4]
4 1.0  # c4  cons1[5]
4 1.0  # c5  cons1[6]
4 1.0  # c6  cons1[7]
4 1.0  # c7  cons1[8]
4 1.0  # c8  cons1[9]
4 1.0  # c9  cons1[10]
4 10.0  # c10  cons2
b
0 -1 1  # v0  x[10]
0 -1 1  # v1  x[1]
0 -1 1  # v2  x[2]
0 -1 1  # v3  x[3]
0 -1 1  # v4  x[4]
0 -1 1  # v5  x[5]
0 -1 1  # v6  x[6]
0 -1 1  # v7  x[7]
0 -1 1  # v8  x[8]
0 -1 1  # v9  x[9]
0 -1 1  # v10  y[10]
0 -1 1  # v11  y[1]
0 -1 1  # v12  y[2]
0 -1 1  # v13  y[3]
0 -1 1  # v14  y[4]
0 -1 1  # v15  y[5]
0 -1 1  # v16  y[6]
0 -1 1  # v17  y[7]
0 -1 1  # v18  y[8]
0 -1 1  # v19  y[9]
k19
2
4
6
8
10
12
14
16
18
20
22
24
26
28
30
32
34
36
38
J0 2  #  cons1[1]
1   1.0
11   -1.0
J1 2  #  cons1[2]
2   1.0
12   -1.0
J2 2  #  cons1[3]
3   1.0
13   -1.0
J3 2  #  cons1[4]
4   1.0
14   -1.0
J4 2  #  cons1[5]
5   1.0
15   -1.0
J5 2  #  cons1[6]
6   1.0
16   -1.0
J6 2  #  cons1[7]
7   1.0
17   -1.0
J7 2  #  cons1[8]
8   1.0
18   -1.0
J8 2  #  cons1[9]
9   1.0
19   -1.0
J9 2  #  cons1[10]
0   1.0
10   -1.0
J10 20  #  cons2
0   1.0
1   1.0
2   1.0
3   1.0
4   1.0
5   1.0
6   1.0
7   1.0
8   1.0
9   1.0
10   1.0
11   1.0
12   1.0
13   1.0
14   1.0
15   1.0
16   1.0
17   1.0
18   1.0
19   1.0
G0 20
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
10   0
11   0
12   0
13   0
14   0
15   0
16   0
17   0
18   0
19   0
