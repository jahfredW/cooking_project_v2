
import requests
from bs4 import BeautifulSoup


url = "https://www.cuisine-libre.org/imbolc-moon-cookies"


# décoder les caracteres unicodes 
# paramètre : chaine: str 
# utilisation des fonction encode() et decode()
# retourne une chaine str décodée
def decoder_caracteres_unicodes(chaine: str=""):
    return chaine.encode().decode("unicode-escape")



# nettoie la chaine des caractère
# paramètre : chaine :str 
# remplace et strip 
# retourne la chaine str nettoyé 
def nettoyer_chaine(chaine: str=""):
    return chaine.replace("\xa0", " ").strip()



# extrait la durée du bloc de donnees
# paramètres : objet soup recipe_infos_p, nom de la classe en str
# trouve la balise html, et vérifie si elle existe avant de la renvoyer
# retourne la duree: str après l'avoir nettoyée via f nettoyer_chaine
def extraire_duree_recette(recipe_infos_p: object, class_name: str):
    span = recipe_infos_p.find("span", class_=class_name)
    duree =  span.find("time").text if span else ""
    return nettoyer_chaine(duree).replace('?', '')


# extraction des infos de la recette
# paramètre : l'url de la page 
# requete http et récupération de la response via requests
# creation d'un objet soup ( para response.text, html.parser)
# extraction du titre et de toutes les balises necessaires
# renvoie à termes un dico 

def extraire_infos_recette(url): 
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    titre = soup.find("h1")
    print(titre.text)
    
    recipe_infos_p = soup.find("p", id="recipe-infos")
    # methode 1 : lambda : si la class existe et si elle commence par " article-duree_preparation"
    # duree_preparation = recipe_infos_p.find("time", class_=lambda x: x and x.startswith("article-duree_preparation")).text
    
    
    #methode_cuisson = recipe_infos_p.find("span")
    duree_cuisson = extraire_duree_recette(recipe_infos_p, "cookTime" )
    
    duree_repos = extraire_duree_recette(recipe_infos_p, "duree_repos")
    
    #methode d2 : on va dans le span de classe " duree preparation" et on va cherche le time
    duree_preparation = extraire_duree_recette(recipe_infos_p, "prepTime")
    
    methode_cuisson_a = recipe_infos_p.find("a")
    methode_cuisson = methode_cuisson_a.text if methode_cuisson_a else ""
     
    infos = {"duree_preparation": duree_preparation, "duree_cuisson": duree_cuisson, "duree_repos": duree_repos, "methode_cuisson": methode_cuisson}
    
    
    
    recette = {"titre" : titre, 
               "infos" : infos,
               "ingredients" : None,
               "etapes" : None}
    
    
    
    print(" titre:", titre.text)
    print(infos)
    
    return recette
    
   
extraire_infos_recette(url)  