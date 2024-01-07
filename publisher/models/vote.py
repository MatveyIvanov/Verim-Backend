from sqlalchemy import Table, Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import registry

from .publication import publication_table


mapper_registry = registry()


vote_table = Table(
    "publisher_vote",
    mapper_registry.metadata,
    Column(
        "id", Integer, primary_key=True, unique=True, autoincrement=True, nullable=False
    ),
    Column(
        "publication_id",
        Integer,
        ForeignKey(publication_table.c.id, ondelete="CASCADE"),
        nullable=False,
    ),
    Column("user_id", Integer, nullable=False),
    Column("believed", Boolean, nullable=False),
)


class Publication:
    pass


publication_mapper = mapper_registry.map_imperatively(Publication, publication_table)
