 # GENERATE MIGRATION
 alembic revision --autogenerate -m "migration_init"

 # RUN MIGRATION

 alembic upgrade head

 # RUN SEEDS

 python -m app.db.seeders.seed_run

 # START APP 

 uvicorn app.main:app --reload

 # KILL APP

 taskkill /F /IM python.exe