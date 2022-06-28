from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime, date


class Rate(SQLModel, table=True):
    """Create an SQLModel for rates"""

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    user_id: int = Field(foreign_key="app_db.appuser.id")
    client_id: int = Field(foreign_key="app_db.client.id")
    valid_from: date
    valid_to: date
    amount: float  # currency: EUR
    created_at: datetime
    updated_at: datetime
    is_active: bool

    __table_args__ = {"schema": "app_db"}
