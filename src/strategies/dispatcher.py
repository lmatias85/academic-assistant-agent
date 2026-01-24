from src.agent.types import Route
from src.strategies.informational import InformationalStrategy
from src.strategies.action import ActionStrategy
from src.strategies.base import RouteStrategy


class StrategyDispatcher:
    """
    Maps a decided route to its execution strategy.
    """

    def __init__(self) -> None:
        self._strategies: dict[Route, RouteStrategy] = {
            Route.INFORMATIONAL: InformationalStrategy(),
            Route.ACTION: ActionStrategy(),
        }

    def dispatch(self, route: Route) -> RouteStrategy:
        return self._strategies[route]
