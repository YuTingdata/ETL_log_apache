#  Pipeline ETL pour logs Apache

Ce projet met en place un pipeline ETL (Extract, Transform, Load) simple pour traiter des journaux d'accès Apache.  
Il télécharge les logs depuis une URL publique, détecte les nouvelles lignes, les parse, les transforme, et les sauvegarde dans des fichiers CSV quotidiens.

---

## Structure du projet

.
├── etl_tp_main.py # Script principal pour télécharger, parser et sauvegarder les logs
├── etl_tp_utils.py # Module utilitaire avec la regex et la fonction de parsing
├── apache_logs.txt # Fichier accumulant les lignes de log déjà vues
├── logs_YYYY-MM-DD.csv # Fichiers CSV générés, un par jour
└── README.md 


---

##  Fonctionnalités

- Téléchargement de logs Apache depuis une source distante  
- Traitement uniquement des nouvelles lignes (évite les doublons)  
- Parsing des logs en données structurées via expressions régulières  
- Conversion des dates, codes HTTP, et tailles  
- Identification des erreurs (codes HTTP ≥ 400)  
- Sauvegarde groupée par date dans des fichiers CSV

---

##  Prérequis

- Python 3.9+
- Bibliothèques : `pandas`, `requests`

Installation des dépendances :

```bash
pip install pandas requests

##  Exécution
    - Clone ou télécharge le projet
    - Lance le script principal :

python etl_tp_main.py

Ce script :
    - Télécharge les derniers logs
    - Ajoute les nouvelles lignes à apache_logs.txt
    - Parse et transforme les données
    - Génère ou met à jour les fichiers CSV comme logs_2025-06-01.csv


##  Auteur
HUANG Yu-Ting
TP ETL – Analyse de logs Apache
