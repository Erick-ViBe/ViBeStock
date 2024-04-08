from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        extra_fields = {}
        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True
        return self.create_user(email, password, **extra_fields)
