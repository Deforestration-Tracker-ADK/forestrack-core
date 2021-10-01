from opportunity.enums import OpportunityState, VolunteerOpportunityState
from opportunity.models import Opportunity, VolunteerOpportunity
from vio.models import Vio


class OpportunityService:
    @staticmethod
    def getOpportunities(state=OpportunityState.APPROVED, num_of=None):
        if num_of is None:
            return Opportunity.objects.filter(state=state).order_by("-created_at").values()
        else:
            return Opportunity.objects.filter(state=state).order_by("-created_at").values()[:num_of]

    @staticmethod
    def getVolunteerOpportunitiesForVolunteer(vol_id, state=VolunteerOpportunityState.ACCEPTED, num_of=None):
        if num_of is None:
            return VolunteerOpportunity.objects.filter(volunteer_id=vol_id, state=state).order_by(
                "-created_at").values()
        else:
            return VolunteerOpportunity.objects.filter(volunteer_id=vol_id, state=state).order_by(
                "created_at").values()[:num_of]

    @staticmethod
    def getVolunteersForOpportunity(opportunity_id, state=VolunteerOpportunityState.ACCEPTED, num_of=None):
        if num_of is None:
            return VolunteerOpportunity.objects.filter(opportunity_id=opportunity_id, state=state).order_by(
                "created_at").values()
        else:
            return VolunteerOpportunity.objects.filter(opportunity_id=opportunity_id, state=state).order_by(
                "created_at").values()[:num_of]

    @staticmethod
    def searchOpportunitiesByName(search_term, num_of=None):
        if search_term is None:
            return None

        if num_of is None:
            return Opportunity.objects.filter(name__unaccent__icontains=search_term).order_by('-created_at').values()
        else:
            return VolunteerOpportunity.objects.filter(name__unaccent__icontains=search_term).order_by(
                "created_at").values()[:num_of]

    @staticmethod
    def getOpportunityById(opportunity_id):
        if Opportunity.objects.filter(id=opportunity_id, state=OpportunityState.APPROVED).exists():
            opportunity = Opportunity.objects.filter(id=opportunity_id).values()[0]
            print(opportunity)
            opportunity["vio"] = Vio.objects.filter(user_id=opportunity["vio_id"]).values()[0]

            return opportunity

        return None

    @staticmethod
    def getOpportunityByVioId(vio_id):
        opportunity = Opportunity.objects.filter(vio_id=vio_id).values()
        return opportunity
