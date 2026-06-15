from .db import migrate_db, seed_db
from .jwt_keys import ensure_keys
from .server import start_server


def dev():
    print("[DEV] Bootstrapping app...\n")

    ensure_keys()
    migrate_db()
    seed_db()

    start_server()