import os
import json

JSON_FILENAME = "recette.json"
MES_INGREDIENTS = ['beurre', 'cacao', 'cacao en poudre', 'chocolat noir', 'chocolat noir à dessert', 'chocolat à pâtisserie noir',
                   'citron', 'compote', 'compote de pommes', 'confiture d"abricots', ' crème', 'crème fraîche', 'crème fraiche liquide',
                   "crème semi-épaisse entière", "farine", "eau", "eau-tiède", "farine de blé", "farine", "levure", "jus d'orange",
                   "huile végétale", 'œuf', 'œuf battu', 'œuf bien battu', 'œuf délayé avec quelques gouttes d’eau', 'œuf entier',
                   'œuf pour dorer', 'œuf+ 2 jaunes', 'œufs', 'œufs + 1 jaune pour la pâte', 'œufs + 1 œuf battu',
                   'œufs entiers', 'œufs séparés', 'sel', 'sel fin', 'sucre', 'sucre blanc', 'sucre brun', 'sucre en grains',
                   'sucre en poudre', 'sucre fin', 'sucre glace', 'sucre roux', 'sucre roux en poudre', 'pâte feuilletée', 'pâte feuilletée',
                   'lait', 'lait tiède', 'lait végétal']


def charger_fichier_json(filename):
    if os.path.exists(filename):
        f = open(filename, "r")
        json_data = f.read()
        f.close()
        return json.loads(json_data)
    return None

def filtrer_nom_ingredient(nom_ingredient):

    filtre_gauche = False
    filtre_droit = False

    index_de = nom_ingredient.find(" de ")
    if index_de != -1:
        nom_ingredient = nom_ingredient[index_de+4:]
        filtre_gauche = True

    if not filtre_gauche:
        index_d_apostrophe = nom_ingredient.find(" d'")
        if index_d_apostrophe == -1:
            index_d_apostrophe = nom_ingredient.find(" d’")
        if index_d_apostrophe != -1:
            nom_ingredient = nom_ingredient[index_d_apostrophe + 3:]
            filtre_gauche = True


    if not filtre_gauche:
        nom_split = nom_ingredient.split(" ")
        if nom_split[0].isdigit() and nom_split[1] == "ou" and nom_split[2].isdigit():
            nom_split = " ".join(nom_split[3:])
            nom_ingredient =  nom_split
            filtre_gauche = True


    if not filtre_gauche:
        nom_split = nom_ingredient.split(" ")
        if nom_split[0].isdigit() and nom_split[1] == "g":
            nom_split = " ".join(nom_split[2:])
            nom_ingredient =  nom_split
            filtre_gauche = True

    if not filtre_gauche:
        nom_split = nom_ingredient.split(" ")
        if nom_split[0].isdigit():
            nom_split = " ".join(nom_split[1:])
            nom_ingredient = nom_split
            filtre_gauche = True


    if not filtre_gauche:
        if nom_ingredient.startswith("du "):
            nom_ingredient =  nom_ingredient[3:]
            filtre_gauche = True

    if not filtre_gauche:
        if nom_ingredient.startswith("des "):
            nom_ingredient = nom_ingredient[4:]
            filtre_gauche = True

    #filtre à droite :
    index_parenthese = nom_ingredient.find("(")
    if index_parenthese != -1:
        return nom_ingredient[:index_parenthese]

    index_tiret = nom_ingredient.find(" - ")
    if index_tiret != -1:
        return nom_ingredient[:index_tiret]


    index_crochet = nom_ingredient.find(" [")
    if index_crochet != -1:
        return nom_ingredient[:index_crochet]



    return nom_ingredient


def trier_recettes_par_liste_ingredients(liste_recettes, liste_ingredients):

    for recette in liste_recettes:
        ingredients = recette["recette"]["ingredients"]
        noms_ingredients = [filtrer_nom_ingredient(index).lower().strip() for index in ingredients]
        recette["noms_ingredients"] = noms_ingredients
        recette["ingredients_correspondants"] = [items for items in recette["noms_ingredients"]if items in MES_INGREDIENTS]
        recette["ingredients_manquants"] = [items for items in recette["noms_ingredients"] if items not in MES_INGREDIENTS]
        recette["score_recette"] = len(recette["ingredients_correspondants"]) - 2 * len(recette["ingredients_manquants"])
        if len(recette["ingredients_manquants"]) == 0:
            recette["score_recette"] += 100
        if len(recette["ingredients_correspondants"]) == 0:
            recette["score_recette"] -= 100

    liste_recettes.sort(key=lambda x: x["score_recette"], reverse = True )

    return liste_recettes