#!/bin/bash
./certs/jwt.bat

alembic upgrade head

python -m app.db.seeders.seed_run

uvicorn app.main:app --reload

