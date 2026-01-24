from src.agent.primary_agent import PrimaryAgent
from src.agent.types import Route


def start_cli() -> None:
    """
    Minimal CLI to validate Primary Agent integration.
    """
    agent = PrimaryAgent()

    print("Academic System Assistant")
    print("-------------------------")
    print("Primary Agent initialized.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input(">> ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        decision = agent.decide(user_input)

        print(f"[Decision] Route: {decision.route.value}")
        print(f"[Reason] {decision.reason}\n")
