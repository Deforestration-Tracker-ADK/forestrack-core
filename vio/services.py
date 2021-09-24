from opportunity.enums import VolunteerOpportunityState
from opportunity.models import VolunteerOpportunity


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
