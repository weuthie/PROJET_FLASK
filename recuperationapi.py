import requests
def donneapi(chaine):
        list_info = ["posts","comments","photos","todos","albums","users"]
        if chaine in list_info:
            res = requests.get(f"https://jsonplaceholder.typicode.com/{chaine}")
            chaine = res.json()
            return chaine
        else:
            return "le nom n'est pas valide"

