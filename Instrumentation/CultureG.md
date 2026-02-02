# 📘 Résumé Technique Approfondi (Instrumentation)

## 1. Analyse Fréquentielle & Fenêtrage (Windowing)
**Source :** [1], [2], [3], [4] (Chap 10)

Le fenêtrage est indispensable lorsque le signal analysé n'est pas parfaitement périodique dans la fenêtre d'échantillonnage (discontinuité aux bords = fuites spectrales / leakage).

### Comparatif des Fenêtres
| Fenêtre | Caractéristiques Principales | Usage Recommandé |
| :--- | :--- | :--- |
| **Rectangle** | • Meilleure résolution fréquentielle (pic très fin).<br>• Pire précision d'amplitude (fuites spectrales énormes si non-périodique). | • Signaux transitoires qui s'éteignent avant la fin de la fenêtre.<br>• Signaux parfaitement synchrones/périodiques avec la fenêtre. |
| **Hanning** | • Bon compromis général.<br>• Réduit fortement les lobes secondaires (fuites).<br>• Le pic est plus large que le rectangle. | • **Usage général**.<br>• Discerner un signal faible noyé dans du bruit ou proche d'un fort signal. |
| **Flat-top** | • **Meilleure précision d'amplitude** (<0.1dB).<br>• Pic très large (mauvaise résolution fréquentielle). | • Calibration.<br>• Mesure exacte de l'amplitude d'une sinusoïde (ex: harmoniques). |

*Note : La fenêtre introduit une atténuation globale qui doit être compensée par un facteur de gain lors du calcul.*

---

## 2. Capteurs Inductifs (Focus)
**Source :** [5], [6], [7], [8], [9] (Chap 5)

### Principe
Utilise la variation d'un champ magnétique généré par une bobine. L'inductance $L$ change selon la position d'une cible ferromagnétique.
*   **Formule de base :** $L_x \propto \frac{N^2}{R_{m}(x)}$ (Réluctance variable).

### Variantes
1.  **Réluctance Variable (Sans contact) :** La cible modifie l'entrefer. Relation non-linéaire en $1/x$.
2.  **Plongeur (Noyau mobile) :** Un noyau entre dans la bobine. Meilleure linéarité ($L \propto x$).
3.  **LVDT (Transformateur Différentiel) :** Mesure la différence de tension induite entre deux bobines secondaires. Très précis, sortie nulle au centre [9].

### Avantages & Inconvénients [9]
*   ✅ **Avantages :** Pas de friction (vie illimitée), robuste, insensible à l'huile/poussière.
*   ❌ **Inconvénients :**
    *   Sensible aux métaux environnants.
    *   **Température :** La résistance de la bobine change avec $T^\circ$, affectant la mesure.
    *   **Bande passante limitée :** La fréquence porteuse limite la vitesse de détection.
    *   Hystérésis magnétique possible.

---

## 3. Guide de Choix des Capteurs (Quel capteur pour quoi ?)

### 📏 Mesure de Position / Déplacement
| Besoin | Capteur Recommandé | Pourquoi ? | Sources |
| :--- | :--- | :--- | :--- |
| **Faible coût, statique** | **Potentiomètre** | Simple, mais attention à l'usure et à l'effet de charge ($R_{load}$). | [10], [11] |
| **Haute précision, robuste, rotation** | **Résolver** | Pas d'électronique embarquée, très robuste (avions, industrie lourde), mais nécessite un circuit complexe (Tracking Loop). | [12] |
| **Rotation, Vitesse & Position** | **Codeur Incrémental** | Numérique direct, haute résolution. Attention à la perte de zéro en cas de coupure (sauf si Codeur Absolu). | [13] |
| **Sans contact, courte distance** | **Inductif / Capacitif** | Inductif pour métaux (robuste). Capacitif pour tout matériau (haute résolution mais craint l'humidité). | [5], [14] |

### 🚀 Mesure d'Accélération
| Besoin | Capteur Recommandé | Pourquoi ? | Sources |
| :--- | :--- | :--- | :--- |
| **Vibrations, Haute fréquence** | **Piézoélectrique** | Très rigide, bande passante élevée. **Ne mesure pas le DC** (gravité statique). Nécessite ampli de charge. | [15], [16] |
| **Inclinaison, Smartphone, DC** | **Capacitif (MEMS)** | Mesure le statique (gravité 1g). Faible coût, intégré. | [17] |
| **Haute précision (Navigation)** | **Asservi (Servo)** | Mesure la force de contre-réaction. Très cher, très précis. | [18] |

### 🌡️ Mesure de Température (Labo & Quiz)
| Besoin | Capteur | Propriétés | Sources |
| :--- | :--- | :--- | :--- |
| **Précision & Stabilité** | **Pt100 (RTD)** | Linéaire (assez bien), très stable. Attention à l'auto-échauffement ($P=RI^2$). Connexion 3 ou 4 fils recommandée. | [19], [20] |
| **Sensibilité max** | **NTC** | Variation énorme de R pour petit $\Delta T$. Très non-linéaire (exponentiel). | [21], [22] |

---

## 4. Mesure de Courant & Puissance (Électrique)
**Source :** [23], [24], [25] (Chap 9)

*   **Shunt (Résistance) :** Simple, mais pas d'isolation galvanique et chute de tension.
*   **Sonde de Hall :** Mesure DC et AC. Isolation galvanique totale. Pas de perte d'insertion.
*   **Transformateur de courant (Rogowski/Fluxgate) :** Pour AC seulement (Rogowski) ou AC/DC haute précision (Fluxgate à saturation).
*   **Puissance AC :**
    *   Utiliser la moyenne du produit instantané $u(t) \cdot i(t)$ pour avoir la **Puissance Active (P)**.
    *   $P = U_{eff} I_{eff} \cos \phi$. Si harmoniques présents, $P = \sum P_{harmoniques}$.

---

## 5. Corrélation Croisée (Détection de signal)
**Source :** [26] (Chap 11)

*   **Usage principal :** Mesure de **Temps de Vol** (Distance) ou retrouvailles d'un signal connu dans du bruit.
*   **Mécanisme :** On fait glisser un signal sur l'autre et on multiplie. Le pic indique le retard ($\tau$).
*   **Formule Distance :** $d = \frac{c \cdot \Delta t}{2}$ (pour un écho/aller-retour). $\Delta t$ est trouvé grâce à l'index du pic de corrélation ($k_{peak} / f_s$).
