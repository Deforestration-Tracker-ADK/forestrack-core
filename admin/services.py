from authentication.enums import VolunteerVioState
from opportunity.enums import OpportunityState
from opportunity.models import Opportunity
from vio.models import Vio
from volunteer.models import Volunteer


class AdminService:
    @staticmethod
    def approveOpportunity(opportunity_id, approve):
        opportunity = Opportunity.objects.get(id=opportunity_id)
        if opportunity:
            opportunity.state = OpportunityState.APPROVED if approve else OpportunityState.REJECTED
            opportunity.save()
            return True

        return False

    @staticmethod
    def approveVio(vio_id, approve):
        vio = Vio.objects.get(id=vio_id, state=VolunteerVioState.UNAPPROVED)
        if vio:
            vio.state = VolunteerVioState.APPROVED if approve else VolunteerVioState.REJECTED
            vio.save()
            return True
        return False

    @staticmethod
    def approveVolunteer(volunteer_id, approve):
        volunteer = Volunteer.objects.get(id=volunteer_id, state=VolunteerVioState.UNAPPROVED)
        if volunteer:
            volunteer.state = VolunteerVioState.APPROVED if approve else VolunteerVioState.REJECTED
            volunteer.save()
            return True

        return False
