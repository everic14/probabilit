# -*- coding: utf-8 -*-
"""
Created on Sat May 18 17:25:39 2024

@author: Éric
"""
###### Calcul de factorielles élevées avec résultat en notation scientifique########
import math
from decimal import Decimal, getcontext

# Fixer la précision souhaitée
getcontext().prec = 50

def factorial_scientific(n):
    # Calculer la factorielle de n
    fact = Decimal(math.factorial(n))
    
    # Formater le résultat en notation scientifique avec 4 décimales
    scientific_notation = f"{fact:.4e}"
    
    return scientific_notation

############### Exemple d'utilisation#######################################
############### Entrer le nombre entier positif#############################
n = 8 
##### Vous pouvez changer cette valeur pour tester d'autres factorielles####
############################################################################
############################################################################
result = factorial_scientific(n)
print(f"Factorielle de {n} en notation scientifique: {result}")