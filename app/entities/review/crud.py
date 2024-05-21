from app.database import SessionLocal


class ReviewCRUD:
    def __init__(self, db: SessionLocal):
        self.db = db