


import math

def nombre_sequences_possibles(n, k):
    sequences_possibles = math.factorial(n) // math.factorial(n - k)
    return sequences_possibles

def probabilite_sequence_pour_k_elements(n, k):
    probabilite_sequence = 1 / nombre_sequences_possibles(n, k)
    return probabilite_sequence


# définir k et n   k:nombre choisi n: nombre de choix possibles
n = 49
k = 6

sequences_possibles = nombre_sequences_possibles(n, k)
print(f"Nombre de séquences possibles : {sequences_possibles}")

probabilite_sequence = probabilite_sequence_pour_k_elements(n, k)
# Utilisation d'un format personnalisé pour l'affichage
print(f"Probabilité d'obtenir une séquence prédéfinie : {probabilite_sequence:.6e}".replace('e', ' x 10^'))

