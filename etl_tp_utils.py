"""
Module utilitaire pour le traitement des logs Apache.

Ce module contient :
- Une expression régulière pour extraire les champs d'une ligne de log Apache
- Une fonction `parse_log_line` qui retourne un dictionnaire des champs extraits

"""
import re

log_pattern = re.compile(
    r'(?P<ip>\S+) - - \[(?P<datetime>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d+) (?P<size>\S+) "(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'
)

def parse_log_line(line):
    """
    Tente de parser une ligne de log Apache selon le format attendu.
    Args:
        line (str): Une ligne brute du fichier de log.
    Returns:
        dict ou None: Un dictionnaire contenant les champs extraits si la ligne correspond,
                      sinon None.
    """
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    return None
