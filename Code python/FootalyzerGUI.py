import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter

class FootalyzerGUI(tk.Tk):
    """
    Classe principale de l'interface graphique Footalyzer.
    Permet la navigation entre l'accueil, les résultats, le classement et la génération de graphes.
    """

    def __init__(self, controleur):
        """
        Initialise la fenêtre principale et configure le contrôleur.
        Args:
            controleur: Instance du contrôleur principal de l'application.
        """
        super().__init__()
        self.title("Footalyzer")
        self.controleur = controleur
        self.bg_photo = None  # Pour garder une référence à l'image

    def afficher_fond(self, size):
        """
        Affiche une image de fond floutée ou une couleur de secours si l'image n'est pas trouvée.
        Args:
            size (tuple): Taille de la fenêtre (largeur, hauteur).

        Cette méthode a été créé par CHAT GPT.
        Requète : "Créer une méthode pour afficher un fond d'écran flou dans une interface Tkinter.
        Si l'image n'est pas trouvée, afficher une couleur de fond par défaut.
        Elle doit prendre en paramètre la taille de la fenêtre."
        """
        try:
            self.bg_image = Image.open("stade-football.png")
            self.bg_image = self.bg_image.resize(size, Image.Resampling.LANCZOS)
            bg_image_flou = self.bg_image.filter(ImageFilter.GaussianBlur(3))
            self.bg_photo = ImageTk.PhotoImage(bg_image_flou)
            self.background_label = tk.Label(self, image=self.bg_photo)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.background_label.lower()  # Met le fond derrière les autres widgets
        except :
            try:
                self.bg_image = Image.open("Code python/stade-football.png")
                self.bg_image = self.bg_image.resize(size, Image.Resampling.LANCZOS)
                bg_image_flou = self.bg_image.filter(ImageFilter.GaussianBlur(3))
                self.bg_photo = ImageTk.PhotoImage(bg_image_flou)
                self.background_label = tk.Label(self, image=self.bg_photo)
                self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
                self.background_label.lower()  # Met le fond derrière les autres widgets
            except Exception as e:
                print(f"Erreur de chargement du fond : {e}")
                self.configure(bg="#2c3e50")

    def page_accueil(self, event=None):
        """
        Affiche la page d'accueil avec le formulaire de sélection du championnat et de l'année,
        ainsi que les boutons pour accéder aux différentes fonctionnalités.
        Args:
            event: Événement Tkinter (optionnel).
        """
        self.supprimer_widgets()
        self.geometry("390x275")
        self.afficher_fond((390, 275))

        # Titre
        titre = tk.Label(self, text="FOOTALYZER", font=("Arial", 28, "bold"), fg="white", bg="#2c3e50")
        titre.grid(row=0, column=0, pady=20, sticky="n", columnspan=3)

        # Formulaire
        label_championnat = tk.Label(self, text="Championnat :", font=("Arial", 12), fg='white',bg="#2c3e50")
        label_championnat.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.choix_championnat = ttk.Combobox(self, values=["Ligue 1", "Premier League", "La Liga", "Bundesliga", "Serie A", "Matchs Amicaux", "Eredivisie", "Campeonato Brasileiro Série A", "Primeira Liga"], width=28, font=("Arial", 11))
        self.choix_championnat.grid(row=1, column=1, padx=10, pady=5, columnspan=2)

        label_annee = tk.Label(self, text="Année :", font=("Arial", 12), fg='white',bg="#2c3e50")
        label_annee.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.choix_annee = ttk.Combobox(self, values=["2024/2025", "2023/2024"], width=28, font=("Arial", 11))
        self.choix_annee.grid(row=2, column=1, padx=10, pady=5, columnspan=2)

        if event == None :
            self.choix_championnat.current(0)
            self.choix_annee.current(0)
        else :
            self.choix_annee.set(self.annee)
            self.choix_championnat.set(self.pays)

        # Boutons
        bouton_resultat = tk.Button(self, text="Résultats")
        bouton_resultat.grid(row=3, column=0)
        bouton_resultat.bind("<Button-1>", self.afficher_resultats)
        bouton_classement = tk.Button(self, text="Classement")
        bouton_classement.grid(row=3, column=1)
        bouton_graphe = tk.Button(self, text="Graphe équipe")
        bouton_graphe.grid(row=3, column=2)
        bouton_graphe.bind("<Button-1>", self.afficher_graphe_equipe)
        bouton_classement.bind("<Button-1>", self.afficher_classement)
        bouton_quitter = tk.Button(self, text="Quitter")
        bouton_quitter.grid(row=4, column=0, columnspan=3, pady=20)
        bouton_quitter.bind("<Button-1>", self.quitter)

    def afficher_graphe_equipe(self, event=None):
        """
        Affiche la page de génération de graphe pour une équipe sélectionnée.
        Args:
            event: Événement Tkinter (optionnel).
        """
        self.pays = self.choix_championnat.get()
        if self.pays == "Matchs Amicaux":
            tk.messagebox.showerror("Erreur", "Impossible d'afficher un graphe pour des matchs amicaux !")
            return
        self.annee = self.choix_annee.get()
        self.supprimer_widgets()
        self.geometry("390x275")
        self.afficher_fond((390, 275))

        label = tk.Label(self, text="Entrez le nom d'une équipe :")
        label.pack(pady=10)

        self.entree_equipe_graphe = tk.Entry(self)
        self.entree_equipe_graphe.pack()

        btn_afficher = tk.Button(self, text="Générer le graphe", command=self.generer_affichage_graphe)
        btn_afficher.pack(pady=10)

        btn_retour = tk.Button(self, text="Retour")
        btn_retour.bind("<Button-1>", self.page_accueil)
        btn_retour.pack()
    
    def generer_affichage_graphe(self):
        """
        Génère et affiche le graphe des rencontres pour l'équipe saisie par l'utilisateur.
        Affiche un message d'erreur si l'équipe n'est pas trouvée ou en cas d'échec.
        """
        equipe = self.entree_equipe_graphe.get().strip()
        if not equipe:
            tk.messagebox.showerror("Erreur", "Veuillez entrer un nom d'équipe.")
            return
        
        try:
            result = self.controleur.recuperer_graphe(self.pays, self.annee, equipe)
            if result is None:
                tk.messagebox.showerror("Erreur", f"Aucun match trouvé pour l'équipe {equipe} dans le championnat {self.pays} pour l'année {self.annee}.")
                return
            #tk.messagebox.showinfo("Succès", f"Graphe pour l'équipe {equipe} généré avec succès.")
        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Impossible de générer le graphe : {e}")

    def afficher_resultats(self, event=None):
        """
        Affiche la page des résultats pour le championnat, l'année et la journée sélectionnés.
        Permet de naviguer entre les journées avec une Spinbox.
        Args:
            event: Événement Tkinter (optionnel).
        """
        if event is not None:
            self.pays = self.choix_championnat.get()
            self.annee = self.choix_annee.get()
            self.journee = 1
        self.supprimer_widgets()

        if self.pays == "Matchs Amicaux":
            self.geometry("750x440")
            self.afficher_fond((750, 440))
            titre = tk.Label(self, text="Prédiction des résultats des Matchs Amicaux", font=("Arial", 24, "bold"), fg="white", bg="#2c3e50")
            titre.pack(pady=20)

        else:
            self.geometry("630x780")
            self.afficher_fond((630, 780))

            # Titre
            titre = tk.Label(self, text="Résultats", font=("Arial", 24, "bold"), fg="white", bg="#2c3e50")
            titre.pack(pady=20)

            # Sélecteur de journée avec Spinbox
            frame_journee = tk.Frame(self, bg="#2c3e50")
            frame_journee.pack(pady=(0, 15))
            label_journee = tk.Label(frame_journee, text="Journée :", font=("Arial", 12), fg="white", bg="#2c3e50")
            label_journee.pack(side="left", padx=(0, 5))
            self.spin_journee = tk.Spinbox(frame_journee, from_=1, to=38, width=5, font=("Arial", 11))
            self.spin_journee.pack(side="left")
            self.spin_journee.delete(0, "end")
            self.spin_journee.insert(0, self.journee)

            bouton_afficher = tk.Button(frame_journee, text="Afficher", command=self.rafraichir_resultats)
            bouton_afficher.pack(side="left", padx=(10, 0))

        # Conteneur pour les matchs (stocké comme attribut)
        self.matches_container = tk.Frame(self)
        self.matches_container.pack(fill="both", expand=True)

        self.rafraichir_resultats()  # Affiche les matchs pour la journée courante

        btn_retour = tk.Button(self, text="Retour")
        btn_retour.bind("<Button-1>", self.page_accueil)
        btn_retour.pack(pady=20)

    def rafraichir_resultats(self):
        """
        Rafraîchit l'affichage des résultats pour la journée sélectionnée dans la Spinbox.
        Efface les anciens matchs et affiche les nouveaux.
        """
        # Efface uniquement les anciens matchs
        for widget in self.matches_container.winfo_children():
            widget.destroy()
        if self.pays == "Matchs Amicaux":
            self.journee = 1
        else:
            self.journee = int(self.spin_journee.get())
        resultats = self.controleur.recuperer_resultats(self.pays, self.annee, self.journee)
        for match in resultats:
            self.display_match(match, self.matches_container)

    def display_match(self, match, parent):
        """
        Affiche un match sous forme de boîte compacte dans le conteneur parent.
        Args:
            match: Objet Match à afficher.
            parent: Widget parent dans lequel afficher le match.

        Cette méthode a été créé par CHAT GPT.
        Requète : "Créer une méthode pour afficher un match de football dans une interface Tkinter.
        L'affichage doit être compact, sans emoji, avec des noms d'équipes plus grands et un score au centre.
        La date doit être affichée en dessous du score dans un format lisible."
        """
        from datetime import datetime

        frame = tk.Frame(parent, bd=1, relief="solid", padx=3, pady=3)
        frame.pack(fill="x", padx=10, pady=3, ipady=1)

        row = tk.Frame(frame, bg="white")
        row.pack()

        # Récupération avec valeurs par défaut
        domicile = match.equipe_domicile or "Équipe 1"
        exterieur = match.equipe_exterieur or "Équipe 2"
        but_dom = match.but_domicile if match.but_domicile is not None else "-"
        but_ext = match.but_exterieur if match.but_exterieur is not None else "-"
        score = f"{but_dom} - {but_ext}"

        # Affichage équipes et score (sans emoji, noms plus grands)
        tk.Label(row, text=domicile, font=("Helvetica", 13, "bold"), bg="white", fg="black").grid(row=0, column=0, padx=10)
        tk.Label(row, text=score, font=("Helvetica", 15, "bold"), bg="white", fg="black").grid(row=0, column=1, padx=10)
        tk.Label(row, text=exterieur, font=("Helvetica", 13, "bold"), bg="white", fg="black").grid(row=0, column=2, padx=10)

        # Conversion et affichage de la date
        try:
            dt = datetime.strptime(match.date, "%Y-%m-%dT%H:%M:%SZ")
            date_affichee = dt.strftime("%d %b %Y à %Hh%M")
        except Exception:
            date_affichee = match.date or ""

        tk.Label(frame, text=date_affichee, font=("Helvetica", 8), bg="white", fg="#333").pack(pady=(2, 0))

    def afficher_classement(self, event):
        """
        Affiche la page du classement du championnat sélectionné.
        Affiche un tableau avec les statistiques de chaque équipe.
        Args:
            event: Événement Tkinter.
        """
        self.pays = self.choix_championnat.get()
        if self.pays == "Matchs Amicaux" :
            tk.messagebox.showerror("Erreur", "Impossible d'afficher un classement pour des matchs amicaux !")
            return
        self.annee = self.choix_annee.get()
        self.supprimer_widgets()
        self.geometry("1040x800")
        self.afficher_fond((1040, 800))

        # Titre
        titre = tk.Label(self, text="CLASSEMENT", font=("Arial", 24, "bold"), fg="white", bg="#2c3e50")
        titre.pack(pady=20)
        
        classement, info_equipe = self.controleur.recuperer_classement(self.pays, self.annee)

        # Tableau
        """
        Ce Tableau a été créé par CHAT GPT.
        Requète : "Créer un tableau Tkinter pour afficher le classement d'un championnat de football."
        """
        colonnes = ["Position", "Équipe", "Points", "GA", "Victoires", "Nuls", "Défaites", "Buts Marqués", "Buts Encaissés"]
        tableau = ttk.Treeview(self, columns=colonnes, show="headings", height=20)
        tableau.pack(pady=20)
        for col in colonnes:
            tableau.heading(col, text=col)
            if col == "Équipe":
                tableau.column(col, anchor="w", width=180)
            else :
                tableau.column(col, anchor="center", width=100)
        
        style = ttk.Style(self)
        style.configure("Treeview", rowheight=25)
        style.map("Treeview", background=[('selected', '#b3d9ff')])
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Lignes alternées
        tableau.tag_configure('oddrow', background='#f0f0f0')
        tableau.tag_configure('evenrow', background='#ffffff')

        for i, equipe in enumerate(classement):
            position = i + 1
            stats = info_equipe[equipe]
            ligne = (
                equipe,
                stats.get("points", 0),
                stats.get("buts marqués", 0) - stats.get("buts encaissés", 0),
                stats.get("victoires", 0),
                stats.get("nuls", 0),
                stats.get("defaites", 0),
                stats.get("buts marqués", 0),
                stats.get("buts encaissés", 0)
            )
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tableau.insert("", "end", values=(position, *ligne), tags=(tag,))

        btn_retour = tk.Button(self, text="Retour")
        btn_retour.bind("<Button-1>", self.page_accueil)
        btn_retour.pack(pady=20)

    def supprimer_widgets(self):
        """
        Détruit tous les widgets enfants de la fenêtre principale.
        Permet de réinitialiser l'affichage lors d'un changement de page.
        """
        for widget in self.winfo_children():
            widget.destroy()

    def quitter(self, event):
        """
        Ferme proprement l'application Footalyzer.
        Args:
            event: Événement Tkinter.
        """
        self.destroy()