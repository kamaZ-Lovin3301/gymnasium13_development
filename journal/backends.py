from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import Teacher, Student, Parent

UserModel = get_user_model()

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            user_obj = Teacher.objects.get(login=username)
            if user_obj.password_hash == password:
                user, created = UserModel.objects.get_or_create(username=username)
                if created:
                    user.password = make_password(password)
                    user.save()
                elif not user.check_password(password):
                    user.set_password(password)
                    user.save()
                return user
        except Teacher.DoesNotExist:
            pass

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
            pass

        try:
            parent_obj = Parent.objects.get(login=username)
            if parent_obj.password_hash == password:
                user, created = UserModel.objects.get_or_create(username=username)
                if created:
                    user.password = make_password(password)
                    user.save()
                elif not user.check_password(password):
                    user.set_password(password)
                    user.save()
                return user
        except Parent.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None