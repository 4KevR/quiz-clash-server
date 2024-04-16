from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


class QuestionOption(Base):
    __tablename__ = 'QUESTION_OPTION'

    id = Column("id", Integer, primary_key=True)
    question_option = Column("questionOption", String)
    is_right = Column("isRight", Boolean)
    question_id = Column(ForeignKey("QUESTION.id"))

    question = relationship("Question", back_populates="question_options")
