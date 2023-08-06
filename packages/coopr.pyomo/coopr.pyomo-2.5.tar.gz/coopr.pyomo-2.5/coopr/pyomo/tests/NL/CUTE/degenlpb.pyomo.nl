g3 1 1 0	# problem unknown
 20 15 1 0 15	# vars, constraints, objectives, general inequalities, equalities
 0 0	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 0 0 0	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0 	# discrete variables: binary, integer, nonlinear (b,c,o)
 82 9	# nonzeros in Jacobian, obj. gradient
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1
C0	#cons1[None]
n0
C1	#cons2[None]
n0
C2	#cons3[None]
n0
C3	#cons4[None]
n0
C4	#cons5[None]
n0
C5	#cons6[None]
n0
C6	#cons7[None]
n0
C7	#cons8[None]
n0
C8	#cons9[None]
n0
C9	#cons12[None]
n0
C10	#cons13[None]
n0
C11	#cons10[None]
n0
C12	#cons11[None]
n0
C13	#cons14[None]
n0
C14	#cons15[None]
n0
O0 0	#f[None]
n0.0
x20
0 1.0 # x[10] initial
1 1.0 # x[11] initial
2 1.0 # x[12] initial
3 1.0 # x[13] initial
4 1.0 # x[14] initial
5 1.0 # x[15] initial
6 1.0 # x[16] initial
7 1.0 # x[17] initial
8 1.0 # x[18] initial
9 1.0 # x[19] initial
10 1.0 # x[1] initial
11 1.0 # x[20] initial
12 1.0 # x[2] initial
13 1.0 # x[3] initial
14 1.0 # x[4] initial
15 1.0 # x[5] initial
16 1.0 # x[6] initial
17 1.0 # x[7] initial
18 1.0 # x[8] initial
19 1.0 # x[9] initial
r
4 0.70785  # c0  cons1
4 0.0  # c1  cons2
4 0.0  # c2  cons3
4 0.0  # c3  cons4
4 0.0  # c4  cons5
4 0.0  # c5  cons6
4 0.0  # c6  cons7
4 0.0  # c7  cons8
4 0.0  # c8  cons9
4 0.0  # c9  cons12
4 0.0  # c10  cons13
4 0.0  # c11  cons10
4 0.0  # c12  cons11
4 0.0  # c13  cons14
4 0.0  # c14  cons15
b
0 0.0 1.0  # v0  x[10]
0 0.0 1.0  # v1  x[11]
0 0.0 1.0  # v2  x[12]
0 0.0 1.0  # v3  x[13]
0 0.0 1.0  # v4  x[14]
0 0.0 1.0  # v5  x[15]
0 0.0 1.0  # v6  x[16]
0 0.0 1.0  # v7  x[17]
0 0.0 1.0  # v8  x[18]
0 0.0 1.0  # v9  x[19]
0 0.0 1.0  # v10  x[1]
0 0.0 1.0  # v11  x[20]
0 0.0 1.0  # v12  x[2]
0 0.0 1.0  # v13  x[3]
0 0.0 1.0  # v14  x[4]
0 0.0 1.0  # v15  x[5]
0 0.0 1.0  # v16  x[6]
0 0.0 1.0  # v17  x[7]
0 0.0 1.0  # v18  x[8]
0 0.0 1.0  # v19  x[9]
k19
3
7
12
17
21
25
30
32
34
39
44
46
52
58
64
67
71
75
78
J0 10  #  cons1
0   1.0
10   1.0
12   2.0
13   2.0
14   2.0
15   1.0
16   2.0
17   2.0
18   1.0
19   2.0
J1 5  #  cons2
10   0.326
12   -101.0
15   200.0
16   0.06
17   0.02
J2 5  #  cons3
10   0.0066667
13   -1.03
16   200.0
18   0.06
19   0.02
J3 5  #  cons4
0   0.02
10   0.00066667
14   -1.01
17   200.0
19   0.06
J4 5  #  cons5
1   100.0
2   0.03
3   0.01
12   0.978
15   -201.0
J5 6  #  cons6
2   100.0
4   0.03
5   0.01
12   0.01
13   0.489
16   -101.03
J6 6  #  cons7
3   100.0
5   0.03
6   0.01
12   0.001
14   0.489
17   -101.03
J7 6  #  cons8
5   100.0
8   0.03
9   0.01
13   0.001
14   0.01
19   -1.04
J8 5  #  cons9
4   100.0
7   0.03
9   0.01
13   0.02
18   -1.06
J9 4  #  cons12
1   -0.00257
2   0.25221
4   -6.2
7   1.09
J10 6  #  cons13
1   0.00629
2   -0.20555
3   -4.1106
5   101.04
6   505.1
9   -256.72
J11 5  #  cons10
0   -1.02
6   100.0
9   0.03
11   0.01
14   0.002
J12 4  #  cons11
1   -2.5742e-06
3   0.00252
6   -0.61975
11   1.03
J13 6  #  cons14
2   0.00841
3   -0.08406
4   -0.20667
6   20.658
8   1.07
9   -10.5
J14 4  #  cons15
10   -1.0
12   300.0
13   0.09
14   0.03
G0 9
0   -100.0
12   -0.01
13   -33.333
14   -100.0
15   -0.01
16   -33.343
17   -100.01
18   -33.333
19   -133.33
