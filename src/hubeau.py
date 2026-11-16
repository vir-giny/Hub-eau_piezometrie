"""
Fonctions utilitaires pour interroger l'API Hub'Eau (piézométrie).

Utilisé par les notebooks 01_collectAPI_stations et 01_collectAPI_chroniques.
"""

import math
import time

import requests


def bbox_autour(lat, lon, demi_cote_km):
    """
    Calcule une bbox carrée centrée sur un point, au format Hub'Eau.

    Paramètres
    ----------
    lat, lon : float      Coordonnées du centre (WGS84)
    demi_cote_km : float  Demi-côté du carré en km

    Renvoie
    -------
    str  "min_lon,min_lat,max_lon,max_lat" (4 décimales)
    """
    d_lat = demi_cote_km / 111.32
    d_lon = demi_cote_km / (111.32 * math.cos(math.radians(lat)))
    return f"{lon - d_lon:.4f},{lat - d_lat:.4f},{lon + d_lon:.4f},{lat + d_lat:.4f}"


def appeler_api(url, params=None, max_pages=50, timeout_s=30, pause_s=0.2):
    """
    Interroge un endpoint Hub'Eau et récupère toutes les pages de résultats.

    Paramètres
    ----------
    url : str          URL de l'endpoint
    params : dict      Paramètres de la requête (bbox, size, format...)
    max_pages : int    Sécurité : nombre maximum de pages à récupérer
    timeout_s : float  Délai max d'attente d'une réponse (secondes)
    pause_s : float    Pause entre deux pages (secondes)

    Renvoie
    -------
    list[dict]  L'ensemble des résultats (contenu des champs "data")
    """
    resultats = []
    num_page = 1

    while url:
        reponse = requests.get(url, params=params, timeout=timeout_s)

        # 200 = tout est là / 206 = résultat partiel, d'autres pages suivent
        if reponse.status_code not in (200, 206):
            raise RuntimeError(f"Erreur API {reponse.status_code} : {reponse.text[:300]}")

        contenu = reponse.json()
        resultats.extend(contenu["data"])
        print(f"Page {num_page} : {len(contenu['data'])} résultats "
              f"({len(resultats)}/{contenu['count']})")

        url = contenu.get("next")    # None sur la dernière page => fin de la boucle
        params = None                # l'URL "next" contient déjà tous les paramètres
        num_page += 1

        if num_page > max_pages:
            print(f"⚠️ Arrêt après {max_pages} pages : résultats incomplets")
            break
        if url:
            time.sleep(pause_s)

    return resultats
