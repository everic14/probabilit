def bayes_theorem(prob_a, prob_b_given_a, prob_b, decimal_places=9):
    # Vérification des probabilités
    if not (0 <= prob_a <= 1) or not (0 <= prob_b_given_a <= 1)\
            or not (0 <= prob_b <= 1):
        raise ValueError("Les probabilités doivent être comprises entre 0 et 1.")

    # Vérification pour éviter une division par zéro
    if prob_b == 0 and prob_b_given_a == 1:
        raise ValueError("""La probabilité de B est
                         nulle, ce qui provoque une division par zéro.""")

    # Si la probabilité de B sachant A est de 1, le résultat de Bayes
    # est simplement la probabilité de A
    if prob_b_given_a == 1:
        return round(prob_a, decimal_places)

    # Correction de la formule pour éviter des résultats incohérents
    prob_a_given_b = round((prob_b_given_a * prob_a) /
                           ((prob_b_given_a * prob_a) +
                            ((1 - prob_b_given_a) * (1 - prob_a))), decimal_places)
    return prob_a_given_b


# Exemple d'utilisation
try:
    # Spécifiez les probabilités de base
    prob_a = float(input("Entrez la probabilité de A: "))
    prob_b_given_a = float(input("Entrez la probabilité de B sachant A: "))
    prob_b = float(input("Entrez la probabilité de B: "))

    # Calcul de la probabilité de A sachant B
    result = bayes_theorem(prob_a, prob_b_given_a, prob_b)

    # Affichage du résultat en notation scientifique avec 9 décimales
    print(f"La probabilité que A soit vrai si B est vrai: {result:.9e}")
    print(f"La probabilité que A soit faux si B est vrai: {round(1 - result, 9):.9e}")

except ValueError as e:
    print(f"Erreur: {e}")
