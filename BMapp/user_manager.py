class UserManager:
    current_user = None

    @classmethod
    def set_current_user(cls, user):
        cls.current_user = user

    @classmethod
    def get_current_user(cls):
        return cls.current_user