import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

CSV_FILE = "data/hockey/NHL_DTL.csv"


# ============================================================
# COLONNES DU CSV
# ============================================================

COLUMNS = [
    "Match ID",
    "Venue",
    "Attendance",
    "Stage Name", 
    "Incident Team",
    "Participant",
    "Incident",
    "Subname",
    "Time"
]


# ============================================================
# CONNEXION
# ============================================================

conn = psycopg2.connect(**DB_CONFIG)

try:

    with conn.cursor() as cursor:

        # ----------------------------------------------------
        # Création d'une table temporaire
        # ----------------------------------------------------

        cursor.execute("""
            CREATE TEMP TABLE tmp_hky_nhl_dtl AS
            SELECT
                "Match ID",
                "Venue",
                "Attendance",
                "Stage Name", 
                "Incident Team",
                "Participant",
                "Incident",
                "Subname",
                "Time"
            FROM raw."HKY_NHL_DTL"
            WITH NO DATA;
        """)

        # ----------------------------------------------------
        # Import CSV dans la table temporaire
        # ----------------------------------------------------

        with open(CSV_FILE, "r", encoding="utf-8") as f:

            cursor.copy_expert(
                """
                COPY tmp_hky_nhl_dtl (
                    "Match ID",
                    "Venue",
                    "Attendance",
                    "Stage Name", 
                    "Incident Team",
                    "Participant",
                    "Incident",
                    "Subname",
                    "Time"
                )
                FROM STDIN
                WITH (
                    FORMAT CSV,
                    HEADER TRUE,
                    DELIMITER ',',
                    NULL 'N/A'
                )
                """,
                f
            )

        # ----------------------------------------------------
        # Insertion dans la table finale
        # ----------------------------------------------------

        cursor.execute("""
            INSERT INTO raw."HKY_NHL_DTL" (
                "Match ID",
                "Venue",
                "Attendance",
                "Stage Name", 
                "Incident Team",
                "Participant",
                "Incident",
                "Subname",
                "Time"
            )
            SELECT
                "Match ID",
                "Venue",
                "Attendance",
                "Stage Name", 
                "Incident Team",
                "Participant",
                "Incident",
                "Subname",
                "Time"
            FROM tmp_hky_nhl_dtl
            ON CONFLICT ("Match ID", "Stage Name", "Incident Team", "Participant", "Incident") DO NOTHING;;
        """)

        print(
            f"{cursor.rowcount} lignes insérées dans "
            f'raw."HKY_NHL_DTL"'
        )

    # --------------------------------------------------------
    # COMMIT
    # --------------------------------------------------------

    conn.commit()

except Exception as e:

    conn.rollback()
    print("ERREUR :", e)
    raise

finally:

    conn.close()

print("Ingestion terminée.")