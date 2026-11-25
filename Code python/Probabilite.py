import numpy as np
from scipy.stats import poisson
from Match import Match

class Probabilite:
    """
    Classe permettant de calculer les scores Elo et de prédire les scores de matchs à l'aide de la loi de Poisson.
    """

    def __init__(self, donnees):
        """
        Initialise la classe Probabilite avec une liste de listes de matchs.
        Calcule les scores Elo pour chaque équipe.
        Args:
            donnees (list): Liste de listes d'objets Match.
        """
        self.matchs = []
        for liste_match in donnees :
            for match in liste_match:
                self.matchs.append(match)
        self.elo = {}
        self.calculer_elo()

    def calculer_elo(self):
        """
        Calcule le score Elo de chaque équipe à partir de la liste des matchs.
        Prend en compte l'avantage de jouer à domicile.
        """
        # Donne 1500 points Elo à chaque équipe
        for match in self.matchs:
            for equipe in [match.equipe_domicile, match.equipe_exterieur]:
                if equipe not in self.elo:
                    self.elo[equipe] = 1500

        for match in self.matchs:
            if match.complete :
                e1, e2 = match.equipe_domicile, match.equipe_exterieur
                s1, s2 = match.but_domicile, match.but_exterieur
                lieu = match.equipe_domicile  # Lieu du match, équipe qui reçoit
                # on considère l'avantage de jouer a domicile
                elo1 = self.elo[e1]
                elo2 = self.elo[e2]
                if lieu == e1 :
                    elo1 += 100 
                elif lieu == e2 : 
                    elo2 +=  100

                proba1 = 1 / (1 + 10 ** ((elo2 - elo1) / 400))

                # Résultat du match : 1 (victoire), 0.5 (nul), 0 (défaite)
                if s1 > s2:
                    resultat = 1
                elif s1 < s2:
                    resultat = 0
                else:
                    resultat = 0.5
                # k est un facteur qui contrôle l’impact d’un match
                k = 20
                # Modification des scores Elo en fonction du résultat du match
                self.elo[e1] += k * (resultat - proba1)
                self.elo[e2] += k * ((1 - resultat) - (1 - proba1))

    def _moyenne_buts(self, equipe):
        """
        Calcule la moyenne de buts marqués par une équipe sur l'ensemble des matchs complets.
        Args:
            equipe (str): Nom de l'équipe.
        Returns:
            float: Moyenne de buts marqués.
        """
        buts = []
        for match in self.matchs :
            if match.complete : 
                if match.equipe_domicile == equipe:
                    buts.append(match.but_domicile)
                elif match.equipe_exterieur == equipe:
                    buts.append(match.but_exterieur)
        return np.mean(buts) if buts else 1

   def predire_score_poisson(self, e1, e2, echelle=1600):
    """
    Prédit le score le plus probable en combinant Elo et loi de Poisson.
    Les moyennes de buts sont ajustées selon l'écart d'Elo (avantage domicile inclus).
    Args:
        e1 (str): équipe à domicile.
        e2 (str): équipe à l'extérieur.
        echelle (int): plus elle est petite, plus l'Elo pèse dans la prédiction.
    Returns:
        tuple: (score le plus probable, probabilité associée)
    """
    moy1 = self._moyenne_buts(e1)
    moy2 = self._moyenne_buts(e2)

    # Écart d'Elo avec avantage du terrain
    diff = (self.elo.get(e1, 1500) + 100) - self.elo.get(e2, 1500)
    facteur = 10 ** (diff / echelle)   # ex : +200 d'Elo -> facteur ~1.33

    lambda1 = moy1 * facteur   # l'équipe la plus forte marque plus
    lambda2 = moy2 / facteur   # l'autre marque moins

    meilleur_score = (0, 0)
    meilleure_proba = 0
    for X1 in range(6):
        for X2 in range(6):
            p = poisson.pmf(X1, lambda1) * poisson.pmf(X2, lambda2)
            if p > meilleure_proba:
                meilleure_proba = p
                meilleur_score = (X1, X2)

    return meilleur_score, round(meilleure_proba, 2)

        return meilleur_score, round(meilleure_proba, 2)

    def predire_match(self, e1, e2, echelle=1600):
        """
        Prédit le résultat d'un match entre deux équipes en combinant la probabilité Elo et la prédiction Poisson.
        Args:
            e1 (str): Nom de l'équipe à domicile.
            e2 (str): Nom de l'équipe à l'extérieur.
        Returns:
            dict: Dictionnaire contenant la probabilité Elo, le score prédit et la confiance.
        """
        elo1 = self.elo.get(e1, 1500)# get car peut etre qu'une équipe n'a pas encore joué
        elo2 = self.elo.get(e2, 1500)
       # on oublie pas de reconsidèrer l'avantage de jouer à domicile
        elo1 += 100 

        proba_elo = 1 / (1 + 10 ** ((elo2 - elo1) / 400))
        score, confiance = self.predire_score_poisson(e1, e2)

        return {
            "proba_elo": round(proba_elo, 2),
            "score_pred": score,
            "confiance": confiance
        }
