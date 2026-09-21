import os
import csv
import io
import time
import requests


# ==========================================
# Configuration
# ==========================================

MATCH_IDS = [
    "dr7vSRxA"
]

API_KEY = os.getenv("RAPIDAPI_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

# Chemin uniquement dans Supabase Storage
SUPABASE_FILE_PATH = (
    "hockey/Hockey_results_Liiga_2025-2026_test_v2.csv"
)


# ==========================================
# Vérification configuration
# ==========================================

if not API_KEY:
    raise ValueError(
        "La variable d'environnement RAPIDAPI_KEY "
        "n'est pas définie."
    )

if not SUPABASE_URL:
    raise ValueError(
        "La variable d'environnement SUPABASE_URL "
        "n'est pas définie."
    )

if not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError(
        "La variable d'environnement "
        "SUPABASE_SERVICE_ROLE_KEY n'est pas définie."
    )

if not SUPABASE_BUCKET:
    raise ValueError(
        "La variable d'environnement SUPABASE_BUCKET "
        "n'est pas définie."
    )


# ==========================================
# Fonction récupération API
# ==========================================

def get_match_data(match_id, api_key):

    url = (
        "https://flashscore4.p.rapidapi.com/"
        "api/flashscore/v2/matches/details"
    )

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

            print(
                f"❌ Erreur API pour le match {match_id}: "
                f"{response.status_code}"
            )

            print(response.text)

            # On lève une exception pour arrêter
            # complètement le processus
            raise Exception(
                f"Erreur API pour {match_id}: "
                f"HTTP {response.status_code}"
            )

        return response.json()

    except requests.RequestException as e:

        print(
            f"❌ Exception lors de la requête "
            f"pour {match_id}: {e}"
        )

        # On arrête complètement le processus
        raise Exception(
            f"Impossible de récupérer les données "
            f"du match {match_id}"
        ) from e


# ==========================================
# Extraction des données
# ==========================================

def extract_match_info(data):

    if not data:
        raise ValueError(
            "Les données du match sont vides."
        )

    match = data.get("data", data)

    if not match:
        raise ValueError(
            "Aucune donnée de match trouvée."
        )

    scores = match.get("scores", {})
    venue = match.get("venue", {})
    tournament = match.get("tournament", {})
    home_team = match.get("home_team", {})
    away_team = match.get("away_team", {})

    match_id = match.get("match_id")

    if not match_id:
        raise ValueError(
            "Le match_id est absent de la réponse API."
        )

    return [
        match_id,
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
# Création du CSV en mémoire
# ==========================================

def create_csv():

    output = io.StringIO()

    writer = csv.writer(output)

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

    writer.writerow(headers)

    for match_id in MATCH_IDS:

        print(
            f"🔎 Récupération : {match_id}"
        )

        # Si une erreur survient ici,
        # create_csv() s'arrête immédiatement
        data = get_match_data(
            match_id,
            API_KEY
        )

        row = extract_match_info(data)

        writer.writerow(row)

        print(
            f"✅ Match {match_id} enregistré"
        )

        time.sleep(1)

    print(
        f"✅ {len(MATCH_IDS)} match(s) récupéré(s) "
        "avec succès."
    )

    return output.getvalue()


# ==========================================
# Upload vers Supabase
# ==========================================

def upload_to_supabase(csv_content):

    url = (
        f"{SUPABASE_URL}/storage/v1/object/"
        f"{SUPABASE_BUCKET}/{SUPABASE_FILE_PATH}"
    )

    headers = {
        "Authorization": (
            f"Bearer {SUPABASE_SERVICE_ROLE_KEY}"
        ),
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Content-Type": "text/csv",
        "x-upsert": "true"
    }

    response = requests.post(
        url,
        headers=headers,
        data=csv_content.encode("utf-8")
    )

    if response.status_code not in [200, 201]:

        print(
            "❌ Erreur lors de l'upload Supabase"
        )

        print(
            response.status_code
        )

        print(
            response.text
        )

        raise Exception(
            "Upload Supabase échoué."
        )

    print(
        "☁️ Fichier envoyé dans Supabase : "
        f"{SUPABASE_BUCKET}/"
        f"{SUPABASE_FILE_PATH}"
    )


# ==========================================
# Programme principal
# ==========================================

def main():

    try:

        # --------------------------------------
        # 1. Extraction
        # --------------------------------------
        # Si une seule requête échoue,
        # cette fonction lève une exception.
        csv_content = create_csv()

        # --------------------------------------
        # 2. Upload
        # --------------------------------------
        # On n'arrive ici QUE si toutes les
        # requêtes API ont réussi.
        upload_to_supabase(csv_content)

        print(
            "✅ Extraction et upload terminés."
        )

    except Exception as e:

        print(
            "\n❌ PROCESSUS ARRÊTÉ"
        )

        print(
            f"Erreur : {e}"
        )

        print(
            "⚠️ Aucun fichier n'a été envoyé "
            "dans Supabase."
        )

        raise


if __name__ == "__main__":
    main()