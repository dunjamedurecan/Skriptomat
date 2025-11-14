from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Ako postoji lokalni korisnik s istim emailom, automatski povežemo sociallogin s tim korisnikom.
        Ovo sprječava stvaranje duplikata accounta.
        """
        # Ako je već ulogiran, ništa ne radimo
        if request.user.is_authenticated:
            return

        # pokuša dohvatiti email iz sociallogin objekta
        email = None
        if sociallogin.user and sociallogin.user.email:
            email = sociallogin.user.email
        else:
            # ponekad je email u extra_data
            email = sociallogin.account.extra_data.get("email")

        if not email:
            return

        try:
            existing_user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return

        # povežemo social account s postojećim korisnikom
        sociallogin.connect(request, existing_user)