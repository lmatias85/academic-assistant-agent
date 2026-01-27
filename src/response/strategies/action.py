from src.response.entity.resolver import EntityResolver
from src.response.entity.errors import EntityNotFoundError, EntityAmbiguousError
from response.agent.types_agent import RouterDecision
from src.response.strategies.base import RouteStrategy
from src.response.strategies.tool_registry import TOOL_REGISTRY


class ActionStrategy(RouteStrategy):
    def __init__(self) -> None:
        self.resolver = EntityResolver()

    def execute(self, user_input: str, decision: RouterDecision) -> None:
        if decision.tool_name is None:
            print("\n[Action Error] No tool specified.")
            return

        if decision.arguments is None:
            print("\n[Action Error] Missing arguments for action.")
            return

        try:
            resolved_args = self._resolve_entities(
                decision.tool_name,
                decision.arguments,
            )
        except EntityNotFoundError as exc:
            print("\n[Entity Error]")
            print(str(exc))
            return
        except EntityAmbiguousError as exc:
            print("\n[Entity Ambiguity]")
            print(str(exc))
            return

        handler = TOOL_REGISTRY.get(decision.tool_name)
        if handler is None:
            print(f"\n[Action Error] Unknown tool: {decision.tool_name}")
            return

        try:
            message = handler(resolved_args)
        except Exception as exc:
            print("\n[Action Error]")
            print(str(exc))
            return

        print("\n[Action Result]")
        print(message)

    def _resolve_entities(self, tool_name: str, args: dict) -> dict:
        resolved = dict(args)

        if "student_name" in args:
            student = self.resolver.resolve_student(args["student_name"])
            resolved["student_name"] = student["student_name"]

        if "subject_name" in args:
            subject = self.resolver.resolve_subject(args["subject_name"])
            resolved["subject_name"] = subject["subject_name"]

        return resolved
