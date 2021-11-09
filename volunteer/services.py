from authentication.enums import VolunteerVioState
from authentication.models import User
from volunteer.models import Volunteer


class VolunteerService:
    """
    Volunteer Component
    Service Class
    """

    @staticmethod
    def getVolunteer(state=VolunteerVioState.APPROVED, num_of=None):
        """
        get list of volunteer of a particular state
        :param state:
        :param num_of:
        :return: List of volunteers
        """
        if num_of is None:
            return Volunteer.objects.filter(state=state).order_by("-created_at").values()
        else:
            return Volunteer.objects.filter(state=state).order_by("-created_at").values()[:num_of]

    @staticmethod
    def getVolunteerById(volunteer_id):
        """
        get a volunteer by volunteer_id
        :param volunteer_id:
        :return: Volunteer
        """
        volunteer = Volunteer.objects.filter(user_id=volunteer_id).values()[0]
        user = User.objects.filter(id=volunteer_id).values()[0]
        volunteer["user"] = user

        return volunteer
