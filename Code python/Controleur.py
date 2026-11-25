from FootalyzerGUI import FootalyzerGUI
from Championnat import Championnat, Championnat_amical
from Graphe import Graphe

class Controleur:
    """
    Classe qui fait le lien entre l'interface graphique et le modèle.
    Gère la récupération des résultats, classements et graphes pour les championnats.
    """
    def __init__(self):
        """
        Initialise le contrôleur et lance la page d'accueil de l'interface graphique.
        """
        self.fenetre = FootalyzerGUI(self)
        self.fenetre.page_accueil()

    def get_code_ligue(self, pays):
        """
        Retourne le code de ligue correspondant au nom du championnat.
        Args:
            pays (str): Nom du championnat.
        Returns:
            str: Code de la ligue (ex: "FL1" pour Ligue 1).
        """
        ligue_codes = {
            "Ligue 1": "FL1",
            "Premier League": "PL",
            "La Liga": "PD",
            "Bundesliga": "BL1",
            "Serie A": "SA",
            "Eredivisie": "DED",
            "Primeira Liga": "PPL",
            'Campeonato Brasileiro Série A': 'BSA'
        }
        return ligue_codes.get(pays, None)

    def recuperer_resultats(self, pays, annee, journee):
        """
        Récupère la liste des matchs pour un championnat, une année et une journée donnés.
        Args:
            pays (str): Nom du championnat.
            annee (str): Année du championnat (ex: "2024/2025").
            journee (int): Numéro de la journée.
        Returns:
            list: Liste des objets Match pour la journée.
        """
        annee = annee[:4]
        if pays == "Matchs Amicaux" :
            self.championnat_amical = Championnat_amical(annee, pays)
            return self.championnat_amical.predire_resultats()
        else :
            ligue = self.get_code_ligue(pays)
            self.championnat = Championnat(annee, ligue)
            self.championnat.importer_match()
            return self.championnat.resultats(journee)
    
    def recuperer_classement(self, pays, annee):
        """
        Récupère le classement et le dictionnaire des équipes pour un championnat et une année donnés.
        Args:
            pays (str): Nom du championnat.
            annee (str): Année du championnat (ex: "2024/2025").
        Returns:
            tuple: (classement, dico_equipe)
        """
        annee = annee[:4]
        ligue = self.get_code_ligue(pays)
        self.championnat = Championnat(annee, ligue)
        self.championnat.importer_match()
        self.championnat.classement()
        return self.championnat.classement, self.championnat.dico_equipe
    
    def recuperer_graphe(self, pays, annee, equipe):
        """
        Génère le graphe des matchs d'une équipe pour un championnat et une année donnés.
        Args:
            pays (str): Nom du championnat.
            annee (str): Année du championnat (ex: "2024/2025").
            equipe (str): Nom de l'équipe.
        Returns:
            bool or None: True si le graphe a été généré, None si aucun match trouvé.
        """
        annee = annee[:4]
        ligue = self.get_code_ligue(pays)
        self.championnat = Championnat(annee, ligue)
        self.championnat.importer_match()
        matchs_equipe = self.championnat.resultats_equipe(equipe)
        if len(matchs_equipe) == 0:
            return None
        graphe_equipe = Graphe(equipe)

        for match in matchs_equipe:
            if not match.complete:
                continue
            
            graphe_equipe.ajouter_arrete(
                match.equipe_domicile, 
                match.equipe_exterieur, 
                f"{match.but_domicile} - {match.but_exterieur}", 
                match.gagnant()
            )
        graphe_equipe.generer_graphe(f"graphe_{annee}_{ligue}_{equipe}")
        return True

if __name__ == "__main__":
    """
    Point d'entrée du programme : lance l'interface graphique Footalyzer.
    """
    controleur = Controleur()
    controleur.fenetre.mainloop()  # Lancer la boucle principale de l'interface graphique