from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import Teacher, Student

UserModel = get_user_model()

class CustomAuthBackend(BaseBackend):
    """
    Кастомный бэкенд аутентификации для входа через таблицы Teacher и Student.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        # 1. Пытаемся найти пользователя в вашей таблице Teacher
        try:
            user_obj = Teacher.objects.get(login=username)
            # Если пароль в вашей таблице совпадает с введённым
            if user_obj.password_hash == password:
                # Нужно создать или получить связанного пользователя Django
                user, created = UserModel.objects.get_or_create(username=username)
                # Если пользователь только что создан, установим его пароль в хешированный вид
                if created:
                    user.password = make_password(password)
                    user.save()
                # Обновим пароль на хешированный для существующего пользователя
                elif not user.check_password(password):
                    user.set_password(password)
                    user.save()
                return user
        except Teacher.DoesNotExist:
            pass  # Пользователь не учитель, проверим среди учеников

        # 2. Если не найден как учитель, ищем в таблице Student
        try:
            user_obj = Student.objects.get(login=username)
            if user_obj.password_hash == password:
                user, created = UserModel.objects.get_or_create(username=username)
                if created:
                    user.password = make_password(password)
                    user.save()
                elif not user.check_password(password):
                    user.set_password(password)
                    user.save()
                return user
        except Student.DoesNotExist:
            pass # Пользователь не найден ни как учитель, ни как ученик

        return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None