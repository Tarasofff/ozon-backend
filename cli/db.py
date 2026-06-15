from alembic.config import Config
from alembic import command
from app.db.seeders.seed_run import main as seed_main



def migrate_db():
    print("[DB] Running migrations...")

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

def seed_db():
    print("[DB] Seeding database...")
    seed_main()
