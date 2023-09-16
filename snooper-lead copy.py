import subprocess
import csv
import re
import os
from urllib.request import urlopen, Request
import urllib.error
from bs4 import BeautifulSoup
import argparse
import ssl

# Fonction pour extraire les adresses e-mail à partir d'un site web
def extract_emails_from_website(url):
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        # Connect to source URL
        context = ssl.SSLContext()
        req = Request(url, headers={'User-Agent': user_agent}, method='GET')
        html = urlopen(req, context=context).read()
        bsObj = BeautifulSoup(html, 'lxml')

        emails = set()


        for link in bsObj.findAll("a", href=re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")):
            if 'href' in link.attrs:
                newPage = link.attrs['href']
                try:
                    # Connect to all links one by one
                    req1 = Request(newPage, headers={'User-Agent': user_agent}, method='GET')
                    html1 = urlopen(req1, context=context).read()
                    bsObj1 = BeautifulSoup(html1, 'lxml').get_text()
                    # Find Emails in those links
                    match = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", bsObj1)
                    emails.update(match)
                except Exception as e:
                    print(f"Erreur lors de la récupération des e-mails à partir de {newPage}: {e}")

        return emails

    except urllib.error.HTTPError as e:
        print(f"[!] HTTP Error [!]\n[?] Error Code: {e.code} [?]")
        return set()

# Demande à l'utilisateur de saisir la requête
query = input("Entrez votre requête : ")

# Demande à l'utilisateur de saisir le navigateur
browser_type = input("Entrez le navigateur à utiliser (baidu, bing, duckduckgo, google, yahoo, all) : ")

# Demande à l'utilisateur de saisir le nombre de résultats à explorer
num_results = input("Entrez le nombre de résultats à explorer : ")

# Commande pydork avec les paramètres entrés par l'utilisateur
command = f"pydork search -s -n {num_results} -t {browser_type} -- '{query}'"

# Exécute la commande et récupère la sortie
output = subprocess.check_output(command, shell=True, text=True)

# Divise la sortie en lignes
lines = output.splitlines()

# Crée un dictionnaire pour stocker les adresses e-mail par site web
email_dict = {}

# Parcourt les lignes de la sortie de pydork
for line in lines:
    # Vérifie si la ligne commence par [GoogleSearch], ce qui indique un lien
    if line.startswith('[GoogleSearch]: '):
        # Extrait l'URL en supprimant le préfixe [GoogleSearch]:
        url = line[len('[GoogleSearch]: '):]
        # Extrait les adresses e-mail à partir du site web
        emails = extract_emails_from_website(url)
        # Stocke les adresses e-mail dans le dictionnaire
        email_dict[url] = emails

# Crée un fichier CSV pour stocker les résultats
with open('resultats.csv', 'w', newline='') as csvfile:
    # Crée un objet CSV writer
    csvwriter = csv.writer(csvfile)
    
    # Écrit les résultats dans le fichier CSV
    for url, emails in email_dict.items():
        csvwriter.writerow([url, ', '.join(emails)])

print("Résultats stockés dans resultats.csv")
