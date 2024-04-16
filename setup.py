import json
from database.Base import init_db, db_session
from models import Category, Question, QuestionOption

init_db()

with open("categories.json") as file:
    data = json.loads(file.read())
    for category in data:
        category_model = Category(id=category['id'], category_name=category['categoryName'])
        db_session.add(category_model)
        for question in category['questions']:
            question_model = Question(id=question['id'], question=question['question'], category_id=category_model.id)
            db_session.add(question_model)
            for question_option in question['questionOptions']:
                question_option_model = QuestionOption(question_option=question_option['questionOption'],
                                                       is_right=question_option['isRight'],
                                                       question_id=question_model.id)
                db_session.add(question_option_model)

    db_session.commit()
