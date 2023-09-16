import subprocess
import csv

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

# Crée un fichier CSV pour stocker les résultats
with open('resultats.csv', 'w', newline='') as csvfile:
    # Crée un objet CSV writer
    csvwriter = csv.writer(csvfile)
    
    # Parcourt les lignes de la sortie de pydork
    for line in lines:
        # Vérifie si la ligne commence par [GoogleSearch], ce qui indique un lien
        if line.startswith('[GoogleSearch]: '):
            # Extrait l'URL en supprimant le préfixe [GoogleSearch]: 
            url = line[len('[GoogleSearch]: '):]
            # Écrit l'URL dans le fichier CSV
            csvwriter.writerow([url])

print("Résultats stockés dans resultats.csv")
