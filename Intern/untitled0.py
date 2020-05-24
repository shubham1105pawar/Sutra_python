# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 12:17:23 2020

@author: Shubham
"""
tcs = '''
(a-b)2=a2+b2-2ab
(a+b+c)2=a2+b2+c2+2*a*b+2*b*c+2*c*a
'''
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
R = tcs[0]
L = ['+','-','*','/']
for i in range(1,len(tcs)):
    if tcs[i-1] not in L and tcs[i].isdigit():
        R+=tcs[i].translate(SUP)
    elif  tcs[i-1]=='^' and tcs[i].isdigit():
        R=R[:-1]+tcs[i].translate(SUP)
    else:
        R+=tcs[i]
        
print(R)