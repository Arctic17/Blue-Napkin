import numpy as np
import math

"""
=============================================================================
PARTIE 1 : CALCULS SIMPLES & SIGNAL (ECHANTILLONNAGE, DB, RESOLUTION)
Sources: [8], [4], [9], [5], [10]
=============================================================================
"""

def calcul_resolution_numerique(plage_entree, nombre_bits):
    """
    Calcule la résolution (plus petit incrément mesurable) d'un convertisseur A/D.
    Source: [9]

    Paramètres:
    -----------
    plage_entree : float
        L'étendue de mesure totale (ex: 10V pour -5V à +5V, ou 5V pour 0-5V). [Unité: V]
    nombre_bits : int
        La résolution du convertisseur (ex: 8, 12, 16 bits).

    Retourne:
    ---------
    resolution : float
        La valeur d'un bit (pas de quantification).
    """
    resolution = plage_entree / (2**nombre_bits)
    print(f"--- Résolution Numérique ---")
    print(f"Plage: {plage_entree} V, Bits: {nombre_bits}")
    print(f"Résolution (Pas): {resolution:.6f} V")
    return resolution

def calcul_fft_indices(N_points, f_echantillonnage, f_signal=None, index_k=None):
    """
    Relie la fréquence, l'index FFT et la résolution fréquentielle.
    Source: [11], [4], [12]

    Paramètres:
    -----------
    N_points : int
        Nombre total de points de la FFT (ex: 128, 1024).
    f_echantillonnage : float
        Fréquence d'échantillonnage (fe ou fs). [Hz]
    f_signal : float (Optionnel)
        Fréquence du signal dont on cherche l'index k. [Hz]
    index_k : int (Optionnel)
        Index dans le tableau FFT dont on cherche la fréquence.

    Retourne:
    ---------
    resolution : float (Delta f)
    """
    resolution = f_echantillonnage / N_points
    print(f"--- Analyse FFT (N={N_points}) ---")
    print(f"Résolution fréquentielle (Delta f): {resolution:.2f} Hz")
    print(f"Fréquence Max (Nyquist): {f_echantillonnage/2:.2f} Hz")

    if f_signal is not None:
        k = f_signal / resolution
        print(f"-> Le signal {f_signal} Hz se trouve à l'index k = {k:.2f}")

    if index_k is not None:
        f_k = index_k * resolution
        print(f"-> L'index k={index_k} correspond à la fréquence f = {f_k:.2f} Hz")

    return resolution

def calcul_gain_db(P_out=None, P_in=None, U_out=None, U_in=None):
    """
    Calcule le gain en décibels pour la puissance ou la tension.
    Source: [13], [5]

    Paramètres:
    -----------
    P_out, P_in : float (Optionnel)
        Puissances de sortie et d'entrée. [W]
    U_out, U_in : float (Optionnel)
        Tensions de sortie et d'entrée. [V]

    Note: Remplir soit les P, soit les U.
    """
    print(f"--- Calcul dB ---")
    if P_out is not None and P_in is not None:
        G_db = 10 * np.log10(P_out / P_in)
        print(f"Gain Puissance: {G_db:.2f} dB")
        return G_db
    elif U_out is not None and U_in is not None:
        G_db = 20 * np.log10(U_out / U_in)
        print(f"Gain Tension: {G_db:.2f} dB")
        return G_db
    else:
        print("Erreur: Fournir P_out/P_in OU U_out/U_in")
        return 0

def vitesse_codeur_incremental(N_stries, f_max_signal=None, periode_lecture_s=None, delta_pulses=None):
    """
    Calcule la vitesse ou la fréquence max pour un codeur incrémental.
    Source: [14], [10]

    Paramètres:
    -----------
    N_stries : int
        Nombre de stries (impulsions par tour) du disque.
    f_max_signal : float (Optionnel)
        Fréquence électrique maximale admissible par le capteur. [Hz]
    periode_lecture_s : float (Optionnel)
        Temps d'échantillonnage Ts pour le calcul de vitesse. [s]
    delta_pulses : int (Optionnel)
        Nombre d'impulsions comptées pendant Ts.
    """
    print(f"--- Codeur Incrémental ({N_stries} stries) ---")

    # Cas 1: Vitesse max à partir de la fréquence limite
    if f_max_signal is not None:
        # v_max [tours/s] = f_max / N_stries
        v_tours_sec = f_max_signal / N_stries
        print(f"Vitesse Max (limite élec): {v_tours_sec:.2f} tours/s (= {v_tours_sec*60:.0f} tr/min)")
        return v_tours_sec

    # Cas 2: Calcul de vitesse actuelle
    if periode_lecture_s is not None and delta_pulses is not None:
        # Vitesse = (Delta Pulses) / (N_stries * Ts)
        v_tours_sec = delta_pulses / (N_stries * periode_lecture_s) # Attention: parfois *4 si quadrature
        print(f"Vitesse mesurée: {v_tours_sec:.2f} tours/s")
        return v_tours_sec

"""
=============================================================================
PARTIE 2 : ERREURS & LINEARISATION
Sources: [1], [15], [16], [17]
=============================================================================
"""

def erreur_totale_appareil(lecture, etendue_max, precision_lecture_pct, precision_gamme_pct, digits=0, resolution=0):
    """
    Calcule l'erreur totale d'un appareil (type multimètre).
    Formule: Erreur = (% Lecture * Lecture) + (% Gamme * Gamme) + (Digits * Résolution)
    Source: [1], [15]

    Paramètres:
    -----------
    lecture : float
        La valeur affichée/mesurée. [V, A, etc.]
    etendue_max : float
        La gamme (Range) utilisée (ex: 200V). [V, A, etc.]
    precision_lecture_pct : float
        Précision proportionnelle en %. (ex: 1.5 pour 1.5%)
    precision_gamme_pct : float
        Précision constante (Full Scale) en %. (ex: 0.5 pour 0.5%)
    digits : int (Optionnel)
        Nombre de digits d'erreur (souvent "dgt").
    resolution : float (Optionnel)
        Valeur d'un digit (résolution).

    Retourne:
    ---------
    erreur_abs : float (Erreur absolue)
    """
    partie_prop = (precision_lecture_pct / 100) * lecture
    partie_const = (precision_gamme_pct / 100) * etendue_max
    partie_digits = digits * resolution

    erreur_abs = partie_prop + partie_const + partie_digits

    print(f"--- Erreur de Mesure ---")
    print(f"Lecture: {lecture}, Gamme: {etendue_max}")
    print(f"Erreur Absolue: +/- {erreur_abs:.4f}")
    if lecture != 0:
        print(f"Erreur Relative: +/- {(erreur_abs/lecture)*100:.4f}%")

    return erreur_abs

def linearisation_taylor(fonction, x0, x_mesure, h=1e-5):
    """
    Calcule la valeur linéarisée y = f(x0) + S*(x-x0).
    S (Sensibilité) est la dérivée calculée numériquement.
    Source: [16]

    Paramètres:
    -----------
    fonction : function
        Une fonction Python (ex: lambda x: x**2).
    x0 : float
        Le point de fonctionnement (linéarisation autour de ce point).
    x_mesure : float
        La valeur réelle mesurée pour laquelle on veut l'approximation.
    """
    y0 = fonction(x0)
    # Calcul dérivée (Sensibilité S)
    S = (fonction(x0 + h) - fonction(x0 - h)) / (2 * h)

    y_lin = y0 + S * (x_mesure - x0)

    print(f"--- Linéarisation (Taylor) ---")
    print(f"Point de fonctionnement x0: {x0}")
    print(f"Sensibilité S (dy/dx) à x0: {S:.4f}")
    print(f"Valeur Exacte à {x_mesure}: {fonction(x_mesure):.4f}")
    print(f"Valeur Linéarisée à {x_mesure}: {y_lin:.4f}")
    print(f"Erreur de linéarisation: {abs(y_lin - fonction(x_mesure)):.4e}")
    return y_lin

"""
=============================================================================
PARTIE 3 : CAPTEURS (PONTS, PIEZO, TEMPERATURE)
Sources: [2], [18], [19], [20], [21]
=============================================================================
"""

def pont_wheatstone_jauge(U0, K, epsilon, type_pont='quart', nu=0.3):
    """
    Calcule la tension de sortie Um d'un pont de Wheatstone.
    Source: [2], [18], [22]

    Paramètres:
    -----------
    U0 : float
        Tension d'alimentation du pont. [V]
    K : float
        Facteur de jauge (Gauge Factor). [sans unité]
    epsilon : float
        Déformation (Strain) = Delta L / L. [sans unité] (ex: 1000e-6)
    type_pont : str
        'quart' (1 jauge), 'demi' (2 jauges), 'complet' (4 jauges).
    nu : float (Optionnel)
        Coefficient de Poisson (pour pont complet avec jauges transversales).

    Retourne:
    ---------
    Um : float (Tension de mesure) [V]
    """
    print(f"--- Pont de Wheatstone ({type_pont}) ---")
    Um = 0
    if type_pont == 'quart':
        # Um approx = U0/4 * K * epsilon (Source [2])
        Um = (U0 / 4) * K * epsilon
    elif type_pont == 'demi':
        # Um approx = U0/2 * K * epsilon (Push-Pull)
        Um = (U0 / 2) * K * epsilon
    elif type_pont == 'complet':
        # Avec Poisson (Source [22]): Um = U0/4 * K * epsilon * 2 * (1+nu)
        # Simplifié souvent à: Um = U0 * K * epsilon * (1+nu)/2 selon montage
        # Utilisation formule Source [22] simplifiée:
        Um = (U0 / 4) * K * epsilon * 2 * (1 + nu)

    print(f"Tension de sortie Um: {Um:.6f} V ({Um*1000:.3f} mV)")
    return Um

def piezo_accelerometre(beta, Ms, C_cable, C_ampli, acceleration_ms2=None, Force=None):
    """
    Calcule la tension de sortie d'un capteur piézoélectrique.
    U = Q / C_total = (beta * F) / C_total
    Source: [3], [20], [23]

    Paramètres:
    -----------
    beta : float
        Sensibilité en charge du cristal. [C/N] (Coulomb par Newton)
    Ms : float
        Masse sismique. [kg]
    C_cable : float
        Capacité du câble. [F]
    C_ampli : float
        Capacité d'entrée de l'amplificateur. [F]
    acceleration_ms2 : float (Optionnel)
        Accélération appliquée. [m/s^2]

    Retourne:
    ---------
    U : float (Tension) [V]
    """
    # Calcul Capacité Capteur (modèle plan parallèle C = eps S / h)
    # Souvent C_sensor est donné ou négligeable devant C_cable, ici on suppose
    # qu'il faut l'ajouter si donné, sinon on utilise C_total externe.
    # Dans l'exo 7.2 [20], C_total est la somme.

    # Note: Si C_sensor n'est pas donné explicitement, vérifiez s'il faut le calculer.
    # Ici, nous prenons C_total = C_cable + C_ampli (Hypothèse C_sensor faible ou inclus)
    C_total = C_cable + C_ampli

    print(f"--- Capteur Piézo ---")
    if acceleration_ms2 is not None:
        Force = Ms * acceleration_ms2
        print(f"Force (F = m*a): {Force:.4f} N")

    if Force is not None:
        Q = beta * Force
        U = Q / C_total
        Sensibilite_S = (beta * Ms) / C_total # [V / (m/s^2)]

        print(f"Charge Q: {Q:.2e} C")
        print(f"Capacité Totale: {C_total:.2e} F")
        print(f"Tension U: {U:.6f} V")
        print(f"Sensibilité S: {Sensibilite_S:.6f} V/(m/s^2)")
        return U
    return 0

def temperature_rtd(R0, T, A=3.9083e-3, B=-5.775e-7):
    """
    Calcule la résistance d'une sonde RTD (ex: Pt100) pour une température T.
    Utilise l'équation de Callendar-Van Dusen (simplifiée T>0).
    Source: [21]

    Paramètres:
    -----------
    R0 : float
        Résistance à 0°C (ex: 100 pour Pt100). [Ohm]
    T : float
        Température. [°C]
    """
    # R = R0 * (1 + A*T + B*T^2)
    R = R0 * (1 + A*T + B*(T**2))
    print(f"--- Température RTD (Pt{R0}) ---")
    print(f"Température: {T} °C")
    print(f"Résistance R(T): {R:.4f} Ohm")
    return R

"""
=============================================================================
PARTIE 4 : PHYSIQUE ET FLUIDES (PITOT, TEMPS DE VOL)
Sources: [24], [25], [26]
=============================================================================
"""

def tube_pitot_vitesse(delta_P, rho_air=1.225):
    """
    Calcule la vitesse de l'air à partir de la pression différentielle (Pitot).
    Bernoulli: P_tot = P_stat + 0.5 * rho * v^2
    Source: [24]

    Paramètres:
    -----------
    delta_P : float
        Différence de pression (P_tot - P_stat). [Pa] (Pascal)
        Si vous avez des mmH2O, multiplier par 9.81 (g).
    rho_air : float
        Masse volumique de l'air (ou fluide). [kg/m^3]

    Retourne:
    ---------
    v : float (Vitesse) [m/s]
    """
    # v = sqrt( 2 * DeltaP / rho )
    v = np.sqrt( (2 * delta_P) / rho_air )
    print(f"--- Tube de Pitot ---")
    print(f"Delta P: {delta_P} Pa")
    print(f"Vitesse calculée: {v:.2f} m/s ({v*3.6:.1f} km/h)")
    return v

def distance_temps_vol(lag_echantillons, f_echantillonnage, c=340, mode='echo'):
    """
    Calcule la distance basée sur le temps de vol (Corrélation).
    Source: [7], [26]

    Paramètres:
    -----------
    lag_echantillons : int
        Décalage (lag) du pic de corrélation en nombre d'échantillons.
    f_echantillonnage : float
        Fréquence d'échantillonnage. [Hz]
    c : float
        Vitesse du son. [m/s] (défaut 340)
    mode : str
        'direct' (émetteur -> récepteur) ou 'echo' (aller-retour).

    Retourne:
    ---------
    d : float (Distance) [m]
    """
    delta_t = lag_echantillons / f_echantillonnage
    distance = delta_t * c

    if mode == 'echo':
        distance = distance / 2 # Aller-retour

    print(f"--- Mesure Distance (Mode {mode}) ---")
    print(f"Lag: {lag_echantillons} samples -> Temps: {delta_t*1000:.3f} ms")
    print(f"Distance: {distance:.4f} m")
    return distance

"""
=============================================================================
PARTIE 5 : REGRESSION LINEAIRE (CALIBRATION)
Source: [6], [27]
=============================================================================
"""

def regression_lineaire_moindres_carres(x_data, y_data):
    """
    Calcule la droite y = ax + b qui minimise l'erreur quadratique.
    Source: [6], [27]

    Paramètres:
    -----------
    x_data : list/array
        Valeurs de l'entrée (ex: Pression bar).
    y_data : list/array
        Valeurs de la sortie (ex: Tension V).

    Retourne:
    ---------
    a, b : floats (Pente, Offset)
    """
    x = np.array(x_data)
    y = np.array(y_data)
    N = len(x)

    Sx = np.sum(x)
    Sy = np.sum(y)
    Sxx = np.sum(x**2)
    Sxy = np.sum(x * y)

    # Formules manuelles (Cramer/Déterminant)
    # a = (N*Sxy - Sx*Sy) / (N*Sxx - Sx^2)
    # b = (Sxx*Sy - Sx*Sxy) / (N*Sxx - Sx^2)

    Det = N * Sxx - Sx**2
    a = (N * Sxy - Sx * Sy) / Det
    b = (Sxx * Sy - Sx * Sxy) / Det

    print(f"--- Régression Linéaire (y = ax + b) ---")
    print(f"Pente (Sensibilité) a: {a:.4f}")
    print(f"Offset b: {b:.4f}")

    # Calcul erreur max
    y_model = a * x + b
    erreurs = np.abs(y_data - y_model)
    print(f"Erreur Absolue Max sur les points: {np.max(erreurs):.4f}")

    return a, b

# =============================================================================
# EXEMPLES D'UTILISATION (A DECOMMENTER PENDANT L'EXAMEN)
# =============================================================================

if __name__ == "__main__":
    print("\n=== DÉBUT DES TESTS ===\n")

    # --- EXEMPLE 1 : Echantillonnage ---
    # Question : Résolution fréquentielle pour 128 points à 1000 Hz ?
    # calcul_fft_indices(N_points=128, f_echantillonnage=1000)

    # --- EXEMPLE 2 : Erreur Multimètre (Source [1]) ---
    # Lecture = 150V, Gamme = 200V, Précision = 1.5% lecture + 0.5% gamme (fictif pour exemple)
    # erreur_totale_appareil(lecture=150, etendue_max=200, precision_lecture_pct=1.5, precision_gamme_pct=0.5)

    # --- EXEMPLE 3 : Pont de Jauge (Source [2]) ---
    # Alimentation 10V, K=2, 1000 microstrain (1e-3), Quart de pont
    # pont_wheatstone_jauge(U0=10, K=2.0, epsilon=1e-3, type_pont='quart')

    # --- EXEMPLE 4 : Pitot (Source [24]) ---
    # Delta P = 500 Pa
    # tube_pitot_vitesse(delta_P=500, rho_air=1.225)

    # --- EXEMPLE 5 : Piezo (Source [20]) ---
    # Beta = 2.26 pC/N, Ms = 1g, C_tot = 20 pF
    # piezo_accelerometre(beta=2.26e-12, Ms=0.001, C_cable=20e-12, C_ampli=0, acceleration_ms2=9.81)

    # --- EXEMPLE 6 : Régression Linéaire (Source [28]) ---
    # x = [0.5, 1.5, 2.5], y = [0.35, 0.67, 1.14]
    # regression_lineaire_moindres_carres([0.5, 1.5, 2.5], [0.35, 0.67, 1.14])

    # --- EXEMPLE 7 : Distance par écho (Source [7]) ---
    # Lag de 85 echantillons à 48kHz
    # distance_temps_vol(lag_echantillons=85, f_echantillonnage=48000, mode='direct')

    pass