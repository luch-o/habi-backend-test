import re
from enum import Enum

from connection import connection


class State(str, Enum):
    """Enumeration with valid states visible to the user.

    Used to avoid the user to search a property with a state that should ve invisible to them.
    """

    pre_sale = "pre_venta"
    on_sale = "en_venta"
    sold = "vendido"


class Property:
    base_query = """
    SELECT
        -- the fields we want to return to the user
        p.address,
        p.city,
        p.price,
        p.description,
        s.name
    FROM status_history sh
    JOIN (
        -- subquery to associate a property with its last update date
        -- and thus its active state
        SELECT property_id, max(update_date) as update_date
        FROM status_history GROUP BY property_id
    ) shf
        ON sh.property_id = shf.property_id and sh.update_date = shf.update_date
    JOIN status s
        ON sh.status_id = s.id
    JOIN property p
        ON sh.property_id = p.id
    -- exclude properties with states we want to hide from users and invalid records with price = 0
    WHERE
        s.name in ("pre_venta", "en_venta", "vendido") and p.price > 0;
    """

    @staticmethod
    def _get_result_set(query: str, params: list | dict | None) -> tuple[tuple]:
        """Query the database and returns de resultset."""
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result_set = cursor.fetchall()
        return result_set

    @classmethod
    def _parse_where_clause(cls, conditions: list[str]) -> str:
        """Add filter conditions to the base query where clause."""
        query = re.sub(
            r"(WHERE\s.*)[;A-Z]",
            lambda m: " and ".join([m.group(1)] + conditions) + ";",
            cls.base_query,
        )
        return query

    @classmethod
    def search(
        cls,
        year: int | None = None,
        city: str | None = None,
        state: State | None = None,
    ) -> tuple[tuple]:
        """Retrieves a list of properties from the database.

        Supports optional filters for year, city, and state.
        """
        conditions = []
        params = {}
        if year is not None:
            conditions.append("p.year = %(year)s")
            params["year"] = year
        if city is not None:
            conditions.append("p.city = %(city)s")
            params["city"] = city
        if state is not None:
            conditions.append("s.name = %(state)s")
            params["state"] = state.value
        if conditions:
            query = cls._parse_where_clause(conditions)
        else:
            query = cls.base_query
            params = None
        return cls._get_result_set(query, params)
