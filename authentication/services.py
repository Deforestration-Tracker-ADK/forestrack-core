from authentication.enums import UserState
from authentication.models import User, VolunteerVioState


class AuthService:
    @staticmethod
    def verify_email(email_token):
        if User.objects.filter(email_token=email_token, state=VolunteerVioState.EMAIL_UNVERIFIED).exists():
            user = User.objects.get(email_token=email_token, state=UserState.EMAIL_UNVERIFIED)
            user.state = UserState.EMAIL_VERIFIED
            user.save()

            return True

        return False
