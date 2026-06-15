
from scripts.generate_jwt_keys import main as generate_keys


def ensure_keys():
    print("[STEP] Generating JWT keys...")
    generate_keys()