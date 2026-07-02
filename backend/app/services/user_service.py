"""
========================================
Project : BharatAI
Module  : User Service
Purpose : Business Logic for User APIs
========================================
"""

from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.schemas.user import UserRegister
from backend.app.core.security import (
    hash_password,
    verify_password
)


# ======================================
# Register New User
# ======================================
def create_user(db: Session, user: UserRegister):

    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        return None

    # Create new user
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ======================================
# Authenticate User
# ======================================
def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        return None

    if not verify_password(
        password,
        user.password
    ):
        return None

    return user


# ======================================
# Get User By Email
# ======================================
def get_user_by_email(
    db: Session,
    email: str
):

    return db.query(User).filter(
        User.email == email
    ).first()