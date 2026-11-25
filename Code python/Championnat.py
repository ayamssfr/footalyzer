import requests
import json
from Match import Match
from datetime import datetime
from random import randint
from Probabilite import Probabilite
import os

class Championnat :
    def __init__(self, annee, ligue):
        """
        Initialise un championnat avec une année et une ligue.
        Args:
            annee (str): Année du championnat (ex: "2024").
            ligue (str): Code de la ligue (ex: "FL1").
        """
        self.liste_matchs = []
        self.annee = annee
        self.ligue = ligue
        self.dico_equipe = {}

    def __str__(self):
        """
        Affiche tous les matchs du championnat.
        """
        for match in self.liste_matchs:
            print(match)

    def ajouter_match(self, match):
        """
        Ajoute un objet Match à la liste des matchs du championnat.
        Args:
            match (Match): Objet Match à ajouter.
        """
        self.liste_matchs.append(match)
            
    def importer_match(self):
        """
        Importe les matchs du championnat depuis un fichier JSON local si disponible,
        sinon depuis l'API football-data.org, puis sauvegarde les données localement.
        Remplit la liste des matchs et le dictionnaire des équipes.
        """
        chemin = f"data/{self.ligue}-{self.annee}.json"
        if os.path.exists(chemin):
            with open(chemin, "r", encoding="utf-8") as f:
                data = json.load(f)
            matchs = data.get('matches', [])
        else:
            url = f'https://api.football-data.org/v4/competitions/{self.ligue}/matches?season={self.annee}'
            fichier = requests.get(url, headers={'X-Auth-Token': os.environ.get('FOOTBALL_DATA_TOKEN', '')})
            if fichier.status_code != 200:
                print("❌ Erreur :", fichier.status_code)
                exit()
            data = fichier.json()
            matchs = data.get('matches', [])
            # Sauvegarde pour la prochaine fois
            os.makedirs("data", exist_ok=True)
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        for match in matchs :
            equipe_domicile = match['homeTeam']['name']
            if equipe_domicile not in self.dico_equipe:
                self.dico_equipe[equipe_domicile] = {'url_logo': match['homeTeam']['crest']}
            equipe_exterieur = match['awayTeam']['name']
            if equipe_exterieur not in self.dico_equipe:
                self.dico_equipe[equipe_exterieur] = {'url_logo': match['awayTeam']['crest']}
            complete = match['status'] == 'FINISHED'
            if complete:
                score_domicile = match['score']['fullTime']['home']
                score_exterieur = match['score']['fullTime']['away']
            else :
                score_domicile = None
                score_exterieur = None
            journee = match['matchday']
            date_match = match['utcDate']
            self.ajouter_match(Match(equipe_domicile, equipe_exterieur, score_domicile, score_exterieur, date_match, journee, complete))

    def resultats(self, journee):
        """
        Retourne la liste des matchs correspondant à une journée donnée.
        Args:
            journee (int): Numéro de la journée.
        Returns:
            list: Liste des objets Match de la journée.
        """
        resultats = []
        for match in self.liste_matchs:
            if match.journee == journee :
                resultats.append(match)
        return resultats
        
    def classement(self):
        """
        Calcule et trie le classement des équipes selon les points, la différence de buts et les buts marqués.
        Met à jour le dictionnaire des équipes avec les statistiques.
        """
        classement = []
        for match in self.liste_matchs:
            if match.complete :
                gagnant = match.gagnant()
                if match.equipe_domicile not in classement:
                    classement.append(match.equipe_domicile)
                if match.equipe_exterieur not in classement:
                    classement.append(match.equipe_exterieur)

                self.dico_equipe[match.equipe_domicile]['buts marqués'] = self.dico_equipe[match.equipe_domicile].get('buts marqués', 0) + match.but_domicile
                self.dico_equipe[match.equipe_exterieur]['buts marqués'] = self.dico_equipe[match.equipe_exterieur].get('buts marqués', 0) + match.but_exterieur
                self.dico_equipe[match.equipe_exterieur]['buts encaissés'] = self.dico_equipe[match.equipe_exterieur].get('buts encaissés', 0) + match.but_domicile
                self.dico_equipe[match.equipe_domicile]['buts encaissés'] = self.dico_equipe[match.equipe_domicile].get('buts encaissés', 0) + match.but_exterieur
                if gagnant == match.equipe_domicile:
                    self.dico_equipe[match.equipe_domicile]['points'] = self.dico_equipe[match.equipe_domicile].get('points',0) + 3
                    self.dico_equipe[match.equipe_domicile]['victoires'] = self.dico_equipe[match.equipe_domicile].get('victoires',0) + 1
                    self.dico_equipe[match.equipe_exterieur]['defaites'] = self.dico_equipe[match.equipe_exterieur].get('defaites',0) + 1
                elif gagnant == match.equipe_exterieur:
                    self.dico_equipe[match.equipe_exterieur]['points'] = self.dico_equipe[match.equipe_exterieur].get('points',0) + 3
                    self.dico_equipe[match.equipe_exterieur]['victoires'] = self.dico_equipe[match.equipe_exterieur].get('victoires',0) + 1
                    self.dico_equipe[match.equipe_domicile]['defaites'] = self.dico_equipe[match.equipe_domicile].get('defaites',0) + 1
                else :
                    self.dico_equipe[match.equipe_exterieur]['points'] = self.dico_equipe[match.equipe_exterieur].get('points',0) + 1
                    self.dico_equipe[match.equipe_domicile]['points'] = self.dico_equipe[match.equipe_domicile].get('points',0) + 1
                    self.dico_equipe[match.equipe_exterieur]['nuls'] = self.dico_equipe[match.equipe_exterieur].get('nuls',0) + 1
                    self.dico_equipe[match.equipe_domicile]['nuls'] = self.dico_equipe[match.equipe_domicile].get('nuls',0) + 1
               
        self.classement = sorted(classement, key=lambda x: (self.dico_equipe[x]['points'], self.dico_equipe[x]['buts marqués'] - self.dico_equipe[x]['buts encaissés'],self.dico_equipe[x]['buts marqués']), reverse=True)
    
    def resultats_equipe(self, equipe):
        """
        Retourne la liste des matchs joués par une équipe donnée.
        Args:
            equipe (str): Nom de l'équipe.
        Returns:
            list: Liste des objets Match joués par l'équipe.
        """
        resultats = []
        for match in self.liste_matchs:
            if match.equipe_domicile == equipe or match.equipe_exterieur == equipe:
                resultats.append(match)
        return resultats
    
class Championnat_amical(Championnat):
    def __init__(self, annee, ligue):
        """
        Initialise un championnat amical avec des matchs fictifs.
        Args:
            annee (str): Année du championnat.
            ligue (str): Code de la ligue.
        """
        super().__init__(annee, ligue)
        date = datetime(2025, 7, 4, 20, 30).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.ajouter_match(Match("FC Barcelona", "Villareal CF", None, None, date, 1, False))
        self.ajouter_match(Match("AS Monaco FC", "Olympique Lyonnais", None, None, date, 1, False))
        self.ajouter_match(Match("Borussia Dortmund", "RB Leipzig", None, None, date, 1, False))
        self.ajouter_match(Match("AC Milan", "FC Internazionale Milano", None, None, date, 1, False))
        self.ajouter_match(Match("Everton FC", "Fulham FC", None, None, date, 1, False))
        
    def predire_resultats(self):
        """
        Prédit les scores des matchs amicaux à l'aide du modèle de Poisson
        basé sur les données de plusieurs championnats et années.
        Retourne la liste des matchs avec les scores prédits.
        Returns:
            list: Liste des objets Match avec scores prédits.
        """
        donnees = []
        championnat = ["FL1", "PL", "PD", "BL1", "SA"]
        annee = ["2023","2024"]
        for i in championnat:
            for j in annee:
                championnat = Championnat(j, i)
                championnat.importer_match()
                donnees.append(championnat.liste_matchs)
        proba = Probabilite(donnees)
                proba = Probabilite(donnees)
        for match in self.liste_matchs :
            score, confiance = proba.predire_score_poisson(match.equipe_domicile, match.equipe_exterieur)
            match.but_domicile = score[0]
            match.but_exterieur = score[1]
            print(confiance)
        return self.liste_matchs
    
if __name__ == "__main__":
    championnat = Championnat("2024", "FL1")
    championnat.importer_match()
    for match in championnat.liste_matchs:
        print(match.date)
        break