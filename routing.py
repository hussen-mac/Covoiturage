import requests
import polyline

OSRM_API = "http://router.project-osrm.org/route/v1/driving"

def get_route(start, end):
    """
    Utilise l'API OSRM pour calculer un itinéraire.
    :param start: Tuple (latitude, longitude) du point de départ.
    :param end: Tuple (latitude, longitude) du point d'arrivée.
    :return: Liste des points de l'itinéraire.
    """
    coords = f"{start[1]},{start[0]};{end[1]},{end[0]}"
    response = requests.get(f"{OSRM_API}/{coords}?overview=full")
    if response.status_code == 200:
        route = response.json()["routes"][0]["geometry"]
        encoded_polyline = route
        decoded_points = polyline.decode(encoded_polyline)
        return decoded_points
    else:
        raise Exception("Erreur lors de la récupération de l'itinéraire")
