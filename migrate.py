import os
import sqlite3
import sys

MIGRATIONS_DIR = "migrations"
DB_PATH = "data/scrape_results.db"


def get_applied(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS migrations (name TEXT PRIMARY KEY)")
    return {row[0] for row in conn.execute("SELECT name FROM migrations")}


def get_migration_dirs():
    dirs = sorted(d for d in os.listdir(MIGRATIONS_DIR) if os.path.isdir(f"{MIGRATIONS_DIR}/{d}"))
    return dirs


def apply_migration(conn, name):
    path = f"{MIGRATIONS_DIR}/{name}/up.sql"
    with open(path) as f:
        conn.executescript(f.read())
    conn.execute("INSERT INTO migrations (name) VALUES (?)", (name,))
    print(f"Applied: {name}")


def rollback_migration(conn, name):
    path = f"{MIGRATIONS_DIR}/{name}/down.sql"
    with open(path) as f:
        conn.executescript(f.read())
    conn.execute("DELETE FROM migrations WHERE name = ?", (name,))
    print(f"Rolled back: {name}")


def upgrade(conn):
    applied = get_applied(conn)
    for name in get_migration_dirs():
        if name not in applied:
            apply_migration(conn, name)


def downgrade(conn, steps=1):
    applied = get_applied(conn)
    candidates = [d for d in reversed(get_migration_dirs()) if d in applied]

    for name in candidates[:steps]:
        rollback_migration(conn, name)


def run():
    os.makedirs("data", exist_ok=True)
    command = sys.argv[1] if len(sys.argv) > 1 else "upgrade"
    steps = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    with sqlite3.connect(DB_PATH) as conn:
        if command == "upgrade":
            upgrade(conn)
        elif command == "downgrade":
            downgrade(conn, steps)
        else:
            print(f"Unknown command: {command}. Use 'upgrade' or 'downgrade'.")
            sys.exit(1)


if __name__ == "__main__":
    run()
