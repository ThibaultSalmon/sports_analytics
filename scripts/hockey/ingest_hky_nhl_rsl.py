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

CSV_FILE = "data/hockey/NHL_RSL.csv"


# ============================================================
# COLONNES DU CSV
# ============================================================

COLUMNS = [
    "League",
    "Season",
    "Date",
    "Time",
    "Overtime/TAB",
    "Id game (Flashscore)",
    "Game",
    "Home team",
    "Away team",
    "Result game",
    "Total goals",
    "Total goals before overtime",
    "Result home",
    "Result away",
    "Result 1st TT",
    "Goals 1st TT",
    "More than 1,5 goals 1st TT",
    "1st TT - home",
    "1st TT - away",
    "Result 2nd TT",
    "Goals 2nd TT",
    "More than 1,5 goals 2nd TT",
    "2nd TT - home",
    "2nd TT - away",
    "Result 3rd TT",
    "Goals 3rd TT",
    "More than 1,5 goals 3rd TT",
    "3rd TT - home",
    "3rd TT - away",
    "TT with more goals",
    "4th TT - home",
    "4th TT - away",
    "5th TT - home",
    "5th TT - away",
    "+4,5 goals",
    "+5,5 goals",
    "+6,5 goals",
    "+7,5 goals"
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
            CREATE TEMP TABLE tmp_hky_nhl_rsl AS
            SELECT
                "League",
                "Season",
                "Date",
                "Time",
                "Overtime/TAB",
                "Id game (Flashscore)",
                "Game",
                "Home team",
                "Away team",
                "Result game",
                "Total goals",
                "Total goals before overtime",
                "Result home",
                "Result away",
                "Result 1st TT",
                "Goals 1st TT",
                "More than 1,5 goals 1st TT",
                "1st TT - home",
                "1st TT - away",
                "Result 2nd TT",
                "Goals 2nd TT",
                "More than 1,5 goals 2nd TT",
                "2nd TT - home",
                "2nd TT - away",
                "Result 3rd TT",
                "Goals 3rd TT",
                "More than 1,5 goals 3rd TT",
                "3rd TT - home",
                "3rd TT - away",
                "TT with more goals",
                "4th TT - home",
                "4th TT - away",
                "5th TT - home",
                "5th TT - away",
                "+4,5 goals",
                "+5,5 goals",
                "+6,5 goals",
                "+7,5 goals"
            FROM raw."HKY_NHL_RSL"
            WITH NO DATA;
        """)

        # ----------------------------------------------------
        # Import CSV dans la table temporaire
        # ----------------------------------------------------

        with open(CSV_FILE, "r", encoding="utf-8") as f:

            cursor.copy_expert(
                """
                COPY tmp_hky_nhl_rsl (
                    "League",
                    "Season",
                    "Date",
                    "Time",
                    "Overtime/TAB",
                    "Id game (Flashscore)",
                    "Game",
                    "Home team",
                    "Away team",
                    "Result game",
                    "Total goals",
                    "Total goals before overtime",
                    "Result home",
                    "Result away",
                    "Result 1st TT",
                    "Goals 1st TT",
                    "More than 1,5 goals 1st TT",
                    "1st TT - home",
                    "1st TT - away",
                    "Result 2nd TT",
                    "Goals 2nd TT",
                    "More than 1,5 goals 2nd TT",
                    "2nd TT - home",
                    "2nd TT - away",
                    "Result 3rd TT",
                    "Goals 3rd TT",
                    "More than 1,5 goals 3rd TT",
                    "3rd TT - home",
                    "3rd TT - away",
                    "TT with more goals",
                    "4th TT - home",
                    "4th TT - away",
                    "5th TT - home",
                    "5th TT - away",
                    "+4,5 goals",
                    "+5,5 goals",
                    "+6,5 goals",
                    "+7,5 goals"
                )
                FROM STDIN
                WITH (
                    FORMAT CSV,
                    HEADER TRUE,
                    DELIMITER ',',
                    NULL ''
                )
                """,
                f
            )

        # ----------------------------------------------------
        # Insertion dans la table finale
        # ----------------------------------------------------

        cursor.execute("""
            INSERT INTO raw."test_HKY_NHL_RSL" (
                "League",
                "Season",
                "Date",
                "Time",
                "Overtime/TAB",
                "Id game (Flashscore)",
                "Game",
                "Home team",
                "Away team",
                "Result game",
                "Total goals",
                "Total goals before overtime",
                "Result home",
                "Result away",
                "Result 1st TT",
                "Goals 1st TT",
                "More than 1,5 goals 1st TT",
                "1st TT - home",
                "1st TT - away",
                "Result 2nd TT",
                "Goals 2nd TT",
                "More than 1,5 goals 2nd TT",
                "2nd TT - home",
                "2nd TT - away",
                "Result 3rd TT",
                "Goals 3rd TT",
                "More than 1,5 goals 3rd TT",
                "3rd TT - home",
                "3rd TT - away",
                "TT with more goals",
                "4th TT - home",
                "4th TT - away",
                "5th TT - home",
                "5th TT - away",
                "+4,5 goals",
                "+5,5 goals",
                "+6,5 goals",
                "+7,5 goals"
            )
            SELECT
                "League",
                "Season",
                "Date",
                "Time",
                "Overtime/TAB",
                "Id game (Flashscore)",
                "Game",
                "Home team",
                "Away team",
                "Result game",
                "Total goals",
                "Total goals before overtime",
                "Result home",
                "Result away",
                "Result 1st TT",
                "Goals 1st TT",
                "More than 1,5 goals 1st TT",
                "1st TT - home",
                "1st TT - away",
                "Result 2nd TT",
                "Goals 2nd TT",
                "More than 1,5 goals 2nd TT",
                "2nd TT - home",
                "2nd TT - away",
                "Result 3rd TT",
                "Goals 3rd TT",
                "More than 1,5 goals 3rd TT",
                "3rd TT - home",
                "3rd TT - away",
                "TT with more goals",
                "4th TT - home",
                "4th TT - away",
                "5th TT - home",
                "5th TT - away",
                "+4,5 goals",
                "+5,5 goals",
                "+6,5 goals",
                "+7,5 goals"
            FROM tmp_hky_nhl_rsl
            ON CONFLICT ("Id game (Flashscore)") DO NOTHING;;
        """)

        print(
            f"{cursor.rowcount} lignes insérées dans "
            f'raw."test_HKY_NHL_RSL"'
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