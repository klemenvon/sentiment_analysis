from dataclasses import asdict

from sqlalchemy.orm import DeclarativeBase, MappedAsDataClass


class Base(DeclarativeBase, MappedAsDataClass):
    def dict(self, exclude_unset: bool) -> dict:
        if exclude_unset:
            return {k: str(v) for k, v in asdict(self).items() if v is not None}
        return {k: str(v) for k, v in asdict(self).items()}
