from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = 'USER'

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    sid = Column("sid", String)
    time_created = Column("timeCreated", DateTime(timezone=True), server_default=func.now())
    room_id = Column(ForeignKey("ROOM.id"))

    room = relationship("Room", back_populates="users")
