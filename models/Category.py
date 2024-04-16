from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Category(Base):
    __tablename__ = 'CATEGORY'

    id = Column("id", Integer, primary_key=True)
    category_name = Column("categoryName", String)

    questions = relationship("Question", back_populates="category")
    game_categories = relationship("GameCategory", back_populates="category")
