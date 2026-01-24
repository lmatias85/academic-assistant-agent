from src.agent.primary_agent import PrimaryAgent
from src.strategies.dispatcher import StrategyDispatcher


def start_cli() -> None:

    agent = PrimaryAgent()
    dispatcher = StrategyDispatcher()

    print("Academic System Assistant")
    print("-------------------------")
    print("Primary Agent initialized.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input(">> ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        decision = agent.decide(user_input=user_input)

        print(f"[Decision] Route: {decision.route.value}")
        print(f"[Reason] {decision.reason}\n")

        strategy = dispatcher.dispatch(route=decision.route)
        strategy.execute(user_input=user_input, decision=decision)

        print()
