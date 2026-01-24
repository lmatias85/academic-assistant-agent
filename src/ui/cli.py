from src.agent.primary_agent import PrimaryAgent
from src.agent.types import Route
from src.graph.informational_graph import build_informational_graph


def start_cli() -> None:
    agent = PrimaryAgent()
    informational_graph = build_informational_graph()
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

        if decision.route == Route.INFORMATIONAL:
            result = informational_graph.invoke(
                {
                    "user_input": user_input,
                    "kg_context": None,
                    "rag_context": None,
                    "answer": None,
                }
            )
            print("\n[Answer]")
            print(result["answer"])
        else:
            print("\n[Action]")
            print("Action handling via MCP Server (not implemented yet).")

        print()
