from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class EpicArea(SQLModel, table=True):
    """Create an SQLModel for epic areas"""

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    epic_id: int = Field(foreign_key="app_db.epic.id")
    name: str
    is_active: bool
    start_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    __table_args__ = {"schema": "app_db"}
