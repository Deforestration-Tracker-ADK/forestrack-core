from authentication.enums import VolunteerVioState
from authentication.models import User
from volunteer.models import Volunteer


class VolunteerService:
    @staticmethod
    def getVolunteer(state=VolunteerVioState.APPROVED, num_of=None):
        if num_of is None:
            return Volunteer.objects.filter(state=state).order_by("-created_at").values()
        else:
            return Volunteer.objects.filter(state=state).order_by("-created_at").values()[:num_of]

    @staticmethod
    def getVolunteerById(volunteer_id):
        volunteer = Volunteer.objects.filter(user_id=volunteer_id).values()[0]
        user = User.objects.filter(id=volunteer_id).values()[0]
        volunteer["user"] = user

        return volunteer
