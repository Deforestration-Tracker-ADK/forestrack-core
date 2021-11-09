from authentication.enums import VolunteerVioState
from authentication.models import User
from opportunity.enums import VolunteerOpportunityState
from opportunity.models import VolunteerOpportunity
from vio.models import Vio


class VioService:
    """
    VIO component of the system
    Service class
    """

    @staticmethod
    def approveVolunteerForOpportunity(vol_opp_id, approve, user):
        """
        Approve or reject a volunteer for a opportunity
        :param vol_opp_id:
        :param approve: approve or reject
        :param user: vio user
        :return: true/false
        """
        try:
            volunteer_opportunity = VolunteerOpportunity.objects.get(id=vol_opp_id,
                                                                     state=VolunteerOpportunityState.PENDING)
            if volunteer_opportunity.opportunity.vio_id != user.id:
                return False

            # change state to ACCEPTED if approved else REJECTED
            volunteer_opportunity.state = VolunteerOpportunityState.ACCEPTED if approve else VolunteerOpportunityState.REJECTED
            volunteer_opportunity.save()
            return True

        except VolunteerOpportunity.DoesNotExist:
            return False

    @staticmethod
    def getVio(state=VolunteerVioState.APPROVED, num_of=None):
        """
        Get  VIO details list of a particular state
        :param state:
        :param num_of:
        :return:
        """
        if num_of is None:
            return Vio.objects.filter(state=state).order_by("-created_at").values()
        else:
            return Vio.objects.filter(state=state).order_by("-created_at").values()[:num_of]

    @staticmethod
    def getVioById(vio_id):
        """
        Get Vio details for a VIO id
        :param vio_id:
        :return:
        """
        volunteer = Vio.objects.filter(user_id=vio_id).values()[0]
        user = User.objects.filter(id=vio_id).values()[0]

        # add user details as well
        volunteer["user"] = user

        return volunteer
