# Ovdje se radi custom provjera log in podataka da bi se moglo loginat sa email+password ILI username+password

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):

    def authenticate(self, request, username = None, password = None, **kwargs):

        if username is None or password is None:
            return None
        
        try:
            if '@' in username:
                user = User.objects.get(email = username)
            else:
                user = User.objects.get(username = username)

        except User.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user

        return None