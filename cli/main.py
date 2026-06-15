import sys

from .dev import dev
from .db import migrate_db, seed_db
from .server import start_server


def main():
    if len(sys.argv) < 2:
        print("Usage: app <command>")
        print("Commands: dev | start | db migrate | db seed")
        raise SystemExit(1)

    cmd = sys.argv[1]

    if cmd == "dev":
        dev()
    elif cmd == "start":
        start_server()
    elif cmd == "db":
        if len(sys.argv) < 3:
            print("Usage: app db migrate|seed")
            raise SystemExit(1)

        sub = sys.argv[2]

        if sub == "migrate":
            migrate_db()
        elif sub == "seed":
            seed_db()
        else:
            raise SystemExit(f"Unknown db command: {sub}")
    else:
        raise SystemExit(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()