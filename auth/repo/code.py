from dataclasses import asdict

from services.codes.types import CodeTypeEnum, CodeType
from services.entries import CreateCodeEntry
from services.codes.repo import ICodeRepo
from models.codes import Code


class CodeRepo(ICodeRepo):
    model = Code

    def create(self, entry: CreateCodeEntry) -> CodeType:
        entry.type = entry.type.value
        code = self.model(**asdict(entry))
        with self.session_factory() as session:
            session.add(code)
            session.commit()
            session.refresh(code)
        return code

    def get_last(self, user_id: int, type: CodeTypeEnum) -> CodeType | None:
        with self.session_factory() as session:
            return (
                session.query(self.model)
                .filter(Code.user_id == user_id, Code.type == type.value)
                .order_by(Code.created_at.desc())
                .first()
            )
