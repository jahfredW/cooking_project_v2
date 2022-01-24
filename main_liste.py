from cake_crap_lib import *

# afficher la liste des recettes ( liste des recettes ) :
# 1 - titre de la recette - nombre d'ingrédients - url


def afficher_recette(recettes):
    for index in range(len(recettes)):
        recette = recettes[index]
        ingredients = recette["recette"]["ingredients"]
        url = recette["url"]
        print(index + 1, recette["titre"], "(nb_ingrédient :",  str(len(ingredients)) + ") - " + url)

liste_recettes_sauvegardees = charger_fichier_json(JSON_FILENAME)
if not liste_recettes_sauvegardees:
    print("Erreur : Aucune donnée")
    exit(0)

print("Nombre de recettes:", len(liste_recettes_sauvegardees))


afficher_recette(liste_recettes_sauvegardees)