import os
import csv
import time
import requests


# ==========================================
# Configuration
# ==========================================

MATCH_IDS = [
    "dr7vSRxA"
]

API_KEY = os.getenv("RAPIDAPI_KEY")

CSV_FILENAME = "data/raw/Hockey_results_Liiga_2025-2026.csv"

if not API_KEY:
    raise ValueError("La variable d'environnement RAPIDAPI_KEY n'est pas définie.")


# ==========================================
# Fonction récupération API
# ==========================================

def get_match_data(match_id, api_key):

    url = "https://flashscore4.p.rapidapi.com/api/flashscore/v2/matches/details"

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "flashscore4.p.rapidapi.com"
    }

    params = {
        "match_id": match_id
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            print(f"❌ Erreur {match_id}: {response.status_code}")
            print(response.text)
            return None

        return response.json()

    except requests.RequestException as e:
        print(f"❌ Exception {match_id}: {e}")
        return None


# ==========================================
# Extraction des données
# ==========================================

def extract_match_info(data):

    if not data:
        return None

    match = data.get("data", data)

    scores = match.get("scores", {})
    venue = match.get("venue", {})
    tournament = match.get("tournament", {})
    home_team = match.get("home_team", {})
    away_team = match.get("away_team", {})

    return [
        match.get("match_id"),
        tournament.get("name"),
        match.get("referee"),
        venue.get("name"),
        venue.get("city"),
        venue.get("attendance"),
        home_team.get("name"),
        away_team.get("name"),
        scores.get("home"),
        scores.get("away"),
        scores.get("home_total"),
        scores.get("away_total"),
        scores.get("home_1st_period"),
        scores.get("away_1st_period"),
        scores.get("home_2nd_period"),
        scores.get("away_2nd_period"),
        scores.get("home_3rd_period"),
        scores.get("away_3rd_period"),
        scores.get("home_overtime"),
        scores.get("away_overtime"),
        scores.get("home_penalties"),
        scores.get("away_penalties")
    ]


# ==========================================
# Création du CSV
# ==========================================

def main():

    os.makedirs(os.path.dirname(CSV_FILENAME), exist_ok=True)

    headers = [
        "match_id",
        "tournament_name",
        "referee",
        "venue_name",
        "venue_city",
        "venue_attendance",
        "home_team_name",
        "away_team_name",
        "home_scores",
        "away_scores",
        "home_total",
        "away_total",
        "home_1st_period",
        "away_1st_period",
        "home_2nd_period",
        "away_2nd_period",
        "home_3rd_period",
        "away_3rd_period",
        "home_overtime",
        "away_overtime",
        "home_penalties",
        "away_penalties"
    ]

    with open(
        CSV_FILENAME,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow(headers)

        for match_id in MATCH_IDS:

            print(f"🔎 Récupération : {match_id}")

            data = get_match_data(match_id, API_KEY)

            row = extract_match_info(data)

            if row:
                writer.writerow(row)
                print(f"✅ Match {match_id} enregistré")
            else:
                print(f"⚠️ Aucun résultat pour {match_id}")

            # Éviter les limites de l'API
            time.sleep(1)

    print(f"✅ Extraction terminée : {CSV_FILENAME}")


if __name__ == "__main__":
    main()

