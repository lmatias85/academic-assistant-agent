from dotenv import load_dotenv
from src.infrastructure.database import init_db

# Load environment variables from .env
load_dotenv()


def main() -> None:
    """
    Application entrypoint.
    """
    from src.ui.cli import start_cli

    init_db()
    start_cli()


if __name__ == "__main__":
    main()
