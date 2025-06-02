from app.models.user_model import UserModel

class UserController:
    @staticmethod
    def register(username, password, role_id=None):
        UserModel.create_user(username, password, role_id)
        return "User registered successfully."

    @staticmethod
    def login(username, password):
        return UserModel.authenticate(username, password)
