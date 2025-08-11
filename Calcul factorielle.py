44# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Factorial of a number using recursion

num = float(input("Entrez le nombre: "))
def recur_factorial(n):
   if n == 1:
       return n
   else:
       return n*recur_factorial(n-1)



# check if the number is negative
if num < 0:
   print("Sorry, factorial does not exist for negative numbers")
elif num == 0:
   print("The factorial of 0 is 1")
else:
   print("La factorielle de ", num, "est", recur_factorial(num))

