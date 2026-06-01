from sqlalchemy.orm import Session
from app.models.user_model import User
from app.core.security import hash_password, verify_password

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, name: str, email: str, password: str) -> User:
        """Create a new user"""
        user = User(name=name, email=email, password=hash_password(password))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> User:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def verify_user_credentials(self, email: str, password: str) -> User:
        """Verify user credentials"""
        user = self.get_user_by_email(email)
        if user and verify_password(password, user.password):
            return user
        return None

    def update_user(self, user: User, name: str, email: str) -> User:
        """Update user profile details"""
        user.name = name
        user.email = email
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_password(self, user: User, password: str) -> User:
        """Update user password"""
        user.password = hash_password(password)
        self.db.commit()
        self.db.refresh(user)
        return user
