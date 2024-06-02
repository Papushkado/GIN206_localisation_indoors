#Trilateration

J'ai simplement codé en C et en js les solutions des 4 équations à 3 inconnues

#RSSI

J'ai utilisé : La formule de propagation de log-distance sous cette forme :

RSSI=A−10⋅n⋅log⁡10(d)+X

Où :

    RSSI=A−10⋅n⋅log⁡10(d)+X

    RSSI est la force du signal reçu (en dBm).
    A est la puissance du signal reçu à une distance de référence (en dBm).
    n est l'exposant du chemin, qui dépend des caractéristiques de l'environnement (typiquement entre 2 et 4 en intérieur, et entre 2 et 3 en extérieur).
    d est la distance entre l'émetteur et le récepteur (en mètres).
    X est une variable aléatoire représentant les pertes ou gains supplémentaires.