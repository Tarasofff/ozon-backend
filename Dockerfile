FROM python:3.13.3-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN sudo apt-get install libcairo2 pango1.0-tools libpango-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

RUN chmod +x ./scripts/entrypoint.sh    

ENTRYPOINT ["./scripts/entrypoint.sh"]
