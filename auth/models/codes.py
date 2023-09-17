from sqlalchemy import (
    Table,
    Column,
    String,
    DateTime,
    func,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import registry

from .users import user_table


mapper_registry = registry()


code_table = Table(
    "auth_code",
    mapper_registry.metadata,
    Column(
        "id", Integer, primary_key=True, unique=True, autoincrement=True, nullable=False
    ),
    Column("user_id", Integer, ForeignKey(user_table.c.id), nullable=False),
    Column("code", String(4), nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
)


class Code:
    pass


code_mapper = mapper_registry.map_imperatively(Code, code_table)
