# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 17:30:02 2023

@author: Éric
"""

import math

# spécifier le nombre k de choix que l'on fera à partir de n possibilités.
# l'ordre du choix n'est pas important, mais chaque nombre ne peut être choisi qu'une seule fois.
n = 49
k = 6
##l'ordre des nombres n'est pas important  1,2,3,4 et 1,4,2,3 sont équivalents


def nombre_combinaisons(n, k):
    combinaisons = math.factorial(n) // (math.factorial(k) * math.factorial(n - k))
    return combinaisons


def probabilite_combinaison_pour_k_elements(n, k):
    probabilite_combinaison = 1 / combinaisons
    return probabilite_combinaison


combinaisons = nombre_combinaisons(n, k)
print(f"Nombre de combinaisons possibles : {combinaisons}")

probabilite_combinaison = 1/combinaisons
# Utilisation de la notation scientifique pour l'affichage
print(f"Probabilité d'obtenir une combinaison prédéfinie de {k}nombres choisis parmi {n} nombres, sans tenir compte de l'ordre: {probabilite_combinaison:.5e}".replace(
    'e', ' x 10^'))
