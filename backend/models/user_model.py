from database import db
from werkzeug.security import generate_password_hash, check_password_hash

users_collection = db["users"]

def create_user(name, email, password):
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    users_collection.insert_one({"name": name, "email": email, "password": hashed_password})
    return True

def find_user_by_email(email):
    return users_collection.find_one({"email": email})

def verify_password(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)

def get_all_users():
    users_cursor = users_collection.find({}, {"_id": 0, "password": 0}) 
    return list(users_cursor)

def delete_user_by_email(email):
    """
    Delete a user from the 'users' collection based on email.
    Returns True if deleted, False if no user was found.
    """
    result = users_collection.delete_one({"email": email})
    return result.deleted_count > 0


def update_user(email, new_name=None, new_email=None, password=None):
    """
    Update a user in the 'users' collection based on email.
    Returns True if updated, False if no user was found.
    """
    update_data = {}
    if new_name:
        update_data["name"] = new_name
    if new_email:
        update_data["email"] = new_email
    if password:
        update_data["password"] = generate_password_hash(password, method="pbkdf2:sha256")

    if not update_data:
        return False

    result = users_collection.update_one({"email": email}, {"$set": update_data})
    return result.matched_count > 0
