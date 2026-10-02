from enum import Enum as PyEnum

class Role(str, PyEnum):
    ADMIN = "admin"
    CUSTOMER = "customer"

class Gender(str, PyEnum):
    MALE = "male"
    FEMALE = "female"

class AccountType(str, PyEnum):
    CHECKING = "checking"
    SAVING = "saving"

class TransferType(str, PyEnum):
    WIRE_TRANSFER = "wire_transfer"
    LOCAL_TRANSFER = "local_transfer"
    INTERNAL_TRANSFER = "internal_transfer"

class ChatStatus(str, PyEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class Status(str, PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class AccountStatus(str, PyEnum):
    ACTIVE = "active"
    FROZEN = "frozen"
    RESTRICTED = "restricted"
