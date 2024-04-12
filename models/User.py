from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'USER'

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    sid = Column("sid", String)
    ready = Column("ready", Boolean, default=False)
    room_id = Column(ForeignKey("ROOM.id"))

    room = relationship("Room", back_populates="users")
