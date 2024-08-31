"""This module defines serializer classes that turn model objects into json compatuble dictonaries."""

from models import Property


class PropertySerializer:
    _fields: list[str] = [
        "address",
        "city",
        "price",
        "description",
        "status",
    ]

    @classmethod
    def to_dict(cls, p: Property):
        return {field: p.__getattribute__(field) for field in cls._fields}
