# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 17:10:07 2024

@author: ericd
""""""Calcule la fonction sigmoïde de x et de la dérivée"""

import math

def sigmoid(x):
    """Calcule la fonction sigmoïde de x."""
    return 1 / (1 + math.exp(-x))

def sigmoid_derivative(x):
    """Calcule la dérivée de la fonction sigmoïde de x."""
    sig = sigmoid(x)
    return sig * (1 - sig)

# Invite l'utilisateur à fournir une valeur pour x
try:
    x = float(input("Entrez la valeur de x : "))
    sig_value = sigmoid(x)
    sig_derivative_value = sigmoid_derivative(x)
    print(f"La valeur de la fonction sigmoïde pour x = {x} est : {sig_value}")
    print(f"La valeur de la dérivée de la fonction sigmoïde pour x = {x} est : {sig_derivative_value}")
except ValueError:
    print("Veuillez entrer un nombre valide.")
