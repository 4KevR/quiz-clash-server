from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Room(Base):
    __tablename__ = 'ROOM'

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    code = Column("code", String)
    active = Column("active", Boolean)

    users = relationship("User", back_populates="room")
