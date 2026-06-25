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

    # v0.0.3 新的分类体系
    error_category: Mapped[str] = mapped_column(
        String(32), index=True,
        comment="CE, RE_div0, RE_oob, WA_logic, WA_code, TLE, MLE"
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

    # v0.0.3 AI 自动生成的错误点清单
    error_points: Mapped[Optional[list]] = mapped_column(SAJson, nullable=True)

    # v0.0.3 新增反思/手动补充错误点字段
    reflection: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    resolved: Mapped[bool] = mapped_column(default=False)
    resolved_at: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
