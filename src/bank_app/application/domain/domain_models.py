import abc
import datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

import attr


@attr.dataclass
class ValueSerializer:
    value: Any

    def serialize(self) -> Any:
        if isinstance(self.value, (Decimal, UUID)):
            return str(self.value)
        if isinstance(self.value, EntityIdentity):
            return self.value.serialize()
        return self.value


class ValueObject(abc.ABC):
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __hash__(self) -> int:
        raise NotImplementedError


class EntityIdentity(ValueObject):
    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError("Subclasses must implement serialize()")

    @classmethod
    def deserialize(cls, payload: dict[str, Any]) -> Optional["EntityIdentity"]:
        if not payload:
            return None
        return cls(**payload)


class Entity(abc.ABC):
    def __init__(
        self, *args: Any, entity_id: Optional[EntityIdentity] = None, **kwargs: Any
    ) -> None:
        self.entity_id = entity_id
        super().__init__(*args, **kwargs)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.entity_id == other.entity_id
        return False

    def __hash__(self) -> int:
        return hash(self.entity_id)


class DomainService(abc.ABC):
    """
    A service used by the domain to return information from database.
    These information can not be Domain object.
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
    def delete(cls, entity_id: EntityIdentity, **kwargs: Any) -> None:
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


@attr.dataclass(frozen=True, slots=True)
class AccountIdentity(EntityIdentity):
    uuid: UUID


class Account(Entity):
    entity_id: AccountIdentity
    account_number: UUID
    balance: Decimal
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def __attrs_post_init__(self) -> None:
        """post init before instantiate"""
        if self.balance < 0:
            raise ValueError("The balance cannot be negative")
        self._validate_initial_state()

    def _validate_initial_state(self) -> None:
        pass

    @abc.abstractmethod
    def deposit(self, amount: Decimal) -> None:
        """deposit money of an account"""
        pass

    @abc.abstractmethod
    def withdraw(self, amount: Decimal) -> None:
        """redraw money of an account"""
        pass

    @abc.abstractmethod
    def has_sufficient_funds(self, amount: Decimal) -> bool:
        """check if account has enough cash"""
        pass

    @property
    @abc.abstractmethod
    def available_balance(self) -> Decimal:
        """Retrieve current amount in account"""
        pass
