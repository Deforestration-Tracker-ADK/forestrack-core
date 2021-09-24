from opportunity.enums import OpportunityState
from opportunity.models import Opportunity


class OpportunityService:
    @staticmethod
    def getOpportunities(state=OpportunityState.APPROVED, num_of=None):
        if num_of is None:
            return Opportunity.objects.filter(state=state).order_by("created_at").values()
        else:
            return Opportunity.objects.filter(state=state).order_by("created_at").values()[:num_of]
