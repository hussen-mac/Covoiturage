from database import add_user, add_itinerary, get_users, get_itineraries
from routing import get_route
from matching import find_matches, is_on_route

proposeur = {
    "name": "Alice",
    "start": (48.8449, 2.3749), 
    "end": (48.8918, 2.2430)
}

demandeur = {
    "name": "Bob",
    "destination": (48.8675, 2.3170) 
}

add_user({"name": proposeur["name"]})
add_user({"name": demandeur["name"]})

try:
    proposeur_route = get_route(proposeur["start"], proposeur["end"])
    add_itinerary({"name": proposeur["name"], "route": proposeur_route})
except Exception as e:
    print(f"Erreur lors du calcul de l'itinéraire : {e}")
    exit()

demandeurs_destinations = [demandeur["destination"]]


matches = find_matches(proposer_route=[proposeur["start"], proposeur["end"]], demandeurs=demandeurs_destinations, max_distance=5.0)

if matches:
    print("Correspondances trouvées :")
    for match in matches:
        print(f"Demandeur correspondant à {match}")
else:
    print("Aucune correspondance trouvée.")


for destination in demandeurs_destinations:
    if is_on_route(route_points=proposeur_route, destination=destination, max_distance=5.0):
        print(f"La destination {destination} est sur l'itinéraire d'Alice.")
    else:
        print(f"La destination {destination} n'est pas sur l'itinéraire d'Alice.")