from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class GameCategory(Base):
    __tablename__ = 'GAME_CATEGORY'

    id = Column("id", Integer, primary_key=True)
    category_id = Column(ForeignKey("CATEGORY.id"))
    room_id = Column(ForeignKey("ROOM.id"))
    question_id = Column(ForeignKey("QUESTION.id"))

    category = relationship("Category", back_populates="game_categories")
    room = relationship("Room", back_populates="game_categories")
    question = relationship("Question", back_populates="game_categories")
