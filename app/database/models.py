from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime

from datetime import datetime

# Standard field for tables
class Base(DeclarativeBase):
    timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now)

# Creating table for ads
class Advertisements(Base):
    __tablename__ = 'advertisements'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    added_photo: Mapped[str] = mapped_column(nullable=False)
    added_text: Mapped[str] = mapped_column(nullable=False)
    added_price: Mapped[str] = mapped_column(nullable=False)

# Creating premium user`s list table
class Premium(Base):
    __tablename__ = 'premium'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    timed_out: Mapped[DateTime] = mapped_column(DateTime)

class Misc(Base):
    __tablename__ = 'misc'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    welcome_image_id: Mapped[str] = mapped_column(nullable=False)