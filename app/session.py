class Session:
    current_user = None

    @classmethod
    def login(cls, user):
        cls.current_user = user

    @classmethod
    def logout(cls):
        cls.current_user = None

    @classmethod
    def is_authenticated(cls):
        return cls.current_user is not None

    @classmethod
    def get_user(cls):
        return cls.current_user
