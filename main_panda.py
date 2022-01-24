import pandas

"""
data = {
    "noms" : ["Jean", "Paul", "Emilie"],
    "ages" : [30, 20, 25]
}

noms_et_ages = pandas.DataFrame(data)
noms_et_ages.to_csv("noms_et_ages.csv")
noms_et_ages.to_excel("noms_et_ages.xlsx")

fichier = open("recette.json", "r")
donnees = fichier.read()
fichier.close()

print(donnees)
"""

recettes = pandas.read_json("recette.json")
print(recettes)
recettes.to_excel("recettes.xlsx")