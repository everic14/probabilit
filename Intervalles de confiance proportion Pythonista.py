# -*- coding: utf-8 -*-
"""
Created on 33
Wed Aug 13 13:58:32 2025

@author: ericd
"""

# --- Détection/initialisation mpmath (compatible Pythonista) ---
import math
def clip01(x):
    """Force x à rester entre 0 et 1."""
    return max(0.0, min(1.0, x))


_HAVE_MPMATH = False
_beta_ppf = None
_norm_ppf = None
# -*- coding: utf-8 -*-
# Script compatible Pythonista (iOS) – SciPy non requis

import math, os

# ---------- Optionnel: mini-UI Pythonista ----------
try:
    import dialogs  # dispo dans Pythonista
    _USE_DIALOGS = True
except Exception:
    _USE_DIALOGS = False

# ---------- Try mpmath (active Clopper–Pearson & Jeffreys si présent) ----------
try:
    import mpmath as mp
    mp.mp.dps = 80  # précision interne

    def _norm_ppf(q):
        return float(mp.sqrt(2) * mp.erfinv(2*q - 1))

    def _beta_ppf(q, a, b, tol=None, maxiter=500):
        """Inversion robuste par bissection"""
        if not (0.0 < q < 1.0):
            return float('nan')
        q = mp.mpf(q); a = mp.mpf(a); b = mp.mpf(b)
        if tol is None:
            tol = mp.mpf(10) ** (-(mp.mp.dps - 10))
        eps = mp.mpf('1e-30')
        lo = eps
        hi = 1 - eps
        for _ in range(maxiter):
            mid = (lo + hi) / 2
            val = mp.betainc(a, b, 0, mid, regularized=True)
            if val < q:
                lo = mid
            else:
                hi = mid
            if hi - lo <= tol:
                return float((lo + hi) / 2)
        return float((lo + hi) / 2)

    _HAVE_MPMATH = True

except Exception:
    _HAVE_MPMATH = False
    # Ici on met votre code de repli (Acklam) pour _norm_ppf
    def _norm_ppf(p):
        # code du quantile normal approximatif...
        pass
    # Pas de _beta_ppf disponible dans ce mode

# ---------- Méthodes ----------
def wilson(x, n, alpha=0.05):
    z = _norm_ppf(1 - alpha/2)
    phat = x / n
    den = 1 + (z*z)/n
    center = phat + (z*z)/(2*n)
    adj = z * math.sqrt(phat*(1 - phat)/n + (z*z)/(4*n*n))
    return (clip01((center - adj)/den), clip01((center + adj)/den))

def agresti_coull(x, n, alpha=0.05):
    z = _norm_ppf(1 - alpha/2)
    n_t = n + z*z
    p_t = (x + (z*z)/2) / n_t
    se = math.sqrt(p_t*(1 - p_t)/n_t)
    return (clip01(p_t - z*se), clip01(p_t + z*se))

def logit_transform(x, n, alpha=0.05):
    z = _norm_ppf(1 - alpha/2)
    p_t = (x + 0.5) / (n + 1.0)  # Haldane–Anscombe
    logit_p = math.log(p_t/(1 - p_t))
    se = math.sqrt(1.0/(n*p_t*(1 - p_t)))
    lo = 1/(1 + math.exp(-(logit_p - z*se)))
    hi = 1/(1 + math.exp(-(logit_p + z*se)))
    return (clip01(lo), clip01(hi))

def arcsin_sqrt_anscombe(x, n, alpha=0.05):
    z = _norm_ppf(1 - alpha/2)
    p_t = (x + 3/8) / (n + 3/4)
    theta = math.asin(math.sqrt(clip01(p_t)))
    half = z / (2 * math.sqrt(n))
    lo = math.sin(max(0.0, theta - half))**2
    hi = math.sin(min(math.pi/2, theta + half))**2
    return (clip01(lo), clip01(hi))

# Méthodes nécessitant Beta-quantiles (activées si mpmath présent)
def clopper_pearson(x, n, alpha=0.05):
    if not _HAVE_MPMATH: return (float('nan'), float('nan'))
    a2 = alpha/2
    lower = 0.0 if x == 0 else _beta_ppf(a2, x, n - x + 1)
    upper = 1.0 if x == n else _beta_ppf(1 - a2, x + 1, n - x)
    return (clip01(lower), clip01(upper))

def jeffreys(x, n, alpha=0.05):
    if not _HAVE_MPMATH: return (float('nan'), float('nan'))
    a_post = x + 0.5
    b_post = n - x + 0.5
    return (_beta_ppf(alpha/2, a_post, b_post),
            _beta_ppf(1 - alpha/2, a_post, b_post))

def compute_all(n, x, conf_level=0.95):
    alpha = 1 - conf_level
    methods = [
        ("Clopper–Pearson (exact)", clopper_pearson),
        ("Wilson (score)",          wilson),
        ("Agresti–Coull",           agresti_coull),
        ("Jeffreys (Beta(0.5,0.5))",jeffreys),
        ("Logit transform",         logit_transform),
        ("Arcsin √ (Anscombe)",     arcsin_sqrt_anscombe),
    ]
    res = []
    for name, func in methods:
        lo, hi = func(x, n, alpha)
        res.append((name, lo, hi))
    return res

def pretty_print(n, x, conf_level, res):
    print(f"\nProportion observée: x/n = {x}/{n} = {x/n:.8f}")
    print(f"Niveau de confiance: {conf_level*100:.1f}%\n")
    width = max(len(name) for name, _, _ in res)
    header = f"{'Méthode'.ljust(width)}  Borne inf.          Borne sup."
    print(header)
    print("-"*len(header))
    for name, lo, hi in res:
        s_lo = "n/a" if math.isnan(lo) else f"{lo:16.8f}"
        s_hi = "n/a" if math.isnan(hi) else f"{hi:16.8f}"
        print(f"{name.ljust(width)}  {s_lo}    {s_hi}")
    print("""
Choisir :

Clopper–Pearson si l’on privilégie la couverture garantie.

Wilson ou Jeffreys si l’on souhaite un bon compromis largeur / couverture.

Pour n très petit (< 20) et p faible : privilégier la méthode exacte ou bayésienne.
""")

def save_csv(res, path):
    try:
        import csv
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Méthode", "Borne inférieure", "Borne supérieure"])
            for name, lo, hi in res:
                w.writerow([name,
                            "" if math.isnan(lo) else f"{lo:.8f}",
                            "" if math.isnan(hi) else f"{hi:.8f}"])
        print(f"Résultats enregistrés: {path}")
    except Exception as e:
        print(f"Échec enregistrement CSV: {e}")

def get_inputs():
    if _USE_DIALOGS:
        form = dialogs.form_dialog(title='IC proportion (Pythonista)', fields=[
            {'type':'number','key':'n','title':'n (total)', 'value':200},
            {'type':'number','key':'x','title':'x (positifs)', 'value':5},
            {'type':'number','key':'cl','title':'Confiance (0-1)', 'value':0.95},
            {'type':'switch','key':'csv','title':'Enregistrer CSV', 'value':True},
        ])
        if not form: raise SystemExit("Annulé.")
        n = int(form['n']); x = int(form['x']); cl = float(form['cl'])
        save = bool(form['csv'])
        return n, x, cl, save
    # fallback console
    n = int(input("n (total): ").strip())
    x = int(input("x (positifs): ").strip())
    cl_in = input("Confiance (ex 0.95) [0.95]: ").strip()
    cl = float(cl_in) if cl_in else 0.95
    save = input("Enregistrer CSV ? [o/N]: ").strip().lower().startswith('o')
    return n, x, cl, save

if __name__ == "__main__":
    n, x, cl, save = get_inputs()
    if n <= 0 or x < 0 or x > n:
        raise SystemExit("Conditions: n > 0 et 0 ≤ x ≤ n.")
    res = compute_all(n, x, cl)
    pretty_print(n, x, cl, res)
    if save:
        docs = os.path.expanduser("~/Documents")
        save_csv(res, os.path.join(docs, "intervals.csv"))
    if not _HAVE_MPMATH:
        print("Note: mpmath non détecté — Clopper–Pearson et Jeffreys affichés comme n/a.\n"
              "Vous pouvez installer mpmath (pur Python) dans Pythonista pour les activer.")
try:
    import mpmath as mp
    mp.mp.dps = 60  # précision interne
    def _norm_ppf(q):
        return float(mp.sqrt(2) * mp.erfinv(2*q - 1))
    def _beta_ppf(q, a, b):
        # Inversion de l’incomplète bêta régulière via findroot, bornes [ε, 1-ε]
        eps = mp.mpf('1e-20')
        f = lambda x: mp.betainc(a, b, 0, x, regularized=True) - q
        return float(mp.findroot(f, (eps, 1 - eps)))
    _HAVE_MPMATH = True
except Exception:
    # Fallback: quantile normal (Acklam) pour Wilson/Agresti/Logit/Arcsin
    def _norm_ppf(p):
        if p <= 0.0 or p >= 1.0:
            raise ValueError("p doit être dans (0,1)")
        a = [-3.969683028665376e+01,  2.209460984245205e+02,
             -2.759285104469687e+02,  1.383577518672690e+02,
             -3.066479806614716e+01,  2.506628277459239e+00]
        b = [-5.447609879822406e+01,  1.615858368580409e+02,
             -1.556989798598866e+02,  6.680131188771972e+01,
             -1.328068155288572e+01]
        c = [-7.784894002430293e-03, -3.223964580411365e-01,
             -2.400758277161838e+00, -2.549732539343734e+00,
              4.374664141464968e+00,  2.938163982698783e+00]
        d = [ 7.784695709041462e-03,  3.224671290700398e-01,
              2.445134137142996e+00,  3.754408661907416e+00]
        plow, phigh = 0.02425, 1 - 0.02425
        if p < plow:
            q = math.sqrt(-2*math.log(p))
            return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                   ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
        elif p <= phigh:
            q = p - 0.5
            r = q*q
            num = (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q
            den = (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
            return num/den
        else:
            q = math.sqrt(-2*math.log(1-p))
            return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                     ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)

    # Signaler proprement dans Pythonista comment installer mpmath
    _msg = (
        "Module manquant : mpmath\n\n"
        "Pour activer Clopper–Pearson et Jeffreys :\n"
        "1) Installez StaSh dans Pythonista en exécutant :\n"
        "   import requests as r; exec(r.get('https://bit.ly/get-stash').text)\n"
        "2) Ouvrez StaSh puis tapez :\n"
        "   pip install mpmath\n\n"
        "Les méthodes exactes/bayésiennes seront affichées comme n/a jusqu’à l’installation."
    )
    try:
        import dialogs
        dialogs.alert("Info", _msg, "OK", hide_cancel_button=True)
    except Exception:
        try:
            import console
            console.alert("Info", _msg, "OK", hide_cancel_button=True)
        except Exception:
            print(_msg)
