import random
import pandas as pd 
import math
from datetime import datetime, timezone
import uuid 

operateurs = ["Orange", "SFR", "Bouygues", "Free"]

technologie = ["4G", "5G", "3G"]

bandes = {
    "3G": ["900",  "2100"],
    "4G": ["800",  "1800", "2600"],
    "5G": ["2100", "3500", "700"]
}

performance_map = {
    "3G": {"lat_min": 70, "lat_max": 150, "debit_min": 1, "debit_max": 42},
    "4G": {"lat_min": 25, "lat_max": 70,  "debit_min": 10, "debit_max": 150},
    "5G": {"lat_min": 8,  "lat_max": 25,  "debit_min": 100, "debit_max": 1000}
}

regions = [
    "Île-de-France", "Auvergne-Rhône-Alpes", "Nouvelle-Aquitaine",
    "Occitanie", "Hauts-de-France", "Provence-Alpes-Côte d'Azur",
    "Bourgogne-Franche-Comté", "Normandie", "Bretagne", "Centre-Val de Loire"
]

azimuths_map = {
    1: [0],           # 1 secteur 
    2: [0, 180],      # 2 secteurs 
    3: [0, 120, 240]  # 3 secteurs 
}

def generate_network_data(nombre_tour):
    data = []
    
    # 1. BOUCLE DES SITES
    for i in range(nombre_tour):
        id_site = str(uuid.uuid4().int)[:8]
        region = random.choice(regions)
        operateur = random.choice(operateurs).upper()[:3]
        
        # Position GPS du pylône (identique pour tous les secteurs et technos de ce site)
        latitude = round(random.uniform(42.0, 51.0), 5)
        longitude = round(random.uniform(-5.0, 8.0), 5)
        
        nb_secteurs = random.choices([1, 2, 3], weights=[10, 20, 100])[0]
        liste_azimuths = azimuths_map[nb_secteurs]
        
        # 2. BOUCLE DES SECTEURS (Azimuts)
        for j, azimuth in enumerate(liste_azimuths):
            sector_id = j + 1
            
            # Caractéristiques physiques de ce secteur (identiques pour la 3G/4G/5G de ce secteur)
            hauteur = random.randint(10, 100)
            dist_centre = round(random.uniform(1.0, 2.5), 2)
            offset_x = round(dist_centre * math.sin(math.radians(azimuth)), 2)
            offset_y = round(dist_centre * math.cos(math.radians(azimuth)), 2)
            
            # 3. BOUCLE DES TECHNOLOGIES (On installe 3G, 4G et 5G sur le même secteur)
            for type_antenne in technologie:
                
                # Identifiants uniques pour ce flux précis
                device_id = f"{operateur}-ANT{type_antenne}-{region[:3].lower()}-{id_site}"
                transmitter_name = f"{device_id}_L-{sector_id}"
                
                bande = random.choice(bandes[type_antenne])
                temps_actuel = datetime.now(timezone.utc).isoformat()
                
                # Récupération du profil de performance (Latence et Débit)
                profil = performance_map[type_antenne]
                
                seuil = random.random()
                if seuil < 0.05:  # 5% du temps : ERREUR CRITIQUE
                    latency = random.randint(profil["lat_max"] * 2, profil["lat_max"] * 5)
                    debit_actuel = round(random.uniform(0.0, profil["debit_min"] / 2), 2)
                    packet_loss = round(random.uniform(5.0, 15.0), 2)
                    status = "ERROR"
                elif seuil < 0.15:  # 10% du temps : DÉGRADÉ
                    latency = random.randint(profil["lat_max"], profil["lat_max"] * 2)
                    debit_actuel = round(random.uniform(profil["debit_min"] / 2, profil["debit_min"]), 2)
                    packet_loss = round(random.uniform(2.0, 5.0), 2)
                    status = "WARNING"
                else:  # 85% du temps : NORMAL
                    latency = random.randint(profil["lat_min"], profil["lat_max"])
                    debit_actuel = round(random.uniform(profil["debit_min"], profil["debit_max"]), 2)
                    packet_loss = round(random.uniform(0.0, 1.5), 2)
                    status = "OK"

                # Ajout de la ligne dans le tableau
                data.append({
                    "Timestamp": temps_actuel,
                    "Device_ID": device_id,
                    "Transmitter": transmitter_name,
                    "Region": region,
                    "Operateur": operateur,
                    "Type_Antenne": type_antenne,
                    "Band_MHz": bande,
                    "Sector_ID": sector_id,
                    "Azimuth_deg": azimuth,
                    "Hauteur_m": hauteur,
                    "Latitude": latitude,
                    "Longitude": longitude,
                    "Offset_X_m": offset_x,
                    "Offset_Y_m": offset_y,
                    "Latency_ms": latency,
                    "Throughput_Mbps": debit_actuel,
                    "Packet_Loss_pct": packet_loss,
                    "Status": status
                })

    return pd.DataFrame(data)

