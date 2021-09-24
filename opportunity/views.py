# Create your views here.
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from opportunity.enums import OpportunityState
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
