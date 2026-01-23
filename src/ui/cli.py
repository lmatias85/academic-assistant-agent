def start_cli() -> None:
    """
    Minimal CLI to validate environment and project setup.
    """
    print("Academic System Assistant")
    print("-------------------------")
    print("Environment loaded successfully.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input(">> ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        print(f"You said: {user_input}")
