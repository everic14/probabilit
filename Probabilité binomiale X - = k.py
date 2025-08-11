# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 08:56:57 2023

@author: Éric
"""
### Probabilité binomiale X <= k

from math import comb

# Paramètres du problème: probabilité binomiale cumulée avec p = K/N et n piges
N = 1000  # Taille totale de la population
K = 500   # Nombre d'éléments dans la population avec le trait caractéristique
n = 12    # Nombre de tirages
k = 4    # nombre de résultats positifs

# Calcul de la probabilité P(X <= k)
probability = sum(comb(K, k) * comb(N - K, n - k) / comb(N, n) for k in range(0,k+1))

print(f"La probabilité de (X <={k}), est :", probability)


