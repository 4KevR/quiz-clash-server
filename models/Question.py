from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Question(Base):
    __tablename__ = 'QUESTION'

    id = Column("id", Integer, primary_key=True)
    question = Column("question", String)
    category_id = Column(ForeignKey("CATEGORY.id"))

    category = relationship("Category", back_populates="questions")
    question_options = relationship("QuestionOption", back_populates="question")
    game_categories = relationship("GameCategory", back_populates="question")
