# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 09:47:16 2023

@author: Éric
### Probabilité binomiale que X = k"""

from math import comb

# Paramètres du problème
N = 1000  # Taille totale de la population
K = 500   # Nombre d'éléments dans la population avec le trait caractéristique
n = 12    # Nombre de tirages
k = 4     # Nombre de résultats + (présence du trait)

# Calcul de la probabilité P(X = 4)
probability = comb(K, k) * comb(N - K, n - k) / comb(N, n)

print("La probabilité P(X = 4) est :", probability)
