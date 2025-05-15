from infrastructure.user_repository import get_user_by_email , create_user
class UserService:
    @staticmethod
    def create_user_application(name: str , email: str = None):
        existing_user = get_user_by_email(email)
        if(existing_user):
            raise Exception("Ese correo ya ha sido usado")
        user = create_user(name , email)
        return user
    @staticmethod
    def login(email: str = None):
        existing_user = get_user_by_email(email = email)
        if(existing_user is None):
            raise Exception("Ese usuario no esta registrado")
        return existing_user