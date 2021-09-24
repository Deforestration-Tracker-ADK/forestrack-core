# Create your views here.
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from opportunity.serializers import OpportunitySerializer
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
