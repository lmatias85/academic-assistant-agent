class EntityNotFoundError(Exception):
    pass


class EntityAmbiguousError(Exception):
    def __init__(self, entity_type: str, candidates: list[str]):
        self.entity_type = entity_type
        self.candidates = candidates
        super().__init__(
            f"Ambiguous {entity_type}. Candidates: {', '.join(candidates)}"
        )
