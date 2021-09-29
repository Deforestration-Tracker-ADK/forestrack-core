from authentication.enums import VolunteerVioState, UserType
from authentication.models import User
from opportunity.enums import OpportunityState
from opportunity.models import Opportunity
from vio.models import Vio
from volunteer.models import Volunteer


class AdminService:
    @staticmethod
    def approveOpportunity(opportunity_id, approve):
        try:
            opportunity = Opportunity.objects.get(id=opportunity_id, state=OpportunityState.UNAPPROVED)
            opportunity.state = OpportunityState.APPROVED if approve else OpportunityState.REJECTED
            opportunity.save()
            return True

        except Opportunity.DoesNotExist as no_volunteer:
            return False

    @staticmethod
    def approveVio(vio_id, approve):
        try:
            vio = Vio.objects.get(user_id=vio_id, state=VolunteerVioState.UNAPPROVED)
            vio.state = VolunteerVioState.APPROVED if approve else VolunteerVioState.REJECTED
            vio.save()
            return True

        except Vio.DoesNotExist as no_volunteer:
            return False

    @staticmethod
    def approveVolunteer(volunteer_id, approve):
        try:
            volunteer = Volunteer.objects.get(user_id=volunteer_id, state=VolunteerVioState.UNAPPROVED)
            volunteer.state = VolunteerVioState.APPROVED if approve else VolunteerVioState.REJECTED
            volunteer.save()
            return True

        except Volunteer.DoesNotExist as no_volunteer:
            return False

    @staticmethod
    def getListOfAdmins():
        try:
            users = User.objects.filter(user_type=UserType.ADMIN).order_by('created_at').values()
            return users

        except User.DoesNotExist as no_user:
            return None
