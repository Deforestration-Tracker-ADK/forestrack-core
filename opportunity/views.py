# Create your views here.
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from opportunity.enums import OpportunityState, VolunteerOpportunityState
from opportunity.serializers import OpportunitySerializer
from opportunity.services import OpportunityService
from vio.permissions import IsVio


class RegisterAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVio]
    serializer_class = OpportunitySerializer

    def post(self, request):
        data = request.data
        data["vio_id"] = request.user.id
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUnapprovedOpportunity(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request):
        return response.Response(OpportunityService.getOpportunities(state=OpportunityState.UNAPPROVED),
                                 status=status.HTTP_200_OK)


class GetApprovedOpportunity(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request):
        return response.Response(OpportunityService.getOpportunities(), status=status.HTTP_200_OK)


class GetVolunteerPendingProjectsForVolunteer(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request, vol_id):
        return response.Response(
            OpportunityService.getVolunteerOpportunitiesForVolunteer(vol_id, state=VolunteerOpportunityState.PENDING),
            status=status.HTTP_200_OK)


class GetVolunteerAcceptedProjectsForVolunteer(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request, vol_id):
        return response.Response(
            OpportunityService.getVolunteerOpportunitiesForVolunteer(vol_id, state=VolunteerOpportunityState.ACCEPTED),
            status=status.HTTP_200_OK)


class GetVolunteerCompletedProjectsForVolunteer(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request, vol_id):
        return response.Response(
            OpportunityService.getVolunteerOpportunitiesForVolunteer(vol_id, state=VolunteerOpportunityState.COMPLETED),
            status=status.HTTP_200_OK)


class GetAcceptedVolunteersForOpportunity(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request, opportunity_id):
        return response.Response(
            OpportunityService.getVolunteerOpportunitiesForOpportunity(opportunity_id,
                                                                       state=VolunteerOpportunityState.ACCEPTED),
            status=status.HTTP_200_OK)


class GetPendingVolunteersForOpportunity(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request, opportunity_id):
        return response.Response(
            OpportunityService.getVolunteerOpportunitiesForOpportunity(opportunity_id,
                                                                       state=VolunteerOpportunityState.PENDING),
            status=status.HTTP_200_OK)


class GetCompletedVolunteersForOpportunity(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request, opportunity_id):
        return response.Response(
            OpportunityService.getVolunteerOpportunitiesForOpportunity(opportunity_id,
                                                                       state=VolunteerOpportunityState.COMPLETED),
            status=status.HTTP_200_OK)


class SearchOpportunity(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request):
        search_term = request.query_params.get("search")
        if search_term is None:
            response.Response("No Search term provided", status=status.HTTP_400_BAD_REQUEST)

        return response.Response(OpportunityService.searchOpportunitiesByName(search_term), status=status.HTTP_200_OK)


class GetOpportunityById(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request, opportunity_id):
        if opportunity_id is None:
            return response.Response({"message": "opportunity Id undefined"}, status=status.HTTP_400_BAD_REQUEST)
        opportunity = OpportunityService.getOpportunityById(opportunity_id)
        return response.Response(opportunity, status=status.HTTP_200_OK)


class GetOpportunityByForVio(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request, vio_id):
        if vio_id is None:
            return response.Response({"message": "opportunity Id undefined"}, status=status.HTTP_400_BAD_REQUEST)
        opportunity = OpportunityService.getOpportunityByVioId(vio_id)
        return response.Response(opportunity, status=status.HTTP_200_OK)


class GetUnapprovedOpportunityForVio(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request, vio_id):
        return response.Response(OpportunityService.getOpportunitiesForVio(vio_id, state=OpportunityState.UNAPPROVED),
                                 status=status.HTTP_200_OK)


class GetApprovedOpportunityForVio(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request, vio_id):
        return response.Response(OpportunityService.getOpportunitiesForVio(vio_id, state=OpportunityState.APPROVED),
                                 status=status.HTTP_200_OK)


class CompleteOpportunityById(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVio]

    @staticmethod
    def post(request, opportunity_id):
        if opportunity_id is None:
            return response.Response({"message": "opportunity Id undefined"}, status=status.HTTP_400_BAD_REQUEST)

        opportunity = OpportunityService.completeOpportunity(opportunity_id, request.user)
        if opportunity is None:
            return response.Response({"message": "No opportunity with that id"}, status=status.HTTP_400_BAD_REQUEST)

        return response.Response(True, status=status.HTTP_200_OK)
