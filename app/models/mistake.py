from sqlalchemy import String, Text, Integer, ForeignKey, JSON as SAJson
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional
import datetime
from app.models.database import Base


class Mistake(Base):
    __tablename__ = "mistakes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    submission_id: Mapped[int] = mapped_column(ForeignKey("submissions.id", ondelete="CASCADE"))
    submission: Mapped["Submission"] = relationship(back_populates="mistakes")

    error_category: Mapped[str] = mapped_column(
        String(32), index=True,
        comment="logic_error, boundary, overflow, uninitialized, complexity, precision, io_format, memory, typo, modular, graph, dp"
    )
    error_severity: Mapped[str] = mapped_column(
        String(16),
        comment="low / high"
    )

    error_summary: Mapped[str] = mapped_column(Text)
    error_detail: Mapped[str] = mapped_column(Text)
    suggestion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    hints: Mapped[Optional[list]] = mapped_column(SAJson, nullable=True)
    current_hint_index: Mapped[int] = mapped_column(default=0)

    resolved: Mapped[bool] = mapped_column(default=False)
    resolved_at: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
