from authentication.models import User
from opportunity.enums import OpportunityState, VolunteerOpportunityState
from opportunity.models import Opportunity, VolunteerOpportunity
from vio.models import Vio
from volunteer.models import Volunteer


class OpportunityService:

    @staticmethod
    def getVolunteerOpportunitiesFromId(vol_opp_id):
        if VolunteerOpportunity.objects.filter(id=vol_opp_id).exists():
            vol_opp = VolunteerOpportunity.objects.filter(id=vol_opp_id).values()[0]
            vol_opp["volunteer"] = Volunteer.objects.filter(user_id=vol_opp["volunteer_id"]).values()[0]
            vol_opp["opportunity"] = Opportunity.objects.filter(id=vol_opp["opportunity_id"]).values()[0]
            vol_opp["volunteer"]["user"] = User.objects.filter(id=vol_opp["volunteer_id"]).values()[0]
            return vol_opp

        return None

    @staticmethod
    def completeOpportunity(opportunity_id, user):
        if Opportunity.objects.filter(id=opportunity_id, vio_id=user.id, state=OpportunityState.APPROVED).exists():
            opportunity = Opportunity.objects.get(id=opportunity_id)

            volunteer_opportunities_accepted = VolunteerOpportunity.objects.filter(opportunity_id=opportunity_id,
                                                                                   state=VolunteerOpportunityState.ACCEPTED)
            for volunteer_opportunity in volunteer_opportunities_accepted:
                volunteer_opportunity.state = VolunteerOpportunityState.COMPLETED
                volunteer_opportunity.save()

            volunteer_opportunities_unaccepted = VolunteerOpportunity.objects.filter(opportunity_id=opportunity_id,
                                                                                     state=VolunteerOpportunityState.PENDING)
            for volunteer_opportunity in volunteer_opportunities_unaccepted:
                volunteer_opportunity.state = VolunteerOpportunityState.UNACCEPTED_COMPLETE
                volunteer_opportunity.save()

            opportunity.state = OpportunityState.COMPLETED
            opportunity.save()
            return True

        return None

    @staticmethod
    def getOpportunities(state=OpportunityState.APPROVED, num_of=None):
        if num_of is None:
            opportunities = Opportunity.objects.filter(state=state).order_by("-created_at").values()
            for opportunity in opportunities:
                opportunity["vio"] = Vio.objects.filter(user_id=opportunity["vio_id"]).values()[0]
            return opportunities
        else:
            opportunities = Opportunity.objects.filter(state=state).order_by("-created_at").values()[:num_of]
            for opportunity in opportunities:
                opportunity["vio"] = Vio.objects.filter(user_id=opportunity["vio_id"]).values()[0]
            return opportunities

    @staticmethod
    def getVolunteerOpportunitiesForVolunteer(vol_id, state=VolunteerOpportunityState.ACCEPTED, num_of=None):
        if num_of is None:
            vol_opp_list = VolunteerOpportunity.objects.filter(volunteer_id=vol_id, state=state).order_by(
                "-created_at").values()

            for vol_opp in vol_opp_list:
                vol_opp["volunteer"] = Volunteer.objects.filter(user_id=vol_opp["volunteer_id"]).values()[0]
                vol_opp["opportunity"] = Opportunity.objects.filter(id=vol_opp["opportunity_id"]).values()[0]

            return vol_opp_list
        else:
            vol_opp_list = VolunteerOpportunity.objects.filter(volunteer_id=vol_id, state=state).order_by(
                "-created_at").values()[:num_of]

            for vol_opp in vol_opp_list:
                vol_opp["volunteer"] = Volunteer.objects.filter(user_id=vol_opp["volunteer_id"]).values()[0]
                vol_opp["opportunity"] = Opportunity.objects.filter(id=vol_opp["opportunity_id"]).values()[0]

            return vol_opp_list

    @staticmethod
    def getVolunteerOpportunitiesForOpportunity(opportunity_id, state=VolunteerOpportunityState.ACCEPTED, num_of=None):
        if num_of is None:
            vol_opp_list = VolunteerOpportunity.objects.filter(opportunity_id=opportunity_id, state=state).order_by(
                "created_at").values()

            for vol_opp in vol_opp_list:
                vol_opp["volunteer"] = Volunteer.objects.filter(user_id=vol_opp["volunteer_id"]).values()[0]
                vol_opp["opportunity"] = Opportunity.objects.filter(id=vol_opp["opportunity_id"]).values()[0]

            return vol_opp_list
        else:
            vol_opp_list = VolunteerOpportunity.objects.filter(opportunity_id=opportunity_id, state=state).order_by(
                "created_at").values()[:num_of]

            for vol_opp in vol_opp_list:
                vol_opp["volunteer"] = Volunteer.objects.filter(user_id=vol_opp["volunteer_id"]).values()[0]
                vol_opp["opportunity"] = Opportunity.objects.filter(id=vol_opp["opportunity_id"]).values()[0]

            return vol_opp_list

    @staticmethod
    def searchOpportunitiesByName(search_term, state=OpportunityState.APPROVED, num_of=None):
        if search_term is None:
            return None

        opportunities = Opportunity.objects.filter(name__icontains=search_term, state=state).order_by(
            '-created_at').values()
        opportunities = opportunities.union(
            Opportunity.objects.filter(description__icontains=search_term, state=state).order_by(
                '-created_at').values())
        opportunities = opportunities.union(
            Opportunity.objects.filter(district__icontains=search_term, state=state).order_by(
                '-created_at').values())
        opportunities = opportunities.union(
            Opportunity.objects.filter(address__icontains=search_term, state=state).order_by(
                '-created_at').values())
        opportunities = opportunities.union(
            Opportunity.objects.filter(goals__icontains=search_term, state=state).order_by(
                '-created_at').values())

        for opportunity in opportunities:
            opportunity["vio"] = Vio.objects.filter(user_id=opportunity["vio_id"]).values()[0]

        if num_of is None:
            return opportunities
        else:
            return opportunities[:num_of]

    @staticmethod
    def getOpportunityById(opportunity_id):
        if Opportunity.objects.filter(id=opportunity_id).exists():
            opportunity = Opportunity.objects.filter(id=opportunity_id).values()[0]
            opportunity["vio"] = Vio.objects.filter(user_id=opportunity["vio_id"]).values()[0]

            return opportunity

        return []

    @staticmethod
    def getOpportunityByVioId(vio_id):
        opportunity = Opportunity.objects.filter(vio_id=vio_id, state=OpportunityState.APPROVED).values()
        return opportunity

    @staticmethod
    def getOpportunitiesForVio(vio_id, state):
        opportunity = Opportunity.objects.filter(vio_id=vio_id, state=state).values()
        return opportunity
