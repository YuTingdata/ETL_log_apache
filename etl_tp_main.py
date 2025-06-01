"""
Script ETL pour les logs Apache.

Ce script :
- Télécharge les logs depuis une URL
- Détecte les nouvelles lignes non encore traitées
- Parse les lignes pour extraire les champs utiles
- Transforme les données (datetime, status, taille, etc.)
- Regroupe les entrées par date et les enregistre en fichiers CSV quotidiens
"""

import os
import sys
import requests
import pandas as pd
from datetime import datetime

from etl_tp_utils import parse_log_line


# Télécharger le fichier log

url = "https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/apache_logs/apache_logs"
response = requests.get(url)
new_lines = response.text.splitlines()

# Lire les anciennes lignes si elles existent
if os.path.exists("apache_logs.txt"):
    with open("apache_logs.txt", "r", encoding="UTF-8") as f:
        old_lines = f.read().splitlines()
else:
    old_lines = []

# Déduire les lignes nouvelles
old_lines_set = set(old_lines)  # fast lookup
lines_to_process = [line for line in new_lines if line not in old_lines_set]
# lines_to_process = [line for line in new_lines if line not in old_lines]

# Ajouter les nouvelles lignes au fichier principal
with open("apache_logs.txt", "a") as f:
    for line in lines_to_process:
        f.write(line + "\n")

print(f" {len(lines_to_process)} nouvelles lignes à traiter.")

# Parser les lignes
parsed_data = []
for line in lines_to_process:
    parsed = parse_log_line(line)
    if parsed:
        parsed_data.append(parsed)

# Créer un DataFrame
df = pd.DataFrame(parsed_data)

if df.empty:
    print(" Aucune nouvelle donnée à enregistrer.")
    sys.exit()

# Nettoyer et transformer

# Convertit les chaînes de caractères en objets datetime (ex: '10/Oct/2000:13:55:36 -0700')
df['datetime'] = pd.to_datetime(df['datetime'], format="%d/%b/%Y:%H:%M:%S %z", errors='coerce')
df['date'] = df['datetime'].dt.date
df['status'] = df['status'].astype(int)
df['size'] = pd.to_numeric(df['size'], errors='coerce').fillna(0)
# Identifie les requêtes en erreur (code HTTP ≥ 400)
df['is_error'] = df['status'] >= 400

# Fusionner avec les fichiers CSV existants par date
for date, group in df.groupby("date"):
    filename = f"logs_{date}.csv"
    if os.path.exists(filename):
        old_df = pd.read_csv(filename)
        combined_df = pd.concat([old_df, group]).drop_duplicates()
    else:
        combined_df = group
    combined_df.to_csv(filename, index=False)
    print(f"Fichier mis à jour : {filename}")
