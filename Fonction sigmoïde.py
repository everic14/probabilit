import numpy as np
import matplotlib.pyplot as plt

# Constantes physiques
k_B = 1.380649e-23  # constante de Boltzmann en J/K
m_H2O = 2.9915e-26  # masse d'une molécule d'eau en kg

# Fonctions de distribution de Maxwell-Boltzmann
def maxwell_boltzmann_distribution(v, T, m):
    return 4 * np.pi * (m / (2 * np.pi * k_B * T))**(1.5) * v**2 * np.exp(-m * v**2 / (2 * k_B * T))

def vitesse_probable(T, m):
    return np.sqrt(2 * k_B * T / m)

def vitesse_moyenne(T, m):
    return np.sqrt(8 * k_B * T / (np.pi * m))

def vitesse_rms(T, m):
    return np.sqrt(3 * k_B * T / m)

# --- Partie principale ---

def main():
    temp_celsius = float(input("Entrez la température en degrés Celsius : "))
    T = temp_celsius + 273.15

    # Simulation de 100 000 vitesses selon Maxwell-Boltzmann
    N = 100000
    v = np.random.normal(loc=0, scale=np.sqrt(k_B * T / m_H2O), size=(N, 3))
    vitesses = np.linalg.norm(v, axis=1)
    vitesses_kmh = vitesses * 3.6

    # Définir les bornes du graphique
    vitesse_max = vitesses_kmh.max()
    bins = np.linspace(0, vitesse_max * 1.1, 60)

    # Histogramme manuel
    counts, bins_hist = np.histogram(vitesses_kmh, bins=bins)
    max_count = counts.max()
    counts = counts * 2

    width = bins_hist[1] - bins_hist[0]

    # Création du graphique
    plt.figure(figsize=(14, 8))
    plt.bar(bins_hist[:-1], counts, width=width, align='edge', color='orange', alpha=0.6, edgecolor='black', label="Histogramme simulé (x2)")

    # Fixer manuellement l'axe Y pour visualiser le doublement
    plt.ylim(0, max_count * 2 * 1.2)

    # Calcul et affichage des vitesses caractéristiques
    v_p = vitesse_probable(T, m_H2O) * 3.6
    v_moy = vitesse_moyenne(T, m_H2O) * 3.6
    v_rms = vitesse_rms(T, m_H2O) * 3.6

    plt.axvline(v_p, color='blue', linestyle='--', label=f"Vitesse probable ({v_p:.0f} km/h)")
    plt.axvline(v_moy, color='green', linestyle='--', label=f"Vitesse moyenne ({v_moy:.0f} km/h)")
    plt.axvline(v_rms, color='red', linestyle='--', label=f"Vitesse RMS ({v_rms:.0f} km/h)")

    plt.title(f"Distribution des vitesses moléculaires simulée\nVapeur d'eau à {temp_celsius:.1f}°C ({T:.1f} K)", fontsize=16)
    plt.xlabel("Vitesse (km/h)", fontsize=14)
    plt.ylabel("Nombre de molécules (amplifié x2)", fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True)

    # Enregistrement en PDF
    plt.savefig("distribution_vitesses_h2o_histogramme_final_sans_courbe.pdf")
    plt.show()

if __name__ == "__main__":
    main()
