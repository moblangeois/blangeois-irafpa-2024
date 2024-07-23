# Expérimentation sur l'IA générative et l'intégrité académique

Ce dépôt contient le code et les données utilisés pour l'expérimentation décrite dans l'article "Repenser l'intégrité académique à l'ère des systèmes d'IA générative : une approche expérimentale" par Morgan Blangeois.

## Structure du dépôt

- `agents/` : Fichiers de configuration JSON et diagrammes Mermaid des agents IA
  - `analyst.json` : Configuration de l'agent Analyste
  - `gap.json` : Configuration de l'agent Gap
  - `reviewer.json` : Configuration de l'agent Revue
  - `*.mermaid` : Diagrammes des agents
- `data/` : Données d'entrée pour l'expérimentation
  - `data_sample.csv` : Exemple de données pour l'analyse
  - `metaprompt.txt` : Prompt pour la génération de méta-prompts
  - `remove_floating_variables_prompt.txt` : Prompt auxiliaire
- `output/` : Résultats générés par les agents
  - `analysis_output.txt` : Sortie de l'agent Analyste
  - `documents_review.txt` : Revue de documents
  - `gap_output.txt` : Sortie de l'agent Gap
  - `review_output.txt` : Sortie de l'agent Revue
- `functions.py` : Fonctions Python utilisées dans l'expérimentation
- `.gitignore` : Fichiers et dossiers ignorés par Git

## Utilisation

Ce code a été utilisé pour démontrer les capacités des systèmes d'IA générative dans un contexte académique. Il n'est pas destiné à être utilisé pour produire du contenu académique frauduleux.

Pour reproduire l'expérimentation :

1. Installez les dépendances nécessaires (liste à fournir)
2. Configurez les clés API requises pour les modèles d'IA utilisés
3. Exécutez les scripts Python correspondant à chaque agent

Note : Le fichier `main.ipynb` n'est pas inclus dans ce dépôt par mesure de précaution.

## Avertissement

Cette expérimentation vise à explorer les implications éthiques de l'IA générative dans la recherche académique. Elle ne doit pas être utilisée pour contourner les principes d'intégrité académique.

## Contact

Pour toute question concernant cette recherche, veuillez contacter morgan.blangeois@uca.fr.
