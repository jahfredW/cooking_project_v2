import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.cuisine-libre.org/"

url = "https://www.cuisine-libre.org/imbolc-moon-cookies"
#url = "https://www.cuisine-libre.org/american-apple-pie"
#url = "https://www.cuisine-libre.org/halwa-de-carotte-aux-cajou-et-pistaches-gajjar-halwa"
url2 = "https://www.cuisine-libre.org/boulangerie-et-patisserie"

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
    return chaine.replace("\xa0", " ").replace("\n", "").strip()



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
    
    tab_license = ["Domaine public", "CC0"]
    
    # vérification de la license : 
    license = soup.find("footer", id="license").text
    license_valide = "cc0" in license.lower() or "dommaine public" in license.lower()  
    if not license_valide:
        print("Vous n'avez pas les droits")
        return None 

    titre = nettoyer_chaine(str(soup.find("h1").contents[0]))
    
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
    
    div_ingredients = soup.find("div", id="ingredients")
    ingredients = div_ingredients.find_all("li")
    liste_ingredients = [nettoyer_chaine(i.text) for i in ingredients if not i.find("i")]   
    
    div_preparation = soup.find("div", id="preparation")
    preparation = div_preparation.find_all("p")
    if len(preparation) == 0:
        preparation = div_preparation.find_all("li")
    etapes = [nettoyer_chaine(p.text) for p in preparation if preparation] # complétion de liste
    
     
        
    print(license)
    infos = {"duree_preparation": duree_preparation, "duree_cuisson": duree_cuisson, "duree_repos": duree_repos, "methode_cuisson": methode_cuisson}
    
    
    
    recette = {"titre" : titre, 
               "infos" : infos,
               "ingredients" : liste_ingredients,
               "etapes" : etapes}
    
    
    print(recette)
    print(infos)
    print(liste_ingredients)
    
    return recette
    
   
def extraire_liste_recettes(url):
    #{ "titre": "", "url": "", "url_image": ""}
    liste_liens = []
    response = requests.get(url)
    if response.status_code != 200:
        return None
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        div_recettes = soup.find("div", id="recettes")
        ul_recettes = div_recettes.find("ul", recursive=False)
        li_recettes = ul_recettes.find_all("li")
    # difference entre la recherche récursive == recherche du premier niveau    
        liste_resultat = []
        for item in li_recettes:
            a = item.find("a")
            strong = a.find("strong")
            url =  BASE_URL + a['href']
            img = item.find("img")
            image = BASE_URL + img["src"]
            titre = nettoyer_chaine(strong.text)
            liste_resultat.append({ "titre": titre, "url": url, "url_image": image})
        
        
    return liste_resultat
print(extraire_liste_recettes(url2))
    
    
   