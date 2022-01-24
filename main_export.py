import pandas
from cake_crap_lib import *
from main import sauvegarder_fichier_json


def extraire_donnees(liste):
    titre = liste["titre"]
    ingredients = ", ".join(liste["recette"]["ingredients"])
    url = liste["url"]

    donnees = {
        "titre" : titre,
        "ingredients" : ingredients,
        "url" : url
    }
    return donnees

liste_recettes_sauvegardees = charger_fichier_json(JSON_FILENAME)
liste_recettes_sauvegardees = trier_recettes_par_liste_ingredients(liste_recettes_sauvegardees, MES_INGREDIENTS)
data = [extraire_donnees(items) for items in liste_recettes_sauvegardees]


data = pandas.DataFrame(data)
print(data)

data.to_excel("liste_finale.xlsx")
data.to_csv("data.csv")
"""
sauvegarder_fichier_json("data.json", data)
print(data)

data = pandas.read_json("data.json")
data.to_excel("data.xlsx")
"""


# IMPORTANT : !
# panda : dataframe.info()
# dataframe.lock[N° de colonne à afficher]
