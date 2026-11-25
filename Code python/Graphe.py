from graphviz import Graph

dot = Graph(format='png', engine='dot')

class Graphe :
    def __init__(self, equipe):
        """
        Initialise un objet Graphe pour une équipe donnée.
        Args:
            equipe (str): Nom de l'équipe centrale du graphe.
        """
        self.dot = Graph(format='png', engine='circo')
        self.equipe = equipe
    
    def ajouter_arrete(self, sommet1, sommet2, score, gagnant):
        """
        Ajoute une arête entre deux sommets avec un label score et une couleur selon le gagnant.
        Args:
            sommet1 (str): Nom du sommet de départ (équipe 1).
            sommet2 (str): Nom du sommet d'arrivée (équipe 2).
            score (str): Score du match (ex: "2 - 1").
            gagnant (str or None): Nom du gagnant ou None si match nul.
        """
        if gagnant == self.equipe:
            couleur = 'green'
        elif gagnant is None:
            couleur = 'black'
        else:
            couleur = 'red'
        self.dot.edge(sommet1, sommet2, label=score, color=couleur)

    def generer_graphe(self, nom_fichier):
        """
        Génère et enregistre le graphe au format PNG dans le dossier data.
        Args:
            nom_fichier (str): Nom du fichier de sortie (sans extension).
        """
        self.dot.attr(overlap='false', splines='true')
        self.dot.render(f"data/{nom_fichier}", view=True)
