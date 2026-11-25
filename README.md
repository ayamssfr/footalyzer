# ⚽ Footalyzer

## 🎯 Contexte et objectif du projet :

Footalyzer est une application développée en Python dans le cadre d’un projet ISN. Elle permet d’analyser les résultats passés des matchs de football des cinq grands championnats européens (Ligue 1, Premier League, Bundesliga, Serie A et La Liga) à partir de fichiers json. L’objectif est également d’introduire un algorithme de prédiction simple pour estimer les résultats futurs. L'application propose une interface graphique intuitive et interactive conçue avec la bibliothèque Tkinter.

## 🛠️ Liste des fonctionnalités :

- 📂 Importation des données : lecture automatique des résultats depuis des fichiers json.
- 📊 Calculs statistiques : classement automatique, performances à domicile/extérieur, nombre de buts marqués/encaissés.
- 📈 Visualisation graphique : affichage de classements, affichage des résultats, création d'un graphe des performances par équipe.
- 🤖 Algorithme prédictif : proposition d’un modèle de prédiction simplifié des résultats futurs.

## Tutoriel

- Sur la page d’accueil, sélectionnez un **championnat** et une **année**.  
  Cliquez ensuite sur **"Résultats"** pour afficher les résultats, **"Classement"** pour consulter le classement, ou **"Graphe Équipe"** pour accéder au menu des graphes par équipe.
- Dans la page **Résultats**, vous pouvez choisir la **journée** à l’aide du compteur, puis cliquer sur **"Afficher"** pour visualiser les résultats de cette journée.  
  Le bouton **"Retour"** permet de revenir à la page d’accueil.
- Dans la page **Classement**, vous pouvez consulter le **classement du championnat sélectionné**, accompagné de toutes les statistiques calculées par notre programme.  
  Le bouton **"Retour"** permet également de revenir à l’accueil.
- Dans la page **Graphe Équipe**, entrez le **nom d’une équipe** du championnat sélectionné, puis cliquez sur **"Générer"** pour afficher le graphe représentant les **victoires, matchs nuls et défaites** de l’équipe.
- Si vous sélectionnez le championnat **"Match Amical"**, vous pourrez consulter les **résultats prédits par notre algorithme** pour **5 matchs** issus des **5 grands championnats européens**.  
  Les fonctionnalités **Classement** et **Graphe Équipe** ne sont pas disponibles pour ce championnat.
  
📌 Footalyzer vise à offrir une expérience informative et agréable aux amateurs de football souhaitant explorer les données et tendances des championnats européens.

## Installation

```bash
pip install -r requirements.txt
python "Code python/Controleur.py"   # à lancer depuis la racine du projet
```

Le graphe par équipe utilise aussi [Graphviz](https://graphviz.org/download/), à installer sur la machine.

Les données des championnats déjà présentes dans `data/` sont lues directement. Pour en télécharger d'autres depuis l'API [football-data.org](https://www.football-data.org/), crée une clé gratuite et mets-la dans la variable d'environnement `FOOTBALL_DATA_TOKEN`.

## Équipe

Projet réalisé en équipe de 4 sur un mois (prépa intégrée, INSA Lyon), dont Aya Messafri.
