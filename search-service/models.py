import re
from enum import Enum

from database import SQL_PLACEHOLDER, Database


class Status(str, Enum):
    """Enumeration with valid states visible to the user.

    Used to avoid the user to search a property with a state that should ve invisible to them.
    """

    pre_sale = "pre_venta"
    on_sale = "en_venta"
    sold = "vendido"


class Property:
    address: str
    city: str
    price: int
    description: str | None
    status: Status
    _base_query = """
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

    def __init__(
        self, address: str, city: str, price: int, description: str | None, state: str
    ):
        self.address = address
        self.city = city
        self.price = price
        self.description = description
        self.status = Status(state)

    @classmethod
    def _get_result_set(
        cls, query: str, params: list | dict | None
    ) -> list["Property"]:
        """Query the database and returns a list of Property objects from the resultset."""
        connection = Database.connect()
        cursor = connection.cursor()
        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result_set = cursor.fetchall()
        cursor.close()
        return [cls(*record) for record in result_set]

    @classmethod
    def _parse_where_clause(cls, conditions: list[str]) -> str:
        """Add filter conditions to the base query where clause."""
        query = re.sub(
            r"(WHERE\s.*)[;A-Z]",
            lambda m: " and ".join([m.group(1)] + conditions) + ";",
            cls._base_query,
        )
        return query

    @classmethod
    def search(
        cls,
        year: int | None = None,
        city: str | None = None,
        status: Status | None = None,
    ) -> list["Property"]:
        """Retrieves a list of properties from the database.

        Supports optional filters for year, city, and state.
        """
        conditions = []
        params = []
        if year is not None:
            conditions.append(f"p.year = {SQL_PLACEHOLDER}")
            params.append(year)
        if city is not None:
            conditions.append(f"p.city = {SQL_PLACEHOLDER}")
            params.append(city)
        if status is not None:
            conditions.append(f"s.name = {SQL_PLACEHOLDER}")
            params.append(status.value)
        if conditions:
            query = cls._parse_where_clause(conditions)
        else:
            query = cls._base_query
            params = None
        return cls._get_result_set(query, params)

    def __repr__(self):
        arguments = ", ".join(
            [
                f'address="{self.address}"',
                f'city="{self.city}"',
                f"price={self.price}",
                f'description="{self.description}"',
                f'status="{self.status}"',
            ]
        )
        return f"{self.__class__.__name__}({arguments})"
