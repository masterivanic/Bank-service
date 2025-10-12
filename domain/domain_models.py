import abc
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

import attr


@attr.dataclass
class ValueSerializer:
    value: Any

    def serialize(self):
        if isinstance(self.value, (Decimal, UUID)):
            return str(self.value)
        if isinstance(self.value, EntityIdentity):
            return self.value.serialize()
        return self.value


class ValueObject(abc.ABC):
    def __eq__(self, other):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError


class EntityIdentity(ValueObject, abc.ABC):
    def serialize(self) -> dict:
        return attr.asdict(
            self,
            value_serializer=lambda inst, field, value: ValueSerializer(
                value
            ).serialize(),
            recurse=True,
        )

    @classmethod
    def deserialize(cls, payload: dict) -> Optional["EntityIdentity"]:
        if not payload:
            return None
        return cls(**payload)


class Entity(abc.ABC):
    def __init__(self, *args, entity_id: EntityIdentity = None, **kwargs):
        self.entity_id = entity_id
        super().__init__(*args, **kwargs)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.entity_id == other.entity_id
        return False

    def __hash__(self):
        return hash(self.entity_id)


class DomainService(abc.ABC):
    """
    A service used by the domain to return informations from database.
    These informations can not be Domain object.
    """

    pass


class AbstractRepository(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get(cls, entity_id: EntityIdentity) -> Entity:
        """
        Function used to get  entity by entity identity.
        :return: The entity
        """
        pass

    @classmethod
    @abc.abstractmethod
    def delete(cls, entity_id: EntityIdentity, **kwargs) -> None:
        """
        Function used to delete a entity via it's entity identity.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def save(cls, entity: Entity) -> None:
        """
        Function used to persist existing domain entity
        into the database.
        :param entity: Any domain entity.
        """
        pass
