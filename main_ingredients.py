from cake_crap_lib import *


liste_recettes_sauvegardées = charger_fichier_json(JSON_FILENAME)


liste_recettes_sauvegardées = trier_recettes_par_liste_ingredients(liste_recettes_sauvegardées, MES_INGREDIENTS)
for index in range(len(liste_recettes_sauvegardées)):
    recette = liste_recettes_sauvegardées[index]
    print(index + 1, recette["titre"], "-", recette["url"])
    print(" Ingrédients que l'on a : ", recette["ingredients_correspondants"])
    print(" Ingrédients manquants : ", recette["ingredients_manquants"])
    print(" Score : ", recette["score_recette"])


