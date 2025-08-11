# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 16:56:02 2024

@author: ericd
"""
##   """Calcule la dérivée de la fonction sigmoïde de x."""

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
    result = sigmoid_derivative(x)
    print(f"La dérivée de la fonction sigmoïde pour x = {x} est : {result}")
except ValueError:
    print("Veuillez entrer un nombre valide.")
