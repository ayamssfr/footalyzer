class Match:
    def __init__(self, equipe_domicile, equipe_exterieur, but_domicile, but_exterieur, date, journee, complete):
        """
        Initialise une instance de la classe Match.

        Args:
            equipe_domicile (str): Le nom de l'équipe jouant à domicile.
            equipe_exterieur (str): Le nom de l'équipe jouant à l'extérieur.
            but_domicile (int): Le nombre de buts marqués par l'équipe à domicile.
            but_exterieur (int): Le nombre de buts marqués par l'équipe à l'extérieur.
            date (Date): La date du match.
            journee (int): Le numéro de la journée du championnat.
            complete (bool): Indique si le match est terminé (True) ou non (False).
        """
        self.equipe_domicile = equipe_domicile
        self.equipe_exterieur = equipe_exterieur
        self.but_domicile = but_domicile
        self.but_exterieur = but_exterieur
        self.date = date
        self.journee = journee
        self.complete = complete
    
    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères du match.

        Returns:
            str: Une chaîne décrivant le match au format 
                 "équipe_domicile but_domicile - but_exterieur équipe_exterieur (date)".
        """
        return f"{self.equipe_domicile} {self.but_domicile} - {self.but_exterieur} {self.equipe_exterieur} ({self.date})"
    
    def gagnant(self):
        """
        Détermine le gagnant du match.

        Returns:
            str: Le nom de l'équipe gagnante (équipe_domicile ou équipe_exterieur).
            None: Si le match est un match nul.

        Raises:
            ValueError: Si le match n'est pas encore terminé (complete est False).
        """
        if self.complete == False:
            raise ValueError("Le match n'est pas encore terminé.")
        if self.but_domicile > self.but_exterieur:
            return self.equipe_domicile
        elif self.but_domicile < self.but_exterieur:
            return self.equipe_exterieur
        else:
            return None
        
    def score(self):
        """
        Retourne le score du match.
        
        Returns:
            str: Le score du match au format "but_domicile - but_exterieur".

        """
        return f"{self.but_domicile} - {self.but_exterieur}"