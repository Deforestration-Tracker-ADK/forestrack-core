from authentication.enums import VolunteerVioState
from volunteer.models import Volunteer


class VolunteerService:
    @staticmethod
    def getVolunteer(state=VolunteerVioState.APPROVED, num_of=None):
        if num_of is None:
            return Volunteer.objects.filter(state=state).order_by("-created_at").values()
        else:
            return Volunteer.objects.filter(state=state).order_by("-created_at").values()[:num_of]
