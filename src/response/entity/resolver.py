from src.infrastructure.database import get_connection
from src.response.entity.errors import EntityNotFoundError, EntityAmbiguousError


class EntityResolver:
    """
    Resolves raw entity names to canonical database records.
    """

    def resolve_student(self, raw_name: str) -> dict:
        return self._resolve(
            table="student",
            id_field="student_id",
            name_field="student_name",
            raw_value=raw_name,
        )

    def resolve_subject(self, raw_name: str) -> dict:
        return self._resolve(
            table="subject",
            id_field="subject_id",
            name_field="subject_name",
            raw_value=raw_name,
        )

    def _resolve(
        self,
        table: str,
        id_field: str,
        name_field: str,
        raw_value: str,
    ) -> dict:
        conn = get_connection()
        cur = conn.cursor()

        # Fuzzy match (=)
        cur.execute(
            f"""
            SELECT {id_field}, {name_field}
            FROM {table}
            WHERE {name_field} = ?
            """,
            (f"%{raw_value}%",),
        )

        rows = cur.fetchall()
        conn.close()

        if not rows:
            raise EntityNotFoundError(f"{table} not found for value '{raw_value}'.")

        if len(rows) > 1:
            raise EntityAmbiguousError(
                entity_type=table,
                candidates=[r[name_field] for r in rows],
            )

        if len(rows) == 1:
            return {
                id_field: rows[0][id_field],
                name_field: rows[0][name_field],
            }

        # Fuzzy match (LIKE)
        cur.execute(
            f"""
            SELECT {id_field}, {name_field}
            FROM {table}
            WHERE {name_field} LIKE ?
            """,
            (f"%{raw_value}%",),
        )

        rows = cur.fetchall()
        conn.close()

        if not rows:
            raise EntityNotFoundError(f"{table} not found for value '{raw_value}'.")

        if len(rows) > 1:
            raise EntityAmbiguousError(
                entity_type=table,
                candidates=[r[name_field] for r in rows],
            )

        return {
            id_field: rows[0][id_field],
            name_field: rows[0][name_field],
        }
