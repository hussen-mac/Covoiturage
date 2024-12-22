from flask import Flask, jsonify, request, render_template
import requests
import polyline
from geopy.distance import geodesic
import os
from database import add_user, user_exists, add_itinerary, get_itineraries

app = Flask(__name__)

OSRM_API = "http://router.project-osrm.org/route/v1/driving"
GEOCODE_API = "https://api.opencagedata.com/geocode/v1/json"
GEOCODE_API_KEY = "684c6e2713074948933599d7b84c5999"


@app.route("/")
def home():
    return render_template("index.html")

import json

def get_user_profile(name):
    """Récupère le profil d'un utilisateur depuis un fichier JSON."""
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
        for user in users:
            if user["name"] == name:
                return user["profile"]
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None  
    return None 



@app.route("/create_user", methods=["POST"])
def create_user():
    """Créer un utilisateur avec un profil (proposeur ou demandeur)."""
    data = request.json
    name = data.get("name")
    profile = data.get("profile")  # 'proposeur' ou 'demandeur'

    if not profile or profile not in ["proposeur", "demandeur"]:
        return jsonify({"message": "Invalid profile. Must be 'proposeur' or 'demandeur'."}), 400

    if user_exists(name):
        return jsonify({"message": "User already exists"}), 400

    add_user({"name": name, "profile": profile})
    return jsonify({"message": f"User '{name}' with profile '{profile}' created successfully"}), 201


@app.route("/get_coordinates", methods=["POST"])
def get_coordinates():
    """Convertir une localisation textuelle (ville, quartier, pays) en coordonnées."""
    data = request.json
    location = data.get("location")
    response = requests.get(GEOCODE_API, params={"q": location, "key": GEOCODE_API_KEY})

    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            coordinates = results[0]["geometry"]
            return jsonify({"latitude": coordinates["lat"], "longitude": coordinates["lng"]}), 200

    return jsonify({"message": "Location not found"}), 404

def save_itinerary(itinerary):
    """Enregistre un itinéraire dans le fichier itineraires.json."""
    try:
        # Vérifier si le fichier existe déjà
        if os.path.exists("itineraires.json"):
            with open("itineraires.json", "r") as file:
                itineraries = json.load(file)
        else:
            itineraries = []

        # Ajouter le nouvel itinéraire
        itineraries.append(itinerary)

        # Écrire dans le fichier
        with open("itineraires.json", "w") as file:
            json.dump(itineraries, file, indent=4)
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de l'itinéraire : {e}")


@app.route('/add_itinerary', methods=['POST'])
def add_itinerary():
    """Ajoute un itinéraire et l'enregistre dans itineraires.json."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    name = data.get('name')
    profile =data.get('profile')
    start = data.get('start')
    end = data.get('end')

    if not name or not start or not end:
        return jsonify({'error': 'Missing fields in request'}), 400

    # Construire l'itinéraire
    itinerary = {'name': name, 'profile' : profile, 'start': start, 'end': end}

    # Sauvegarder l'itinéraire
    save_itinerary(itinerary)

    return jsonify({
        'message': 'Itinerary added successfully',
        'itinerary': itinerary
    }), 201


@app.route("/find_matches", methods=["GET"])
def find_matches():
    """Trouver les correspondances entre itinéraires (proposeur et demandeur)."""
    itineraries = get_itineraries()
    matches = []

    # Identifier les demandeurs et proposeurs
    proposeurs = [i for i in itineraries if i["profile"] == "proposeur"]
    demandeurs = [i for i in itineraries if i["profile"] == "demandeur"]

    for proposeur in proposeurs:
        for demandeur in demandeurs:
            if routes_overlap(proposeur["route"], demandeur["route"]):
                matches.append({"proposeur": proposeur["name"], "demandeur": demandeur["name"]})

    return jsonify(matches), 200


# Fonctions utilitaires
def get_coordinates_from_text(location):
    """Obtenir les coordonnées (latitude/longitude) à partir d'une localisation textuelle."""
    response = requests.get(GEOCODE_API, params={"q": location, "key": GEOCODE_API_KEY})
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            return results[0]["geometry"]["lat"], results[0]["geometry"]["lng"]
    return None


def get_route_between_points(start, end):
    """Obtenir un itinéraire entre deux points via l'API OSRM."""
    coords = f"{start[1]},{start[0]};{end[1]},{end[0]}"
    response = requests.get(f"{OSRM_API}/{coords}?overview=full")
    if response.status_code == 200:
        route = response.json()["routes"][0]["geometry"]
        return polyline.decode(route)
    return None


def routes_overlap(route1, route2, max_distance=1.0):
    """Vérifier si deux itinéraires se chevauchent."""
    for point1 in route1:
        for point2 in route2:
            if geodesic(point1, point2).km <= max_distance:
                return True
    return False


if __name__ == "__main__":
    app.run(debug=True)
