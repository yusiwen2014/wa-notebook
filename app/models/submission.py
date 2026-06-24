from sqlalchemy import String, DateTime, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional
import enum
import datetime
from app.models.database import Base


class Platform(str, enum.Enum):
    LUOGU = "luogu"
    CODEFORCES = "codeforces"


class Status(str, enum.Enum):
    WA = "WA"
    TLE = "TLE"
    RE = "RE"
    CE = "CE"
    AC = "AC"
    OTHER = "OTHER"


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    platform: Mapped[Platform] = mapped_column(SAEnum(Platform), index=True)
    submission_url: Mapped[str] = mapped_column(String(512), unique=True)

    problem_id: Mapped[str] = mapped_column(String(64), index=True)
    problem_name: Mapped[str] = mapped_column(String(256))
    problem_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    difficulty: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    code: Mapped[str] = mapped_column(Text)
    language: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    status: Mapped[Status] = mapped_column(SAEnum(Status))
    failed_test_case: Mapped[Optional[int]] = mapped_column(nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    mistakes: Mapped[list["Mistake"]] = relationship(
        back_populates="submission", cascade="all, delete-orphan"
    )
