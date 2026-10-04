from getpass import getpass
import hotel_fastapi.models
from hotel_fastapi.database import SessionLocal
from hotel_fastapi.models.user import User
from hotel_fastapi.security import hash_password


def create_superuser():
    username = input('username: ')
    email = input('email: ')
    password = getpass('password: ')
    confirm_password = getpass('confirm password: ')

    if len(username) < 3:
        print('username must be at least 3 characters')
        return
    if len(password) < 8:
        print('password must be at least 8 characters')
        return
    if password != confirm_password:
        print('passwords do not match')
        return

    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        if existing_user:
            print('user with this email or username already exists')
            return

        admin = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role='admin'
        )
        db.add(admin)
        db.commit()
        print(f'superuser {username} created')
    finally:
        db.close()


if __name__ == '__main__':
    create_superuser()