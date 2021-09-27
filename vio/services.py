from authentication.enums import VolunteerVioState
from opportunity.enums import VolunteerOpportunityState
from opportunity.models import VolunteerOpportunity
from vio.models import Vio


class VioService:
    @staticmethod
    def approveVolunteerForOpportunity(vol_opp_id, approve, user):
        try:
            volunteer_opportunity = VolunteerOpportunity.objects.get(id=vol_opp_id,
                                                                     state=VolunteerOpportunityState.PENDING)
            if volunteer_opportunity.opportunity.vio_id != user.id:
                return False

            volunteer_opportunity.state = VolunteerOpportunityState.ACCEPTED if approve else VolunteerOpportunityState.REJECTED
            volunteer_opportunity.save()
            return True

        except VolunteerOpportunity.DoesNotExist:
            return False

    @staticmethod
    def getVio(state=VolunteerVioState.APPROVED, num_of=None):
        if num_of is None:
            return Vio.objects.filter(state=state).order_by("created_at").values()
        else:
            return Vio.objects.filter(state=state).order_by("created_at").values()[:num_of]
