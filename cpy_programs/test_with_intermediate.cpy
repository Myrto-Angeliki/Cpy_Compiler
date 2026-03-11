#def main
#int i

i = int(input())
if i>5:
    print(5)
elif i>0 and i<5:
    print(2)
elif i>-5 and i<3:
    print(3)
elif i>100 and i<300:
    print(4)
else:
    print(0)


##The expected output for the intermediate code ##
##
0: begin_block, main, _, _ 
1: in, T_0, _, _ 
2: =, T_0, _, i 
3: >, i, 5, 5 
4: jump, _, _, 
5: out, 5, _, _ 
6: jump, _, _, 27 
7: >, i, 0, 9 
8: jump, _, _, 13 
9: <, i, 5, 11 
10: jump, _, _, 13 
11: out, 2, _, _  
12: jump, _, _, 27 
13: -, 0, 5, T_1
14: >, i, T_1, 16
15: jump, _, _, 20
16: <, i, 3, 18
17: jump, _, _, 20
18: out, 3, _, _
19: jump, _, _, 27
20: >, i, 100, 22
21: jump, _, _, 26
22: <, i, 300, 24
23: jump, _, _, 26
24: out, 4, _, _
25: jump, _, _, 27
26: out, 0, _, _
27: halt, _, _, _
28: end_block, main, _, _
##