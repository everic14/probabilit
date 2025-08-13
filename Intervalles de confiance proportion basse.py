# -*- coding: utf-8 -*-
"""
300Created on Wed Aug 13 07:39:50 2025

@author: ericd
"""

import scipy
print(scipy.__version__)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

# --- Outils statistiques : SciPy si dispo, sinon mpmath ---
_beta_ppf = None
_norm_ppf = None

try:
    from scipy.stats import beta, norm
    _beta_ppf = lambda q, a, b: float(beta.ppf(q, a, b))
    _norm_ppf = lambda q: float(norm.ppf(q))
except Exception:
    try:
        import mpmath as mp
        mp.mp.dps = 60  # précision décimale
        # quantile normal via inverse CDF de la loi normale
        _norm_ppf = lambda q: float(mp.sqrt(2) * mp.erfinv(2*q - 1))
        # quantile Beta via inverse de la fonction bêta incomplète régulière
        def _beta_ppf(q, a, b):
            # mpmath n'a pas de ppf direct; on résout I_x(a,b)=q par bissection
            f = lambda x: mp.betainc(a, b, 0, x, regularized=True) - q
            # bornes [0,1]; éviter singularités avec un petit epsilon
            eps = mp.mpf('1e-20')
            return float(mp.findroot(f, (eps, 1 - eps)))
    except Exception as e:
        raise RuntimeError(
            "Aucune bibliothèque pour les quantiles n'est disponible. "
            "Installez scipy ou mpmath (pip install scipy mpmath)."
        ) from e


def clip01(x):
    return max(0.0, min(1.0, x))


def clopper_pearson(x, n, alpha=0.05):
    """IC exact binomial (Clopper–Pearson), bilatéral."""
    if n <= 0:
        return (float('nan'), float('nan'))
    if x < 0 or x > n:
        return (float('nan'), float('nan'))
    a2 = alpha / 2
    # bornes : Beta(x, n-x+1) et Beta(x+1, n-x)
    lower = 0.0 if x == 0 else _beta_ppf(a2, x, n - x + 1)
    upper = 1.0 if x == n else _beta_ppf(1 - a2, x + 1, n - x)
    return (clip01(lower), clip01(upper))


def wilson(x, n, alpha=0.05):
    """IC de Wilson (score)."""
    if n <= 0:
        return (float('nan'), float('nan'))
    z = _norm_ppf(1 - alpha / 2)
    phat = x / n
    den = 1 + (z*z)/n
    center = phat + (z*z)/(2*n)
    adj = z * math.sqrt(phat*(1 - phat)/n + (z*z)/(4*n*n))
    lower = (center - adj) / den
    upper = (center + adj) / den
    return (clip01(lower), clip01(upper))


def agresti_coull(x, n, alpha=0.05):
    """IC Agresti–Coull (ajout de pseudo-obs)."""
    if n <= 0:
        return (float('nan'), float('nan'))
    z = _norm_ppf(1 - alpha / 2)
    n_t = n + z*z
    p_t = (x + (z*z)/2) / n_t
    se = math.sqrt(p_t*(1 - p_t)/n_t)
    lower = p_t - z*se
    upper = p_t + z*se
    return (clip01(lower), clip01(upper))


def jeffreys(x, n, alpha=0.05):
    """IC bayésien égal-taillé avec a priori de Jeffreys Beta(0.5, 0.5)."""
    if n <= 0:
        return (float('nan'), float('nan'))
    a_post = x + 0.5
    b_post = n - x + 0.5
    lower = _beta_ppf(alpha/2, a_post, b_post)
    upper = _beta_ppf(1 - alpha/2, a_post, b_post)
    return (clip01(lower), clip01(upper))


def logit_transform(x, n, alpha=0.05):
    """IC via transformation logit avec correction pour x=0 ou x=n.
    On utilise la correction de Haldane–Anscombe: p_t = (x+0.5)/(n+1)."""
    if n <= 0:
        return (float('nan'), float('nan'))
    z = _norm_ppf(1 - alpha / 2)
    p_t = (x + 0.5) / (n + 1.0)
    # logit et variance approx 1/(n * p * (1-p))
    logit_p = math.log(p_t / (1 - p_t))
    se_logit = math.sqrt(1.0 / (n * p_t * (1 - p_t)))
    lo = logit_p - z * se_logit
    hi = logit_p + z * se_logit
    # retour sur échelle p: expit
    lower = 1 / (1 + math.exp(-lo))
    upper = 1 / (1 + math.exp(-hi))
    return (clip01(lower), clip01(upper))


def arcsin_sqrt_anscombe(x, n, alpha=0.05):
    """IC via transformation arcsin(√p) avec correction d'Anscombe.
    p_t = (x + 3/8) / (n + 3/4), Var(theta) ≈ 1/(4n)."""
    if n <= 0:
        return (float('nan'), float('nan'))
    z = _norm_ppf(1 - alpha / 2)
    p_t = (x + 3/8) / (n + 3/4)
    theta = math.asin(math.sqrt(clip01(p_t)))
    halfwidth = z / (2 * math.sqrt(n))
    lo_theta = max(0.0, theta - halfwidth)
    hi_theta = min(math.pi/2, theta + halfwidth)
    lower = math.sin(lo_theta) ** 2
    upper = math.sin(hi_theta) ** 2
    return (clip01(lower), clip01(upper))


def compute_all(n, x, conf_level=0.95):
    alpha = 1 - conf_level
    methods = [
        ("Clopper–Pearson (exact)", clopper_pearson),
        ("Wilson (score)", wilson),
        ("Agresti–Coull", agresti_coull),
        ("Jeffreys (bayésien, Beta(0.5,0.5))", jeffreys),
        ("Logit transform (Haldane–Anscombe)", logit_transform),
        ("Arcsin √ (Anscombe)", arcsin_sqrt_anscombe),
    ]
    results = []
    for name, func in methods:
        lo, hi = func(x, n, alpha)
        results.append((name, lo, hi))
    return results


def pretty_print(n, x, conf_level, results):
    print(f"\nProportion observée: x/n = {x}/{n} = {x/n:.6f}")
    print(f"Niveau de confiance: {conf_level*100:.1f}%\n")
    width = max(len(name) for name, _, _ in results)
    header = f"{'Méthode'.ljust(width)}  Borne inf.      Borne sup."
    print(header)
    print("-" * len(header))
    for name, lo, hi in results:
        print(f"{name.ljust(width)}  {lo:>12.8f}    {hi:>12.8f}")
    print("")



if __name__ == "__main__":
    # --- Saisie utilisateur ---
    try:
        n = int(input("Entrez le nombre total d'observations n: ").strip())
        x = int(input("Entrez le nombre d'événements positifs x: ").strip())
        cl_input = input("Niveau de confiance (ex: 0.95) [défaut 0.95]: ").strip()
        conf_level = float(cl_input) if cl_input else 0.95
    except Exception as e:
        raise SystemExit(f"Entrées invalides: {e}")

    if n <= 0 or x < 0 or x > n:
        raise SystemExit("Conditions requises: n > 0 et 0 ≤ x ≤ n.")

    res = compute_all(n, x, conf_level)
    pretty_print(n, x, conf_level, res)
print("""
Choisir :

Clopper–Pearson si l’on privilégie la couverture garantie.

Wilson ou Jeffreys si l’on souhaite un bon compromis largeur / couverture.

Pour n très petit (< 20) et p faible : privilégier la méthode exacte ou bayésienne.
""")    
