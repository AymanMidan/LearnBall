from datetime import datetime
from db import get_mongo_db

class Quiz:
    def __init__(self, question, options, answer, explanation, category, difficulty, image=None):
        self.question = question
        self.options = options
        self.answer = answer
        self.explanation = explanation
        self.category = category
        self.difficulty = difficulty
        self.image = image

    def to_dict(self):
        return {
            'question': self.question,
            'options': self.options,
            'answer': self.answer,
            'explanation': self.explanation,
            'category': self.category,
            'difficulty': self.difficulty,
            'image': self.image
        }

    @staticmethod
    def from_dict(data):
        return Quiz(
            question=data.get('question'),
            options=data.get('options', []),
            answer=data.get('answer'),
            explanation=data.get('explanation'),
            category=data.get('category'),
            difficulty=data.get('difficulty'),
            image=data.get('image')
        )

class UserScore:
    def __init__(self, user_id, score, total_questions, category, difficulty, time_taken, streak, badges_earned=None):
        self.user_id = user_id
        self.score = score
        self.total_questions = total_questions
        self.category = category
        self.difficulty = difficulty
        self.time_taken = time_taken
        self.streak = streak
        self.badges_earned = badges_earned or []
        self.date = datetime.utcnow()

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'score': self.score,
            'total_questions': self.total_questions,
            'category': self.category,
            'difficulty': self.difficulty,
            'time_taken': self.time_taken,
            'streak': self.streak,
            'badges_earned': self.badges_earned,
            'date': self.date
        }

    @staticmethod
    def from_dict(data):
        return UserScore(
            user_id=data.get('user_id'),
            score=data.get('score'),
            total_questions=data.get('total_questions'),
            category=data.get('category'),
            difficulty=data.get('difficulty'),
            time_taken=data.get('time_taken'),
            streak=data.get('streak'),
            badges_earned=data.get('badges_earned', [])
        )

    @staticmethod
    def save_score(score_data):
        db = get_mongo_db()
        return db.user_scores.insert_one(score_data.to_dict())

    @staticmethod
    def get_user_scores(user_id):
        db = get_mongo_db()
        return [UserScore.from_dict(score) for score in db.user_scores.find({'user_id': user_id})]