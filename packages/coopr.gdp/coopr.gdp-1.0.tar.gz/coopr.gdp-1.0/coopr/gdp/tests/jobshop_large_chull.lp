min 
makespan: 
+1.000000 ms

s.t.

c_e_disj_Q46_(C,E,2)_Q46_t(C)_:
-1.000000 NoClash_Q46_(C,E,2,0)_Q46_t(C)
-1.000000 NoClash_Q46_(C,E,2,1)_Q46_t(C)
+1.000000 t(C)
= 0.0

c_u_NoClash_Q46_(B,F,3,1)_Q46_c_hi_:
+5.000000 NoClash_Q46_(B,F,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,F,3,1)_Q46_t(B)
-1.000000 NoClash_Q46_(B,F,3,1)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(B,D,3,0)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(B,D,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,D,3,0)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(A,E,5,1)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(A,E,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,E,5,1)_Q46_t(E)
<= 0.0

c_e_disj_Q46_(A,B,5)_Q46_t(B)_:
-1.000000 NoClash_Q46_(A,B,5,0)_Q46_t(B)
-1.000000 NoClash_Q46_(A,B,5,1)_Q46_t(B)
+1.000000 t(B)
= 0.0

c_u_NoClash_Q46_(B,G,5,1)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,G,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,G,5,1)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(D,G,2,1)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(D,G,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,G,2,1)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(A,E,5,1)_Q46_c_hi_:
+1.000000 NoClash_Q46_(A,E,5,1)_Q46_t(A)
-1.000000 NoClash_Q46_(A,E,5,1)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(B,F,3,0)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(B,F,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,F,3,0)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(E,F,3,1)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(E,F,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,F,3,1)_Q46_t(E)
<= 0.0

c_e_disj_Q46_(C,G,4)_Q46_t(C)_:
-1.000000 NoClash_Q46_(C,G,4,0)_Q46_t(C)
-1.000000 NoClash_Q46_(C,G,4,1)_Q46_t(C)
+1.000000 t(C)
= 0.0

c_u_NoClash_Q46_(A,C,1,0)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,C,1,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,C,1,0)_Q46_t(A)
<= 0.0

c_e_disj(A,B,3)_:
+1.000000 NoClash_Q46_(A,B,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,B,3,1)_Q46_indicator_var
= 1.0

c_e_disj(A,B,5)_:
+1.000000 NoClash_Q46_(A,B,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,B,5,1)_Q46_indicator_var
= 1.0

c_e_disj(A,C,1)_:
+1.000000 NoClash_Q46_(A,C,1,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,C,1,1)_Q46_indicator_var
= 1.0

c_e_disj(A,D,3)_:
+1.000000 NoClash_Q46_(A,D,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,D,3,1)_Q46_indicator_var
= 1.0

c_e_disj(A,E,3)_:
+1.000000 NoClash_Q46_(A,E,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,E,3,1)_Q46_indicator_var
= 1.0

c_e_disj(A,E,5)_:
+1.000000 NoClash_Q46_(A,E,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,E,5,1)_Q46_indicator_var
= 1.0

c_e_disj(A,F,1)_:
+1.000000 NoClash_Q46_(A,F,1,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,F,1,1)_Q46_indicator_var
= 1.0

c_e_disj(A,F,3)_:
+1.000000 NoClash_Q46_(A,F,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,F,3,1)_Q46_indicator_var
= 1.0

c_e_disj(A,G,5)_:
+1.000000 NoClash_Q46_(A,G,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,G,5,1)_Q46_indicator_var
= 1.0

c_e_disj(B,C,2)_:
+1.000000 NoClash_Q46_(B,C,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,C,2,1)_Q46_indicator_var
= 1.0

c_e_disj(B,D,2)_:
+1.000000 NoClash_Q46_(B,D,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,D,2,1)_Q46_indicator_var
= 1.0

c_e_disj(B,D,3)_:
+1.000000 NoClash_Q46_(B,D,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,D,3,1)_Q46_indicator_var
= 1.0

c_e_disj(B,E,2)_:
+1.000000 NoClash_Q46_(B,E,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,2,1)_Q46_indicator_var
= 1.0

c_e_disj(B,E,3)_:
+1.000000 NoClash_Q46_(B,E,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,3,1)_Q46_indicator_var
= 1.0

c_e_disj(B,E,5)_:
+1.000000 NoClash_Q46_(B,E,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,5,1)_Q46_indicator_var
= 1.0

c_e_disj(B,F,3)_:
+1.000000 NoClash_Q46_(B,F,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,F,3,1)_Q46_indicator_var
= 1.0

c_e_disj(B,G,2)_:
+1.000000 NoClash_Q46_(B,G,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,G,2,1)_Q46_indicator_var
= 1.0

c_e_disj(B,G,5)_:
+1.000000 NoClash_Q46_(B,G,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,G,5,1)_Q46_indicator_var
= 1.0

c_e_disj(C,D,2)_:
+1.000000 NoClash_Q46_(C,D,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,D,2,1)_Q46_indicator_var
= 1.0

c_e_disj(C,D,4)_:
+1.000000 NoClash_Q46_(C,D,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,D,4,1)_Q46_indicator_var
= 1.0

c_e_disj(C,E,2)_:
+1.000000 NoClash_Q46_(C,E,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,E,2,1)_Q46_indicator_var
= 1.0

c_e_disj(C,F,1)_:
+1.000000 NoClash_Q46_(C,F,1,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,F,1,1)_Q46_indicator_var
= 1.0

c_e_disj(C,F,4)_:
+1.000000 NoClash_Q46_(C,F,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,F,4,1)_Q46_indicator_var
= 1.0

c_e_disj(C,G,2)_:
+1.000000 NoClash_Q46_(C,G,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,G,2,1)_Q46_indicator_var
= 1.0

c_e_disj(C,G,4)_:
+1.000000 NoClash_Q46_(C,G,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,G,4,1)_Q46_indicator_var
= 1.0

c_e_disj(D,E,2)_:
+1.000000 NoClash_Q46_(D,E,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,E,2,1)_Q46_indicator_var
= 1.0

c_e_disj(D,E,3)_:
+1.000000 NoClash_Q46_(D,E,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,E,3,1)_Q46_indicator_var
= 1.0

c_e_disj(D,F,3)_:
+1.000000 NoClash_Q46_(D,F,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,F,3,1)_Q46_indicator_var
= 1.0

c_e_disj(D,F,4)_:
+1.000000 NoClash_Q46_(D,F,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,F,4,1)_Q46_indicator_var
= 1.0

c_e_disj(D,G,2)_:
+1.000000 NoClash_Q46_(D,G,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,G,2,1)_Q46_indicator_var
= 1.0

c_e_disj(D,G,4)_:
+1.000000 NoClash_Q46_(D,G,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,G,4,1)_Q46_indicator_var
= 1.0

c_e_disj(E,F,3)_:
+1.000000 NoClash_Q46_(E,F,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,F,3,1)_Q46_indicator_var
= 1.0

c_e_disj(E,G,2)_:
+1.000000 NoClash_Q46_(E,G,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,G,2,1)_Q46_indicator_var
= 1.0

c_e_disj(E,G,5)_:
+1.000000 NoClash_Q46_(E,G,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,G,5,1)_Q46_indicator_var
= 1.0

c_e_disj(F,G,4)_:
+1.000000 NoClash_Q46_(F,G,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(F,G,4,1)_Q46_indicator_var
= 1.0

c_e_disj_Q46_(A,E,5)_Q46_t(E)_:
-1.000000 NoClash_Q46_(A,E,5,0)_Q46_t(E)
-1.000000 NoClash_Q46_(A,E,5,1)_Q46_t(E)
+1.000000 t(E)
= 0.0

c_u_NoClash_Q46_(B,D,3,1)_Q46_c_hi_:
-1.000000 NoClash_Q46_(B,D,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,D,3,1)_Q46_t(B)
-1.000000 NoClash_Q46_(B,D,3,1)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(A,B,5,1)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(A,B,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,B,5,1)_Q46_t(B)
<= 0.0

c_e_disj_Q46_(D,G,4)_Q46_t(D)_:
-1.000000 NoClash_Q46_(D,G,4,0)_Q46_t(D)
-1.000000 NoClash_Q46_(D,G,4,1)_Q46_t(D)
+1.000000 t(D)
= 0.0

c_u_NoClash_Q46_(D,F,4,1)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(D,F,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,F,4,1)_Q46_t(D)
<= 0.0

c_e_disj_Q46_(C,F,4)_Q46_t(C)_:
-1.000000 NoClash_Q46_(C,F,4,0)_Q46_t(C)
-1.000000 NoClash_Q46_(C,F,4,1)_Q46_t(C)
+1.000000 t(C)
= 0.0

c_u_NoClash_Q46_(A,E,5,0)_Q46_c_hi_:
+4.000000 NoClash_Q46_(A,E,5,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(A,E,5,0)_Q46_t(A)
+1.000000 NoClash_Q46_(A,E,5,0)_Q46_t(E)
<= 0.0

c_e_disj_Q46_(F,G,4)_Q46_t(F)_:
-1.000000 NoClash_Q46_(F,G,4,0)_Q46_t(F)
-1.000000 NoClash_Q46_(F,G,4,1)_Q46_t(F)
+1.000000 t(F)
= 0.0

c_u_NoClash_Q46_(B,G,5,1)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(B,G,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,G,5,1)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(C,F,4,0)_Q46_c_hi_:
+5.000000 NoClash_Q46_(C,F,4,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(C,F,4,0)_Q46_t(C)
+1.000000 NoClash_Q46_(C,F,4,0)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(A,E,3,0)_Q46_c_hi_:
+7.000000 NoClash_Q46_(A,E,3,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(A,E,3,0)_Q46_t(A)
+1.000000 NoClash_Q46_(A,E,3,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(E,F,3,0)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(E,F,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,F,3,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(A,B,5,1)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,B,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,B,5,1)_Q46_t(A)
<= 0.0

c_u_NoClash_Q46_(B,E,2,1)_Q46_c_hi_:
+3.000000 NoClash_Q46_(B,E,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,2,1)_Q46_t(B)
-1.000000 NoClash_Q46_(B,E,2,1)_Q46_t(E)
<= 0.0

c_e_disj_Q46_(D,F,4)_Q46_t(D)_:
-1.000000 NoClash_Q46_(D,F,4,0)_Q46_t(D)
-1.000000 NoClash_Q46_(D,F,4,1)_Q46_t(D)
+1.000000 t(D)
= 0.0

c_u_NoClash_Q46_(D,F,3,0)_Q46_c_hi_:
-1.000000 NoClash_Q46_(D,F,3,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(D,F,3,0)_Q46_t(D)
+1.000000 NoClash_Q46_(D,F,3,0)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(B,F,3,0)_Q46_c_hi_:
+4.000000 NoClash_Q46_(B,F,3,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(B,F,3,0)_Q46_t(B)
+1.000000 NoClash_Q46_(B,F,3,0)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(B,G,5,0)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,G,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,G,5,0)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(D,G,4,1)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(D,G,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,G,4,1)_Q46_t(G)
<= 0.0

c_e_disj_Q46_(D,E,3)_Q46_t(E)_:
-1.000000 NoClash_Q46_(D,E,3,0)_Q46_t(E)
-1.000000 NoClash_Q46_(D,E,3,1)_Q46_t(E)
+1.000000 t(E)
= 0.0

c_u_NoClash_Q46_(C,F,1,0)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(C,F,1,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,F,1,0)_Q46_t(F)
<= 0.0

c_e_disj_Q46_(A,B,3)_Q46_t(A)_:
-1.000000 NoClash_Q46_(A,B,3,0)_Q46_t(A)
-1.000000 NoClash_Q46_(A,B,3,1)_Q46_t(A)
+1.000000 t(A)
= 0.0

c_u_NoClash_Q46_(B,G,2,1)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(B,G,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,G,2,1)_Q46_t(G)
<= 0.0

c_e_disj_Q46_(E,F,3)_Q46_t(F)_:
-1.000000 NoClash_Q46_(E,F,3,0)_Q46_t(F)
-1.000000 NoClash_Q46_(E,F,3,1)_Q46_t(F)
+1.000000 t(F)
= 0.0

c_e_disj_Q46_(A,F,1)_Q46_t(A)_:
-1.000000 NoClash_Q46_(A,F,1,0)_Q46_t(A)
-1.000000 NoClash_Q46_(A,F,1,1)_Q46_t(A)
+1.000000 t(A)
= 0.0

c_e_disj_Q46_(A,C,1)_Q46_t(C)_:
-1.000000 NoClash_Q46_(A,C,1,0)_Q46_t(C)
-1.000000 NoClash_Q46_(A,C,1,1)_Q46_t(C)
+1.000000 t(C)
= 0.0

c_u_NoClash_Q46_(C,F,1,1)_Q46_c_hi_:
+6.000000 NoClash_Q46_(C,F,1,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,F,1,1)_Q46_t(C)
-1.000000 NoClash_Q46_(C,F,1,1)_Q46_t(F)
<= 0.0

c_e_disj_Q46_(A,E,3)_Q46_t(A)_:
-1.000000 NoClash_Q46_(A,E,3,0)_Q46_t(A)
-1.000000 NoClash_Q46_(A,E,3,1)_Q46_t(A)
+1.000000 t(A)
= 0.0

c_u_NoClash_Q46_(A,E,5,0)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(A,E,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,E,5,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(D,E,2,0)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(D,E,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,E,2,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(C,E,2,0)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(C,E,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,E,2,0)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(E,G,2,1)_Q46_c_hi_:
+4.000000 NoClash_Q46_(E,G,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,G,2,1)_Q46_t(E)
-1.000000 NoClash_Q46_(E,G,2,1)_Q46_t(G)
<= 0.0

c_e_disj_Q46_(A,B,3)_Q46_t(B)_:
-1.000000 NoClash_Q46_(A,B,3,0)_Q46_t(B)
-1.000000 NoClash_Q46_(A,B,3,1)_Q46_t(B)
+1.000000 t(B)
= 0.0

c_u_NoClash_Q46_(A,B,5,1)_Q46_c_hi_:
+3.000000 NoClash_Q46_(A,B,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,B,5,1)_Q46_t(A)
-1.000000 NoClash_Q46_(A,B,5,1)_Q46_t(B)
<= 0.0

c_e_disj_Q46_(C,F,1)_Q46_t(C)_:
-1.000000 NoClash_Q46_(C,F,1,0)_Q46_t(C)
-1.000000 NoClash_Q46_(C,F,1,1)_Q46_t(C)
+1.000000 t(C)
= 0.0

c_u_NoClash_Q46_(A,B,3,0)_Q46_c_hi_:
+4.000000 NoClash_Q46_(A,B,3,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(A,B,3,0)_Q46_t(A)
+1.000000 NoClash_Q46_(A,B,3,0)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(B,E,5,1)_Q46_c_hi_:
+1.000000 NoClash_Q46_(B,E,5,1)_Q46_t(B)
-1.000000 NoClash_Q46_(B,E,5,1)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(C,E,2,1)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(C,E,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,E,2,1)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(A,B,5,0)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,B,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,B,5,0)_Q46_t(A)
<= 0.0

c_e_disj_Q46_(D,G,2)_Q46_t(D)_:
-1.000000 NoClash_Q46_(D,G,2,0)_Q46_t(D)
-1.000000 NoClash_Q46_(D,G,2,1)_Q46_t(D)
+1.000000 t(D)
= 0.0

c_e_disj_Q46_(A,G,5)_Q46_t(A)_:
-1.000000 NoClash_Q46_(A,G,5,0)_Q46_t(A)
-1.000000 NoClash_Q46_(A,G,5,1)_Q46_t(A)
+1.000000 t(A)
= 0.0

c_e_disj_Q46_(C,G,2)_Q46_t(G)_:
-1.000000 NoClash_Q46_(C,G,2,0)_Q46_t(G)
-1.000000 NoClash_Q46_(C,G,2,1)_Q46_t(G)
+1.000000 t(G)
= 0.0

c_u_NoClash_Q46_(A,B,3,1)_Q46_c_hi_:
+5.000000 NoClash_Q46_(A,B,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,B,3,1)_Q46_t(A)
-1.000000 NoClash_Q46_(A,B,3,1)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(A,G,5,1)_Q46_c_hi_:
-3.000000 NoClash_Q46_(A,G,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,G,5,1)_Q46_t(A)
-1.000000 NoClash_Q46_(A,G,5,1)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(A,F,1,1)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(A,F,1,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,F,1,1)_Q46_t(F)
<= 0.0

c_e_disj_Q46_(B,E,5)_Q46_t(E)_:
-1.000000 NoClash_Q46_(B,E,5,0)_Q46_t(E)
-1.000000 NoClash_Q46_(B,E,5,1)_Q46_t(E)
+1.000000 t(E)
= 0.0

c_u_NoClash_Q46_(D,E,2,1)_Q46_c_hi_:
+8.000000 NoClash_Q46_(D,E,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,E,2,1)_Q46_t(D)
-1.000000 NoClash_Q46_(D,E,2,1)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(B,E,5,0)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(B,E,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,5,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(B,G,2,0)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(B,G,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,G,2,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(A,F,3,1)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(A,F,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,F,3,1)_Q46_t(F)
<= 0.0

c_u_Feas(A)_:
-1.000000 ms
+1.000000 t(A)
<= -10

c_u_Feas(B)_:
-1.000000 ms
+1.000000 t(B)
<= -10

c_u_Feas(C)_:
-1.000000 ms
+1.000000 t(C)
<= -15

c_u_Feas(D)_:
-1.000000 ms
+1.000000 t(D)
<= -14

c_u_Feas(E)_:
-1.000000 ms
+1.000000 t(E)
<= -12

c_u_Feas(F)_:
-1.000000 ms
+1.000000 t(F)
<= -14

c_u_Feas(G)_:
-1.000000 ms
+1.000000 t(G)
<= -17

c_e_disj_Q46_(D,F,3)_Q46_t(F)_:
-1.000000 NoClash_Q46_(D,F,3,0)_Q46_t(F)
-1.000000 NoClash_Q46_(D,F,3,1)_Q46_t(F)
+1.000000 t(F)
= 0.0

c_u_NoClash_Q46_(A,F,3,0)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,F,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,F,3,0)_Q46_t(A)
<= 0.0

c_e_disj_Q46_(B,F,3)_Q46_t(F)_:
-1.000000 NoClash_Q46_(B,F,3,0)_Q46_t(F)
-1.000000 NoClash_Q46_(B,F,3,1)_Q46_t(F)
+1.000000 t(F)
= 0.0

c_u_NoClash_Q46_(D,G,4,0)_Q46_c_hi_:
-1.000000 NoClash_Q46_(D,G,4,0)_Q46_t(D)
+1.000000 NoClash_Q46_(D,G,4,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(B,C,2,1)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(B,C,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,C,2,1)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(D,G,2,0)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(D,G,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,G,2,0)_Q46_t(G)
<= 0.0

c_e_disj_Q46_(C,F,4)_Q46_t(F)_:
-1.000000 NoClash_Q46_(C,F,4,0)_Q46_t(F)
-1.000000 NoClash_Q46_(C,F,4,1)_Q46_t(F)
+1.000000 t(F)
= 0.0

c_u_NoClash_Q46_(C,G,2,0)_Q46_c_hi_:
+2.000000 NoClash_Q46_(C,G,2,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(C,G,2,0)_Q46_t(C)
+1.000000 NoClash_Q46_(C,G,2,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(B,D,2,1)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(B,D,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,D,2,1)_Q46_t(D)
<= 0.0

c_e_disj_Q46_(D,G,4)_Q46_t(G)_:
-1.000000 NoClash_Q46_(D,G,4,0)_Q46_t(G)
-1.000000 NoClash_Q46_(D,G,4,1)_Q46_t(G)
+1.000000 t(G)
= 0.0

c_u_NoClash_Q46_(C,D,4,0)_Q46_c_hi_:
+5.000000 NoClash_Q46_(C,D,4,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(C,D,4,0)_Q46_t(C)
+1.000000 NoClash_Q46_(C,D,4,0)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(C,D,4,1)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(C,D,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,D,4,1)_Q46_t(D)
<= 0.0

c_e_disj_Q46_(B,D,3)_Q46_t(D)_:
-1.000000 NoClash_Q46_(B,D,3,0)_Q46_t(D)
-1.000000 NoClash_Q46_(B,D,3,1)_Q46_t(D)
+1.000000 t(D)
= 0.0

c_u_NoClash_Q46_(B,F,3,1)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(B,F,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,F,3,1)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(C,D,4,1)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(C,D,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,D,4,1)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(D,E,3,1)_Q46_c_hi_:
+9.000000 NoClash_Q46_(D,E,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,E,3,1)_Q46_t(D)
-1.000000 NoClash_Q46_(D,E,3,1)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(E,F,3,1)_Q46_c_hi_:
+8.000000 NoClash_Q46_(E,F,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,F,3,1)_Q46_t(E)
-1.000000 NoClash_Q46_(E,F,3,1)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(A,F,3,0)_Q46_c_hi_:
+4.000000 NoClash_Q46_(A,F,3,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(A,F,3,0)_Q46_t(A)
+1.000000 NoClash_Q46_(A,F,3,0)_Q46_t(F)
<= 0.0

c_e_disj_Q46_(B,E,3)_Q46_t(E)_:
-1.000000 NoClash_Q46_(B,E,3,0)_Q46_t(E)
-1.000000 NoClash_Q46_(B,E,3,1)_Q46_t(E)
+1.000000 t(E)
= 0.0

c_u_NoClash_Q46_(A,C,1,0)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(A,C,1,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,C,1,0)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(D,G,4,1)_Q46_c_hi_:
+6.000000 NoClash_Q46_(D,G,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,G,4,1)_Q46_t(D)
-1.000000 NoClash_Q46_(D,G,4,1)_Q46_t(G)
<= 0.0

c_e_disj_Q46_(A,F,3)_Q46_t(A)_:
-1.000000 NoClash_Q46_(A,F,3,0)_Q46_t(A)
-1.000000 NoClash_Q46_(A,F,3,1)_Q46_t(A)
+1.000000 t(A)
= 0.0

c_u_NoClash_Q46_(A,D,3,1)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(A,D,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,D,3,1)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(B,F,3,1)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,F,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,F,3,1)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(A,B,5,0)_Q46_c_hi_:
+2.000000 NoClash_Q46_(A,B,5,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(A,B,5,0)_Q46_t(A)
+1.000000 NoClash_Q46_(A,B,5,0)_Q46_t(B)
<= 0.0

c_e_disj_Q46_(D,E,2)_Q46_t(E)_:
-1.000000 NoClash_Q46_(D,E,2,0)_Q46_t(E)
-1.000000 NoClash_Q46_(D,E,2,1)_Q46_t(E)
+1.000000 t(E)
= 0.0

c_u_NoClash_Q46_(C,G,2,1)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(C,G,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,G,2,1)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(D,F,4,1)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(D,F,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,F,4,1)_Q46_t(F)
<= 0.0

c_e_disj_Q46_(B,E,5)_Q46_t(B)_:
-1.000000 NoClash_Q46_(B,E,5,0)_Q46_t(B)
-1.000000 NoClash_Q46_(B,E,5,1)_Q46_t(B)
+1.000000 t(B)
= 0.0

c_u_NoClash_Q46_(A,C,1,1)_Q46_c_hi_:
+3.000000 NoClash_Q46_(A,C,1,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,C,1,1)_Q46_t(A)
-1.000000 NoClash_Q46_(A,C,1,1)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(A,D,3,0)_Q46_c_hi_:
+10.000000 NoClash_Q46_(A,D,3,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(A,D,3,0)_Q46_t(A)
+1.000000 NoClash_Q46_(A,D,3,0)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(A,D,3,1)_Q46_c_hi_:
+1.000000 NoClash_Q46_(A,D,3,1)_Q46_t(A)
-1.000000 NoClash_Q46_(A,D,3,1)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(B,G,2,0)_Q46_c_hi_:
+8.000000 NoClash_Q46_(B,G,2,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(B,G,2,0)_Q46_t(B)
+1.000000 NoClash_Q46_(B,G,2,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(C,G,2,0)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(C,G,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,G,2,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(C,G,4,1)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(C,G,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,G,4,1)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(C,G,2,1)_Q46_c_hi_:
+9.000000 NoClash_Q46_(C,G,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,G,2,1)_Q46_t(C)
-1.000000 NoClash_Q46_(C,G,2,1)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(C,E,2,1)_Q46_c_hi_:
+9.000000 NoClash_Q46_(C,E,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,E,2,1)_Q46_t(C)
-1.000000 NoClash_Q46_(C,E,2,1)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(B,C,2,1)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,C,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,C,2,1)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(A,C,1,0)_Q46_c_hi_:
+6.000000 NoClash_Q46_(A,C,1,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(A,C,1,0)_Q46_t(A)
+1.000000 NoClash_Q46_(A,C,1,0)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(B,E,5,0)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,E,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,5,0)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(A,D,3,1)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,D,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,D,3,1)_Q46_t(A)
<= 0.0

c_u_NoClash_Q46_(C,F,4,0)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(C,F,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,F,4,0)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(C,F,4,1)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(C,F,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,F,4,1)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(E,G,5,1)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(E,G,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,G,5,1)_Q46_t(E)
<= 0.0

c_e_disj_Q46_(B,G,5)_Q46_t(B)_:
-1.000000 NoClash_Q46_(B,G,5,0)_Q46_t(B)
-1.000000 NoClash_Q46_(B,G,5,1)_Q46_t(B)
+1.000000 t(B)
= 0.0

c_u_NoClash_Q46_(D,G,4,0)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(D,G,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,G,4,0)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(C,G,4,1)_Q46_c_hi_:
+7.000000 NoClash_Q46_(C,G,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,G,4,1)_Q46_t(C)
-1.000000 NoClash_Q46_(C,G,4,1)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(B,D,2,0)_Q46_c_hi_:
+8.000000 NoClash_Q46_(B,D,2,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(B,D,2,0)_Q46_t(B)
+1.000000 NoClash_Q46_(B,D,2,0)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(E,F,3,0)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(E,F,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,F,3,0)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(B,E,3,1)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,E,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,3,1)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(B,G,2,1)_Q46_c_hi_:
+3.000000 NoClash_Q46_(B,G,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,G,2,1)_Q46_t(B)
-1.000000 NoClash_Q46_(B,G,2,1)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(B,E,2,1)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(B,E,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,2,1)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(E,G,5,0)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(E,G,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,G,5,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(A,F,1,1)_Q46_c_hi_:
+3.000000 NoClash_Q46_(A,F,1,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,F,1,1)_Q46_t(A)
-1.000000 NoClash_Q46_(A,F,1,1)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(D,F,3,1)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(D,F,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,F,3,1)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(A,B,3,1)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(A,B,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,B,3,1)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(D,G,2,1)_Q46_c_hi_:
+8.000000 NoClash_Q46_(D,G,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,G,2,1)_Q46_t(D)
-1.000000 NoClash_Q46_(D,G,2,1)_Q46_t(G)
<= 0.0

c_e_disj_Q46_(B,E,3)_Q46_t(B)_:
-1.000000 NoClash_Q46_(B,E,3,0)_Q46_t(B)
-1.000000 NoClash_Q46_(B,E,3,1)_Q46_t(B)
+1.000000 t(B)
= 0.0

c_u_NoClash_Q46_(A,D,3,0)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,D,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,D,3,0)_Q46_t(A)
<= 0.0

c_e_disj_Q46_(B,G,2)_Q46_t(B)_:
-1.000000 NoClash_Q46_(B,G,2,0)_Q46_t(B)
-1.000000 NoClash_Q46_(B,G,2,1)_Q46_t(B)
+1.000000 t(B)
= 0.0

c_u_NoClash_Q46_(A,E,3,0)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,E,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,E,3,0)_Q46_t(A)
<= 0.0

c_e_disj_Q46_(D,E,2)_Q46_t(D)_:
-1.000000 NoClash_Q46_(D,E,2,0)_Q46_t(D)
-1.000000 NoClash_Q46_(D,E,2,1)_Q46_t(D)
+1.000000 t(D)
= 0.0

c_u_NoClash_Q46_(A,F,3,0)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(A,F,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,F,3,0)_Q46_t(F)
<= 0.0

c_e_disj_Q46_(E,G,2)_Q46_t(E)_:
-1.000000 NoClash_Q46_(E,G,2,0)_Q46_t(E)
-1.000000 NoClash_Q46_(E,G,2,1)_Q46_t(E)
+1.000000 t(E)
= 0.0

c_u_NoClash_Q46_(B,E,3,1)_Q46_c_hi_:
+3.000000 NoClash_Q46_(B,E,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,3,1)_Q46_t(B)
-1.000000 NoClash_Q46_(B,E,3,1)_Q46_t(E)
<= 0.0

c_e_disj_Q46_(F,G,4)_Q46_t(G)_:
-1.000000 NoClash_Q46_(F,G,4,0)_Q46_t(G)
-1.000000 NoClash_Q46_(F,G,4,1)_Q46_t(G)
+1.000000 t(G)
= 0.0

c_e_disj_Q46_(B,E,2)_Q46_t(E)_:
-1.000000 NoClash_Q46_(B,E,2,0)_Q46_t(E)
-1.000000 NoClash_Q46_(B,E,2,1)_Q46_t(E)
+1.000000 t(E)
= 0.0

c_u_NoClash_Q46_(D,G,2,0)_Q46_c_hi_:
+8.000000 NoClash_Q46_(D,G,2,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(D,G,2,0)_Q46_t(D)
+1.000000 NoClash_Q46_(D,G,2,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(E,G,2,0)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(E,G,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,G,2,0)_Q46_t(G)
<= 0.0

c_e_disj_Q46_(A,B,5)_Q46_t(A)_:
-1.000000 NoClash_Q46_(A,B,5,0)_Q46_t(A)
-1.000000 NoClash_Q46_(A,B,5,1)_Q46_t(A)
+1.000000 t(A)
= 0.0

c_u_NoClash_Q46_(B,D,3,1)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,D,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,D,3,1)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(B,G,5,0)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(B,G,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,G,5,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(C,F,1,1)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(C,F,1,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,F,1,1)_Q46_t(C)
<= 0.0

c_e_disj_Q46_(A,F,1)_Q46_t(F)_:
-1.000000 NoClash_Q46_(A,F,1,0)_Q46_t(F)
-1.000000 NoClash_Q46_(A,F,1,1)_Q46_t(F)
+1.000000 t(F)
= 0.0

c_u_NoClash_Q46_(D,E,2,1)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(D,E,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,E,2,1)_Q46_t(E)
<= 0.0

c_e_disj_Q46_(D,E,3)_Q46_t(D)_:
-1.000000 NoClash_Q46_(D,E,3,0)_Q46_t(D)
-1.000000 NoClash_Q46_(D,E,3,1)_Q46_t(D)
+1.000000 t(D)
= 0.0

c_e_disj_Q46_(E,G,2)_Q46_t(G)_:
-1.000000 NoClash_Q46_(E,G,2,0)_Q46_t(G)
-1.000000 NoClash_Q46_(E,G,2,1)_Q46_t(G)
+1.000000 t(G)
= 0.0

c_u_NoClash_Q46_(D,G,2,1)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(D,G,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,G,2,1)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(E,G,5,1)_Q46_c_hi_:
-1.000000 NoClash_Q46_(E,G,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,G,5,1)_Q46_t(E)
-1.000000 NoClash_Q46_(E,G,5,1)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(D,G,4,0)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(D,G,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,G,4,0)_Q46_t(G)
<= 0.0

c_e_disj_Q46_(C,G,4)_Q46_t(G)_:
-1.000000 NoClash_Q46_(C,G,4,0)_Q46_t(G)
-1.000000 NoClash_Q46_(C,G,4,1)_Q46_t(G)
+1.000000 t(G)
= 0.0

c_u_NoClash_Q46_(B,G,5,0)_Q46_c_hi_:
+10.000000 NoClash_Q46_(B,G,5,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(B,G,5,0)_Q46_t(B)
+1.000000 NoClash_Q46_(B,G,5,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(E,F,3,1)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(E,F,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,F,3,1)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(D,F,4,0)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(D,F,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,F,4,0)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(E,G,5,0)_Q46_c_hi_:
+7.000000 NoClash_Q46_(E,G,5,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(E,G,5,0)_Q46_t(E)
+1.000000 NoClash_Q46_(E,G,5,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(B,C,2,1)_Q46_c_hi_:
-3.000000 NoClash_Q46_(B,C,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,C,2,1)_Q46_t(B)
-1.000000 NoClash_Q46_(B,C,2,1)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(B,E,2,0)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,E,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,2,0)_Q46_t(B)
<= 0.0

c_e_disj_Q46_(E,F,3)_Q46_t(E)_:
-1.000000 NoClash_Q46_(E,F,3,0)_Q46_t(E)
-1.000000 NoClash_Q46_(E,F,3,1)_Q46_t(E)
+1.000000 t(E)
= 0.0

c_e_disj_Q46_(B,D,2)_Q46_t(B)_:
-1.000000 NoClash_Q46_(B,D,2,0)_Q46_t(B)
-1.000000 NoClash_Q46_(B,D,2,1)_Q46_t(B)
+1.000000 t(B)
= 0.0

c_u_NoClash_Q46_(D,E,2,1)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(D,E,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,E,2,1)_Q46_t(D)
<= 0.0

c_e_disj_Q46_(A,E,5)_Q46_t(A)_:
-1.000000 NoClash_Q46_(A,E,5,0)_Q46_t(A)
-1.000000 NoClash_Q46_(A,E,5,1)_Q46_t(A)
+1.000000 t(A)
= 0.0

c_u_NoClash_Q46_(C,F,4,1)_Q46_c_hi_:
+8.000000 NoClash_Q46_(C,F,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,F,4,1)_Q46_t(C)
-1.000000 NoClash_Q46_(C,F,4,1)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(C,D,4,0)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(C,D,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,D,4,0)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(A,E,3,1)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,E,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,E,3,1)_Q46_t(A)
<= 0.0

c_u_NoClash_Q46_(B,E,3,0)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,E,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,3,0)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(D,E,3,1)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(D,E,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,E,3,1)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(C,G,4,0)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(C,G,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,G,4,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(D,E,3,0)_Q46_c_hi_:
+2.000000 NoClash_Q46_(D,E,3,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(D,E,3,0)_Q46_t(D)
+1.000000 NoClash_Q46_(D,E,3,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(A,F,1,0)_Q46_c_hi_:
+2.000000 NoClash_Q46_(A,F,1,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(A,F,1,0)_Q46_t(A)
+1.000000 NoClash_Q46_(A,F,1,0)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(C,G,4,0)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(C,G,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,G,4,0)_Q46_t(C)
<= 0.0

c_e_disj_Q46_(C,F,1)_Q46_t(F)_:
-1.000000 NoClash_Q46_(C,F,1,0)_Q46_t(F)
-1.000000 NoClash_Q46_(C,F,1,1)_Q46_t(F)
+1.000000 t(F)
= 0.0

c_e_disj_Q46_(C,D,4)_Q46_t(D)_:
-1.000000 NoClash_Q46_(C,D,4,0)_Q46_t(D)
-1.000000 NoClash_Q46_(C,D,4,1)_Q46_t(D)
+1.000000 t(D)
= 0.0

c_u_NoClash_Q46_(A,B,3,0)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(A,B,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,B,3,0)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(F,G,4,0)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(F,G,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(F,G,4,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(D,F,4,1)_Q46_c_hi_:
+7.000000 NoClash_Q46_(D,F,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,F,4,1)_Q46_t(D)
-1.000000 NoClash_Q46_(D,F,4,1)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(B,D,2,1)_Q46_c_hi_:
+3.000000 NoClash_Q46_(B,D,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,D,2,1)_Q46_t(B)
-1.000000 NoClash_Q46_(B,D,2,1)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(A,F,3,1)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,F,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,F,3,1)_Q46_t(A)
<= 0.0

c_u_NoClash_Q46_(B,E,2,0)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(B,E,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,2,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(C,D,2,1)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(C,D,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,D,2,1)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(B,E,3,1)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(B,E,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,3,1)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(A,E,3,1)_Q46_c_hi_:
+4.000000 NoClash_Q46_(A,E,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,E,3,1)_Q46_t(A)
-1.000000 NoClash_Q46_(A,E,3,1)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(D,F,4,0)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(D,F,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,F,4,0)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(B,E,5,0)_Q46_c_hi_:
+5.000000 NoClash_Q46_(B,E,5,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(B,E,5,0)_Q46_t(B)
+1.000000 NoClash_Q46_(B,E,5,0)_Q46_t(E)
<= 0.0

c_e_disj_Q46_(A,E,3)_Q46_t(E)_:
-1.000000 NoClash_Q46_(A,E,3,0)_Q46_t(E)
-1.000000 NoClash_Q46_(A,E,3,1)_Q46_t(E)
+1.000000 t(E)
= 0.0

c_u_NoClash_Q46_(A,C,1,1)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,C,1,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,C,1,1)_Q46_t(A)
<= 0.0

c_u_NoClash_Q46_(C,G,4,0)_Q46_c_hi_:
+4.000000 NoClash_Q46_(C,G,4,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(C,G,4,0)_Q46_t(C)
+1.000000 NoClash_Q46_(C,G,4,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(D,F,3,0)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(D,F,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,F,3,0)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(C,E,2,0)_Q46_c_hi_:
-2.000000 NoClash_Q46_(C,E,2,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(C,E,2,0)_Q46_t(C)
+1.000000 NoClash_Q46_(C,E,2,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(C,D,4,1)_Q46_c_hi_:
+2.000000 NoClash_Q46_(C,D,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,D,4,1)_Q46_t(C)
-1.000000 NoClash_Q46_(C,D,4,1)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(E,F,3,0)_Q46_c_hi_:
+3.000000 NoClash_Q46_(E,F,3,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(E,F,3,0)_Q46_t(E)
+1.000000 NoClash_Q46_(E,F,3,0)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(D,F,3,1)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(D,F,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,F,3,1)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(C,G,2,0)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(C,G,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,G,2,0)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(C,G,2,1)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(C,G,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,G,2,1)_Q46_t(C)
<= 0.0

c_e_disj_Q46_(C,G,2)_Q46_t(C)_:
-1.000000 NoClash_Q46_(C,G,2,0)_Q46_t(C)
-1.000000 NoClash_Q46_(C,G,2,1)_Q46_t(C)
+1.000000 t(C)
= 0.0

c_e_disj_Q46_(E,G,5)_Q46_t(G)_:
-1.000000 NoClash_Q46_(E,G,5,0)_Q46_t(G)
-1.000000 NoClash_Q46_(E,G,5,1)_Q46_t(G)
+1.000000 t(G)
= 0.0

c_u_NoClash_Q46_(C,D,2,0)_Q46_c_hi_:
+2.000000 NoClash_Q46_(C,D,2,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(C,D,2,0)_Q46_t(C)
+1.000000 NoClash_Q46_(C,D,2,0)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(D,F,3,1)_Q46_c_hi_:
+11.000000 NoClash_Q46_(D,F,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,F,3,1)_Q46_t(D)
-1.000000 NoClash_Q46_(D,F,3,1)_Q46_t(F)
<= 0.0

c_e_disj_Q46_(B,C,2)_Q46_t(C)_:
-1.000000 NoClash_Q46_(B,C,2,0)_Q46_t(C)
-1.000000 NoClash_Q46_(B,C,2,1)_Q46_t(C)
+1.000000 t(C)
= 0.0

c_u_NoClash_Q46_(A,G,5,0)_Q46_c_hi_:
+9.000000 NoClash_Q46_(A,G,5,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(A,G,5,0)_Q46_t(A)
+1.000000 NoClash_Q46_(A,G,5,0)_Q46_t(G)
<= 0.0

c_e_disj_Q46_(B,F,3)_Q46_t(B)_:
-1.000000 NoClash_Q46_(B,F,3,0)_Q46_t(B)
-1.000000 NoClash_Q46_(B,F,3,1)_Q46_t(B)
+1.000000 t(B)
= 0.0

c_u_NoClash_Q46_(C,D,2,0)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(C,D,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,D,2,0)_Q46_t(C)
<= 0.0

c_e_disj_Q46_(B,E,2)_Q46_t(B)_:
-1.000000 NoClash_Q46_(B,E,2,0)_Q46_t(B)
-1.000000 NoClash_Q46_(B,E,2,1)_Q46_t(B)
+1.000000 t(B)
= 0.0

c_e_disj_Q46_(C,D,2)_Q46_t(D)_:
-1.000000 NoClash_Q46_(C,D,2,0)_Q46_t(D)
-1.000000 NoClash_Q46_(C,D,2,1)_Q46_t(D)
+1.000000 t(D)
= 0.0

c_u_NoClash_Q46_(F,G,4,1)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(F,G,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(F,G,4,1)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(A,F,1,0)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,F,1,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,F,1,0)_Q46_t(A)
<= 0.0

c_u_NoClash_Q46_(B,G,2,1)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,G,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,G,2,1)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(C,D,4,0)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(C,D,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,D,4,0)_Q46_t(C)
<= 0.0

c_e_disj_Q46_(C,D,4)_Q46_t(C)_:
-1.000000 NoClash_Q46_(C,D,4,0)_Q46_t(C)
-1.000000 NoClash_Q46_(C,D,4,1)_Q46_t(C)
+1.000000 t(C)
= 0.0

c_u_NoClash_Q46_(A,B,5,0)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(A,B,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,B,5,0)_Q46_t(B)
<= 0.0

c_e_disj_Q46_(B,D,3)_Q46_t(B)_:
-1.000000 NoClash_Q46_(B,D,3,0)_Q46_t(B)
-1.000000 NoClash_Q46_(B,D,3,1)_Q46_t(B)
+1.000000 t(B)
= 0.0

c_u_NoClash_Q46_(E,G,2,1)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(E,G,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,G,2,1)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(B,D,3,0)_Q46_c_hi_:
+10.000000 NoClash_Q46_(B,D,3,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(B,D,3,0)_Q46_t(B)
+1.000000 NoClash_Q46_(B,D,3,0)_Q46_t(D)
<= 0.0

c_e_disj_Q46_(E,G,5)_Q46_t(E)_:
-1.000000 NoClash_Q46_(E,G,5,0)_Q46_t(E)
-1.000000 NoClash_Q46_(E,G,5,1)_Q46_t(E)
+1.000000 t(E)
= 0.0

c_u_NoClash_Q46_(B,C,2,0)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,C,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,C,2,0)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(B,E,3,0)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(B,E,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,3,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(B,E,3,0)_Q46_c_hi_:
+7.000000 NoClash_Q46_(B,E,3,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(B,E,3,0)_Q46_t(B)
+1.000000 NoClash_Q46_(B,E,3,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(A,B,3,0)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,B,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,B,3,0)_Q46_t(A)
<= 0.0

c_u_NoClash_Q46_(C,F,1,1)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(C,F,1,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,F,1,1)_Q46_t(F)
<= 0.0

c_e_disj_Q46_(B,D,2)_Q46_t(D)_:
-1.000000 NoClash_Q46_(B,D,2,0)_Q46_t(D)
-1.000000 NoClash_Q46_(B,D,2,1)_Q46_t(D)
+1.000000 t(D)
= 0.0

c_u_NoClash_Q46_(E,G,5,1)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(E,G,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,G,5,1)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(F,G,4,1)_Q46_c_hi_:
+6.000000 NoClash_Q46_(F,G,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(F,G,4,1)_Q46_t(F)
-1.000000 NoClash_Q46_(F,G,4,1)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(B,G,2,0)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,G,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,G,2,0)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(C,F,4,1)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(C,F,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,F,4,1)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(B,G,5,1)_Q46_c_hi_:
-3.000000 NoClash_Q46_(B,G,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,G,5,1)_Q46_t(B)
-1.000000 NoClash_Q46_(B,G,5,1)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(A,G,5,0)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(A,G,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,G,5,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(C,E,2,0)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(C,E,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,E,2,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(A,G,5,0)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,G,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,G,5,0)_Q46_t(A)
<= 0.0

c_u_NoClash_Q46_(E,G,2,0)_Q46_c_hi_:
+8.000000 NoClash_Q46_(E,G,2,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(E,G,2,0)_Q46_t(E)
+1.000000 NoClash_Q46_(E,G,2,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(A,B,3,1)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,B,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,B,3,1)_Q46_t(A)
<= 0.0

c_u_NoClash_Q46_(A,F,1,0)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(A,F,1,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,F,1,0)_Q46_t(F)
<= 0.0

c_e_disj_Q46_(C,D,2)_Q46_t(C)_:
-1.000000 NoClash_Q46_(C,D,2,0)_Q46_t(C)
-1.000000 NoClash_Q46_(C,D,2,1)_Q46_t(C)
+1.000000 t(C)
= 0.0

c_u_NoClash_Q46_(B,D,2,0)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,D,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,D,2,0)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(B,E,5,1)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,E,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,5,1)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(B,E,2,1)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,E,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,2,1)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(E,G,2,0)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(E,G,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,G,2,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(A,G,5,1)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(A,G,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,G,5,1)_Q46_t(G)
<= 0.0

c_e_disj_Q46_(D,G,2)_Q46_t(G)_:
-1.000000 NoClash_Q46_(D,G,2,0)_Q46_t(G)
-1.000000 NoClash_Q46_(D,G,2,1)_Q46_t(G)
+1.000000 t(G)
= 0.0

c_u_NoClash_Q46_(D,G,2,0)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(D,G,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,G,2,0)_Q46_t(D)
<= 0.0

c_e_disj_Q46_(B,G,2)_Q46_t(G)_:
-1.000000 NoClash_Q46_(B,G,2,0)_Q46_t(G)
-1.000000 NoClash_Q46_(B,G,2,1)_Q46_t(G)
+1.000000 t(G)
= 0.0

c_u_NoClash_Q46_(F,G,4,1)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(F,G,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(F,G,4,1)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(A,F,1,1)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,F,1,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,F,1,1)_Q46_t(A)
<= 0.0

c_u_NoClash_Q46_(D,E,3,0)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(D,E,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,E,3,0)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(B,D,3,0)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,D,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,D,3,0)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(D,G,4,1)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(D,G,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,G,4,1)_Q46_t(D)
<= 0.0

c_e_disj_Q46_(A,F,3)_Q46_t(F)_:
-1.000000 NoClash_Q46_(A,F,3,0)_Q46_t(F)
-1.000000 NoClash_Q46_(A,F,3,1)_Q46_t(F)
+1.000000 t(F)
= 0.0

c_u_NoClash_Q46_(B,D,3,1)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(B,D,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,D,3,1)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(C,D,2,0)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(C,D,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,D,2,0)_Q46_t(D)
<= 0.0

c_e_disj_Q46_(B,G,5)_Q46_t(G)_:
-1.000000 NoClash_Q46_(B,G,5,0)_Q46_t(G)
-1.000000 NoClash_Q46_(B,G,5,1)_Q46_t(G)
+1.000000 t(G)
= 0.0

c_u_NoClash_Q46_(E,G,2,1)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(E,G,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,G,2,1)_Q46_t(G)
<= 0.0

c_e_disj_Q46_(D,F,4)_Q46_t(F)_:
-1.000000 NoClash_Q46_(D,F,4,0)_Q46_t(F)
-1.000000 NoClash_Q46_(D,F,4,1)_Q46_t(F)
+1.000000 t(F)
= 0.0

c_u_NoClash_Q46_(B,F,3,0)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,F,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,F,3,0)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(A,C,1,1)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(A,C,1,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,C,1,1)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(F,G,4,0)_Q46_c_hi_:
+6.000000 NoClash_Q46_(F,G,4,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(F,G,4,0)_Q46_t(F)
+1.000000 NoClash_Q46_(F,G,4,0)_Q46_t(G)
<= 0.0

c_u_NoClash_Q46_(B,C,2,0)_Q46_c_hi_:
+9.000000 NoClash_Q46_(B,C,2,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(B,C,2,0)_Q46_t(B)
+1.000000 NoClash_Q46_(B,C,2,0)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(A,D,3,0)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(A,D,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,D,3,0)_Q46_t(D)
<= 0.0

c_e_disj_Q46_(C,E,2)_Q46_t(E)_:
-1.000000 NoClash_Q46_(C,E,2,0)_Q46_t(E)
-1.000000 NoClash_Q46_(C,E,2,1)_Q46_t(E)
+1.000000 t(E)
= 0.0

c_u_NoClash_Q46_(A,E,3,0)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(A,E,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,E,3,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(A,E,3,1)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(A,E,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,E,3,1)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(B,C,2,0)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(B,C,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,C,2,0)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(D,E,3,0)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(D,E,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,E,3,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(F,G,4,0)_Q46_t(F)_hi_:
-92.000000 NoClash_Q46_(F,G,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(F,G,4,0)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(C,G,4,1)_Q46_t(G)_hi_:
-92.000000 NoClash_Q46_(C,G,4,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,G,4,1)_Q46_t(G)
<= 0.0

c_e_disj_Q46_(B,C,2)_Q46_t(B)_:
-1.000000 NoClash_Q46_(B,C,2,0)_Q46_t(B)
-1.000000 NoClash_Q46_(B,C,2,1)_Q46_t(B)
+1.000000 t(B)
= 0.0

c_u_NoClash_Q46_(C,F,4,0)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(C,F,4,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,F,4,0)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(C,D,2,1)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(C,D,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,D,2,1)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(D,E,2,0)_Q46_c_hi_:
+4.000000 NoClash_Q46_(D,E,2,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(D,E,2,0)_Q46_t(D)
+1.000000 NoClash_Q46_(D,E,2,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(A,F,3,1)_Q46_c_hi_:
+6.000000 NoClash_Q46_(A,F,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,F,3,1)_Q46_t(A)
-1.000000 NoClash_Q46_(A,F,3,1)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(D,E,3,1)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(D,E,3,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,E,3,1)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(B,E,5,1)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(B,E,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,E,5,1)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(C,F,1,0)_Q46_t(C)_hi_:
-92.000000 NoClash_Q46_(C,F,1,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,F,1,0)_Q46_t(C)
<= 0.0

c_u_NoClash_Q46_(D,E,2,0)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(D,E,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,E,2,0)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(C,F,1,0)_Q46_c_hi_:
+2.000000 NoClash_Q46_(C,F,1,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(C,F,1,0)_Q46_t(C)
+1.000000 NoClash_Q46_(C,F,1,0)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(E,G,5,0)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(E,G,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(E,G,5,0)_Q46_t(E)
<= 0.0

c_e_disj_Q46_(D,F,3)_Q46_t(D)_:
-1.000000 NoClash_Q46_(D,F,3,0)_Q46_t(D)
-1.000000 NoClash_Q46_(D,F,3,1)_Q46_t(D)
+1.000000 t(D)
= 0.0

c_u_NoClash_Q46_(B,D,2,0)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(B,D,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,D,2,0)_Q46_t(D)
<= 0.0

c_e_disj_Q46_(A,G,5)_Q46_t(G)_:
-1.000000 NoClash_Q46_(A,G,5,0)_Q46_t(G)
-1.000000 NoClash_Q46_(A,G,5,1)_Q46_t(G)
+1.000000 t(G)
= 0.0

c_e_disj_Q46_(A,D,3)_Q46_t(A)_:
-1.000000 NoClash_Q46_(A,D,3,0)_Q46_t(A)
-1.000000 NoClash_Q46_(A,D,3,1)_Q46_t(A)
+1.000000 t(A)
= 0.0

c_u_NoClash_Q46_(A,E,5,0)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,E,5,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,E,5,0)_Q46_t(A)
<= 0.0

c_u_NoClash_Q46_(D,F,4,0)_Q46_c_hi_:
+1.000000 NoClash_Q46_(D,F,4,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(D,F,4,0)_Q46_t(D)
+1.000000 NoClash_Q46_(D,F,4,0)_Q46_t(F)
<= 0.0

c_u_NoClash_Q46_(A,G,5,1)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,G,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,G,5,1)_Q46_t(A)
<= 0.0

c_u_NoClash_Q46_(B,D,2,1)_Q46_t(B)_hi_:
-92.000000 NoClash_Q46_(B,D,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,D,2,1)_Q46_t(B)
<= 0.0

c_u_NoClash_Q46_(A,E,5,1)_Q46_t(A)_hi_:
-92.000000 NoClash_Q46_(A,E,5,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,E,5,1)_Q46_t(A)
<= 0.0

c_u_NoClash_Q46_(D,F,3,0)_Q46_t(D)_hi_:
-92.000000 NoClash_Q46_(D,F,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(D,F,3,0)_Q46_t(D)
<= 0.0

c_u_NoClash_Q46_(C,E,2,1)_Q46_t(E)_hi_:
-92.000000 NoClash_Q46_(C,E,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,E,2,1)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(B,E,2,0)_Q46_c_hi_:
+4.000000 NoClash_Q46_(B,E,2,0)_Q46_indicator_var
-1.000000 NoClash_Q46_(B,E,2,0)_Q46_t(B)
+1.000000 NoClash_Q46_(B,E,2,0)_Q46_t(E)
<= 0.0

c_u_NoClash_Q46_(C,D,2,1)_Q46_c_hi_:
+9.000000 NoClash_Q46_(C,D,2,1)_Q46_indicator_var
+1.000000 NoClash_Q46_(C,D,2,1)_Q46_t(C)
-1.000000 NoClash_Q46_(C,D,2,1)_Q46_t(D)
<= 0.0

c_e_disj_Q46_(A,C,1)_Q46_t(A)_:
-1.000000 NoClash_Q46_(A,C,1,0)_Q46_t(A)
-1.000000 NoClash_Q46_(A,C,1,1)_Q46_t(A)
+1.000000 t(A)
= 0.0

c_e_disj_Q46_(A,D,3)_Q46_t(D)_:
-1.000000 NoClash_Q46_(A,D,3,0)_Q46_t(D)
-1.000000 NoClash_Q46_(A,D,3,1)_Q46_t(D)
+1.000000 t(D)
= 0.0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds 
    0 <=  NoClash_Q46_(A,B,3,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,B,3,0)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,B,3,0)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(A,B,3,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,B,3,1)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,B,3,1)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(A,B,5,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,B,5,0)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,B,5,0)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(A,B,5,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,B,5,1)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,B,5,1)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(A,C,1,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,C,1,0)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,C,1,0)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(A,C,1,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,C,1,1)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,C,1,1)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(A,D,3,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,D,3,0)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,D,3,0)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(A,D,3,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,D,3,1)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,D,3,1)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(A,E,3,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,E,3,0)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,E,3,0)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(A,E,3,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,E,3,1)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,E,3,1)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(A,E,5,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,E,5,0)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,E,5,0)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(A,E,5,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,E,5,1)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,E,5,1)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(A,F,1,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,F,1,0)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,F,1,0)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(A,F,1,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,F,1,1)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,F,1,1)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(A,F,3,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,F,3,0)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,F,3,0)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(A,F,3,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,F,3,1)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,F,3,1)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(A,G,5,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,G,5,0)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,G,5,0)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(A,G,5,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,G,5,1)_Q46_t(A)  <= 92
    0 <=  NoClash_Q46_(A,G,5,1)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(B,C,2,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,C,2,0)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,C,2,0)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(B,C,2,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,C,2,1)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,C,2,1)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(B,D,2,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,D,2,0)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,D,2,0)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(B,D,2,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,D,2,1)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,D,2,1)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(B,D,3,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,D,3,0)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,D,3,0)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(B,D,3,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,D,3,1)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,D,3,1)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(B,E,2,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,E,2,0)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,E,2,0)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(B,E,2,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,E,2,1)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,E,2,1)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(B,E,3,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,E,3,0)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,E,3,0)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(B,E,3,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,E,3,1)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,E,3,1)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(B,E,5,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,E,5,0)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,E,5,0)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(B,E,5,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,E,5,1)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,E,5,1)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(B,F,3,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,F,3,0)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,F,3,0)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(B,F,3,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,F,3,1)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,F,3,1)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(B,G,2,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,G,2,0)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,G,2,0)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(B,G,2,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,G,2,1)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,G,2,1)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(B,G,5,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,G,5,0)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,G,5,0)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(B,G,5,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,G,5,1)_Q46_t(B)  <= 92
    0 <=  NoClash_Q46_(B,G,5,1)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(C,D,2,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(C,D,2,0)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(C,D,2,0)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(C,D,2,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(C,D,2,1)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(C,D,2,1)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(C,D,4,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(C,D,4,0)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(C,D,4,0)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(C,D,4,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(C,D,4,1)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(C,D,4,1)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(C,E,2,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(C,E,2,0)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(C,E,2,0)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(C,E,2,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(C,E,2,1)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(C,E,2,1)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(C,F,1,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(C,F,1,0)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(C,F,1,0)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(C,F,1,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(C,F,1,1)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(C,F,1,1)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(C,F,4,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(C,F,4,0)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(C,F,4,0)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(C,F,4,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(C,F,4,1)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(C,F,4,1)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(C,G,2,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(C,G,2,0)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(C,G,2,0)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(C,G,2,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(C,G,2,1)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(C,G,2,1)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(C,G,4,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(C,G,4,0)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(C,G,4,0)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(C,G,4,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(C,G,4,1)_Q46_t(C)  <= 92
    0 <=  NoClash_Q46_(C,G,4,1)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(D,E,2,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(D,E,2,0)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(D,E,2,0)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(D,E,2,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(D,E,2,1)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(D,E,2,1)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(D,E,3,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(D,E,3,0)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(D,E,3,0)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(D,E,3,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(D,E,3,1)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(D,E,3,1)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(D,F,3,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(D,F,3,0)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(D,F,3,0)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(D,F,3,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(D,F,3,1)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(D,F,3,1)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(D,F,4,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(D,F,4,0)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(D,F,4,0)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(D,F,4,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(D,F,4,1)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(D,F,4,1)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(D,G,2,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(D,G,2,0)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(D,G,2,0)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(D,G,2,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(D,G,2,1)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(D,G,2,1)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(D,G,4,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(D,G,4,0)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(D,G,4,0)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(D,G,4,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(D,G,4,1)_Q46_t(D)  <= 92
    0 <=  NoClash_Q46_(D,G,4,1)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(E,F,3,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(E,F,3,0)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(E,F,3,0)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(E,F,3,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(E,F,3,1)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(E,F,3,1)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(E,G,2,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(E,G,2,0)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(E,G,2,0)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(E,G,2,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(E,G,2,1)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(E,G,2,1)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(E,G,5,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(E,G,5,0)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(E,G,5,0)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(E,G,5,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(E,G,5,1)_Q46_t(E)  <= 92
    0 <=  NoClash_Q46_(E,G,5,1)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(F,G,4,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(F,G,4,0)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(F,G,4,0)_Q46_t(G)  <= 92
    0 <=  NoClash_Q46_(F,G,4,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(F,G,4,1)_Q46_t(F)  <= 92
    0 <=  NoClash_Q46_(F,G,4,1)_Q46_t(G)  <= 92
     -inf <=  ms  <= +inf
    0 <=  t(A)  <= 92
    0 <=  t(B)  <= 92
    0 <=  t(C)  <= 92
    0 <=  t(D)  <= 92
    0 <=  t(E)  <= 92
    0 <=  t(F)  <= 92
    0 <=  t(G)  <= 92
binary
  NoClash_Q46_(A,B,3,0)_Q46_indicator_var
  NoClash_Q46_(A,B,3,1)_Q46_indicator_var
  NoClash_Q46_(A,B,5,0)_Q46_indicator_var
  NoClash_Q46_(A,B,5,1)_Q46_indicator_var
  NoClash_Q46_(A,C,1,0)_Q46_indicator_var
  NoClash_Q46_(A,C,1,1)_Q46_indicator_var
  NoClash_Q46_(A,D,3,0)_Q46_indicator_var
  NoClash_Q46_(A,D,3,1)_Q46_indicator_var
  NoClash_Q46_(A,E,3,0)_Q46_indicator_var
  NoClash_Q46_(A,E,3,1)_Q46_indicator_var
  NoClash_Q46_(A,E,5,0)_Q46_indicator_var
  NoClash_Q46_(A,E,5,1)_Q46_indicator_var
  NoClash_Q46_(A,F,1,0)_Q46_indicator_var
  NoClash_Q46_(A,F,1,1)_Q46_indicator_var
  NoClash_Q46_(A,F,3,0)_Q46_indicator_var
  NoClash_Q46_(A,F,3,1)_Q46_indicator_var
  NoClash_Q46_(A,G,5,0)_Q46_indicator_var
  NoClash_Q46_(A,G,5,1)_Q46_indicator_var
  NoClash_Q46_(B,C,2,0)_Q46_indicator_var
  NoClash_Q46_(B,C,2,1)_Q46_indicator_var
  NoClash_Q46_(B,D,2,0)_Q46_indicator_var
  NoClash_Q46_(B,D,2,1)_Q46_indicator_var
  NoClash_Q46_(B,D,3,0)_Q46_indicator_var
  NoClash_Q46_(B,D,3,1)_Q46_indicator_var
  NoClash_Q46_(B,E,2,0)_Q46_indicator_var
  NoClash_Q46_(B,E,2,1)_Q46_indicator_var
  NoClash_Q46_(B,E,3,0)_Q46_indicator_var
  NoClash_Q46_(B,E,3,1)_Q46_indicator_var
  NoClash_Q46_(B,E,5,0)_Q46_indicator_var
  NoClash_Q46_(B,E,5,1)_Q46_indicator_var
  NoClash_Q46_(B,F,3,0)_Q46_indicator_var
  NoClash_Q46_(B,F,3,1)_Q46_indicator_var
  NoClash_Q46_(B,G,2,0)_Q46_indicator_var
  NoClash_Q46_(B,G,2,1)_Q46_indicator_var
  NoClash_Q46_(B,G,5,0)_Q46_indicator_var
  NoClash_Q46_(B,G,5,1)_Q46_indicator_var
  NoClash_Q46_(C,D,2,0)_Q46_indicator_var
  NoClash_Q46_(C,D,2,1)_Q46_indicator_var
  NoClash_Q46_(C,D,4,0)_Q46_indicator_var
  NoClash_Q46_(C,D,4,1)_Q46_indicator_var
  NoClash_Q46_(C,E,2,0)_Q46_indicator_var
  NoClash_Q46_(C,E,2,1)_Q46_indicator_var
  NoClash_Q46_(C,F,1,0)_Q46_indicator_var
  NoClash_Q46_(C,F,1,1)_Q46_indicator_var
  NoClash_Q46_(C,F,4,0)_Q46_indicator_var
  NoClash_Q46_(C,F,4,1)_Q46_indicator_var
  NoClash_Q46_(C,G,2,0)_Q46_indicator_var
  NoClash_Q46_(C,G,2,1)_Q46_indicator_var
  NoClash_Q46_(C,G,4,0)_Q46_indicator_var
  NoClash_Q46_(C,G,4,1)_Q46_indicator_var
  NoClash_Q46_(D,E,2,0)_Q46_indicator_var
  NoClash_Q46_(D,E,2,1)_Q46_indicator_var
  NoClash_Q46_(D,E,3,0)_Q46_indicator_var
  NoClash_Q46_(D,E,3,1)_Q46_indicator_var
  NoClash_Q46_(D,F,3,0)_Q46_indicator_var
  NoClash_Q46_(D,F,3,1)_Q46_indicator_var
  NoClash_Q46_(D,F,4,0)_Q46_indicator_var
  NoClash_Q46_(D,F,4,1)_Q46_indicator_var
  NoClash_Q46_(D,G,2,0)_Q46_indicator_var
  NoClash_Q46_(D,G,2,1)_Q46_indicator_var
  NoClash_Q46_(D,G,4,0)_Q46_indicator_var
  NoClash_Q46_(D,G,4,1)_Q46_indicator_var
  NoClash_Q46_(E,F,3,0)_Q46_indicator_var
  NoClash_Q46_(E,F,3,1)_Q46_indicator_var
  NoClash_Q46_(E,G,2,0)_Q46_indicator_var
  NoClash_Q46_(E,G,2,1)_Q46_indicator_var
  NoClash_Q46_(E,G,5,0)_Q46_indicator_var
  NoClash_Q46_(E,G,5,1)_Q46_indicator_var
  NoClash_Q46_(F,G,4,0)_Q46_indicator_var
  NoClash_Q46_(F,G,4,1)_Q46_indicator_var
end 
