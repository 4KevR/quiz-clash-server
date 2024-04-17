from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Room(Base):
    __tablename__ = 'ROOM'

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    amount_of_players = Column("amount_of_players", Integer)
    code = Column("code", String)
    active = Column("active", Boolean)
    question_count = Column("questionCount", Integer, default=0)

    users = relationship("User", back_populates="room")
    game_categories = relationship("GameCategory", back_populates="room")
