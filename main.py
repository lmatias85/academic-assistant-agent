from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


def main() -> None:
    """
    Application entrypoint.
    """
    from src.ui.cli import start_cli

    start_cli()


if __name__ == "__main__":
    main()
