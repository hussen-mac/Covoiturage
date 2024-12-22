import json

USER_FILE = "data/users.json"
ITINERARY_FILE = "data/itineraries.json"

def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def user_exists(name):
    """
    Vérifie si un utilisateur existe déjà dans les données.
    :param name: Nom de l'utilisateur.
    :return: True si l'utilisateur existe, sinon False.
    """
    users = load_data(USER_FILE)
    return any(user["name"] == name for user in users)



def add_user(user):
    """
    Ajoute un utilisateur s'il n'existe pas déjà.
    :param user: Dictionnaire contenant les informations de l'utilisateur.
    """
    if user_exists(user["name"]):
        pass
    else :
        users = load_data(USER_FILE)
        users.append(user)
        save_data(USER_FILE, users)

def add_itinerary(itinerary):
    """
    Ajoute un itinéraire s'il n'existe pas déjà.
    :param itinerary: Dictionnaire contenant les informations de l'itinéraire.
    """
    name = itinerary["name"]
    start = itinerary["route"][0]
    end = itinerary["route"][-1]
    
    itineraries = load_data(ITINERARY_FILE)
    itineraries.append(itinerary)
    save_data(ITINERARY_FILE, itineraries)

def get_users():
    """
    Récupère tous les utilisateurs.
    :return: Liste des utilisateurs.
    """
    return load_data(USER_FILE)

def get_itineraries():
    """
    Récupère tous les itinéraires.
    :return: Liste des itinéraires.
    """
    return load_data(ITINERARY_FILE)
