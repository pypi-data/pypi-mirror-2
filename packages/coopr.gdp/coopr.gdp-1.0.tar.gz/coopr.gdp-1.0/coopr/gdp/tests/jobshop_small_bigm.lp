min 
makespan: 
+1.000000 ms

s.t.

c_u_NoClash_Q46_(A,B,3,0)_Q46_c_:
+19.000000 NoClash_Q46_(A,B,3,0)_Q46_indicator_var
-1.000000 t(A)
+1.000000 t(B)
<= 19.0

c_u_NoClash_Q46_(A,C,1,0)_Q46_c_:
+21.000000 NoClash_Q46_(A,C,1,0)_Q46_indicator_var
-1.000000 t(A)
+1.000000 t(C)
<= 19.0

c_u_NoClash_Q46_(A,B,3,1)_Q46_c_:
+24.000000 NoClash_Q46_(A,B,3,1)_Q46_indicator_var
+1.000000 t(A)
-1.000000 t(B)
<= 19.0

c_u_NoClash_Q46_(B,C,2,0)_Q46_c_:
+25.000000 NoClash_Q46_(B,C,2,0)_Q46_indicator_var
-1.000000 t(B)
+1.000000 t(C)
<= 19.0

c_u_NoClash_Q46_(A,C,1,1)_Q46_c_:
+24.000000 NoClash_Q46_(A,C,1,1)_Q46_indicator_var
+1.000000 t(A)
-1.000000 t(C)
<= 19.0

c_u_NoClash_Q46_(B,C,2,1)_Q46_c_:
+20.000000 NoClash_Q46_(B,C,2,1)_Q46_indicator_var
+1.000000 t(B)
-1.000000 t(C)
<= 19.0

c_e_disj(A,B,3)_:
+1.000000 NoClash_Q46_(A,B,3,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,B,3,1)_Q46_indicator_var
= 1.0

c_e_disj(A,C,1)_:
+1.000000 NoClash_Q46_(A,C,1,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(A,C,1,1)_Q46_indicator_var
= 1.0

c_e_disj(B,C,2)_:
+1.000000 NoClash_Q46_(B,C,2,0)_Q46_indicator_var
+1.000000 NoClash_Q46_(B,C,2,1)_Q46_indicator_var
= 1.0

c_u_Feas(A)_:
-1.000000 ms
+1.000000 t(A)
<= -8

c_u_Feas(B)_:
-1.000000 ms
+1.000000 t(B)
<= -5

c_u_Feas(C)_:
-1.000000 ms
+1.000000 t(C)
<= -6

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds 
    0 <=  NoClash_Q46_(A,B,3,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,B,3,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,C,1,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(A,C,1,1)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,C,2,0)_Q46_indicator_var  <= 1
    0 <=  NoClash_Q46_(B,C,2,1)_Q46_indicator_var  <= 1
     -inf <=  ms  <= +inf
    0 <=  t(A)  <= 19
    0 <=  t(B)  <= 19
    0 <=  t(C)  <= 19
binary
  NoClash_Q46_(A,B,3,0)_Q46_indicator_var
  NoClash_Q46_(A,B,3,1)_Q46_indicator_var
  NoClash_Q46_(A,C,1,0)_Q46_indicator_var
  NoClash_Q46_(A,C,1,1)_Q46_indicator_var
  NoClash_Q46_(B,C,2,0)_Q46_indicator_var
  NoClash_Q46_(B,C,2,1)_Q46_indicator_var
end 
