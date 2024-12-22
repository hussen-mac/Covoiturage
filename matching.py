from geopy.distance import geodesic
import numpy as np

from geopy.distance import geodesic
import numpy as np

def find_matches(proposer_route, demandeurs, max_distance=1.0):
    """
    Trouve les correspondances en fonction de l'itinéraire.
    :param proposer_route: Liste des points de l'itinéraire du proposeur.
    :param demandeurs: Liste des destinations des demandeurs [(latitude, longitude), ...].
    :param max_distance: Distance maximale (en km) pour considérer un point comme proche.
    :return: Liste des demandeurs correspondant.
    """
    matched_demandeurs = []
    for demandeur in demandeurs:
        for route_point in proposer_route:
            distance = geodesic(route_point, demandeur).km
            if distance <= max_distance:
                matched_demandeurs.append(demandeur)
                break  
    return matched_demandeurs[:3] 

def is_on_route(route_points, destination, max_distance=1.0):
    """
    Vérifie si la destination se trouve sur l'itinéraire.
    :param route_points: Liste des points (latitude, longitude) de l'itinéraire.
    :param destination: Coordonnées (latitude, longitude) de la destination du demandeur.
    :param max_distance: Distance maximale (en km) pour considérer la destination sur le chemin.
    :return: True si la destination est sur le chemin, sinon False.
    """
    for point in route_points:
        if geodesic(point, destination).km <= max_distance:
            return True
    return False
