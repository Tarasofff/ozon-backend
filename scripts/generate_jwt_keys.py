from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

CERT_DIR = Path("certs")
PRIVATE_KEY_PATH = CERT_DIR / "jwt-private.pem"
PUBLIC_KEY_PATH = CERT_DIR / "jwt-public.pem"


def keys_exist() -> bool:
    return PRIVATE_KEY_PATH.exists() and PUBLIC_KEY_PATH.exists()


def generate_keys():
    CERT_DIR.mkdir(parents=True, exist_ok=True)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    PRIVATE_KEY_PATH.write_bytes(private_pem)
    PUBLIC_KEY_PATH.write_bytes(public_pem)

    print("[OK] Keys generated")


def main():
    if keys_exist():
        print("[SKIP] JWT keys already exist")
        return

    generate_keys()


if __name__ == "__main__":
    main()