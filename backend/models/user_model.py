from database import db
from werkzeug.security import generate_password_hash, check_password_hash

users_collection = db["users"]

def create_user(name, email, password):
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    users_collection.insert_one({"name":name,"email": email, "password": hashed_password})
    return True

def find_user_by_email(email):
    return users_collection.find_one({"email": email})

def verify_password(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)
