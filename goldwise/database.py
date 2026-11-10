from datetime import date, timedelta
import psycopg

from goldwise.config import database_config

METALS = ("24K", "22K", "silver")

def get_connection():
    return psycopg.connect(**database_config())

def initialize_tables():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS public.market_rates (
                id SERIAL PRIMARY KEY,
                rate_date DATE NOT NULL,
                metal VARCHAR(10) NOT NULL,
                rate_per_10g NUMERIC(12, 2) NOT NULL,
                city VARCHAR(50) DEFAULT 'Kamareddy',
                source VARCHAR(50) NOT NULL,
                fetched_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (rate_date, metal, city, source)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS public.report_snapshots (
                metal VARCHAR(10) PRIMARY KEY,
                rate_date DATE NOT NULL,
                rate_per_10g NUMERIC(12, 2) NOT NULL,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)

def save_rates(history, city="Kamareddy", source="Upstox"):
    with get_connection() as conn:
        for record in history:
            for metal in METALS:
                rate = record.get(metal)
                if rate is None:
                    continue
                conn.execute("""
                    INSERT INTO market_rates
                    (rate_date, metal, rate_per_10g, city, source)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (rate_date, metal, city, source)
                    DO UPDATE SET
                        rate_per_10g = EXCLUDED.rate_per_10g,
                        fetched_at = CURRENT_TIMESTAMP
                """, (record["date"], metal, rate, city, source))

        conn.execute("""
            DELETE FROM market_rates
            WHERE rate_date < %s
        """, (date.today() - timedelta(days=14),))

def get_latest_rates():
    latest = {}
    with get_connection() as conn:
        for metal in METALS:
            row = conn.execute("""
                SELECT rate_date, rate_per_10g
                FROM market_rates
                WHERE metal = %s
                ORDER BY rate_date DESC
                LIMIT 1
            """, (metal,)).fetchone()
            if row:
                latest[metal] = {"date": row[0], "rate": row[1]}
    return latest

def get_price_history(metal: str, limit: int = 15):
    if metal not in METALS:
        raise ValueError(f"metal must be one of {METALS}")
    with get_connection() as conn:
        return conn.execute("""
            SELECT rate_date, rate_per_10g
            FROM market_rates
            WHERE metal = %s
            ORDER BY rate_date DESC
            LIMIT %s
        """, (metal, limit)).fetchall()

def get_snapshots():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT metal, rate_per_10g
            FROM report_snapshots
        """).fetchall()
    return dict(rows)

def update_snapshot(latest: dict):
    with get_connection() as conn:
        for metal, data in latest.items():
            conn.execute("""
                INSERT INTO report_snapshots
                (metal, rate_date, rate_per_10g, updated_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (metal)
                DO UPDATE SET
                    rate_date = EXCLUDED.rate_date,
                    rate_per_10g = EXCLUDED.rate_per_10g,
                    updated_at = CURRENT_TIMESTAMP
            """, (metal, data["date"], data["rate"]))
