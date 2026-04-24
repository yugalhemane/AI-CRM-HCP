from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class InteractionRecord(Base):
    __tablename__ = "interaction_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_input: Mapped[str] = mapped_column(Text, nullable=False)
    tool_used: Mapped[str] = mapped_column(String(100), nullable=False, default="unknown")
    assistant_message: Mapped[str] = mapped_column(Text, nullable=False, default="")
    form_data: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
