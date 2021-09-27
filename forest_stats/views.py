from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from forest_stats.services import ForestStatsService


class GetAllForestStats(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request):
        return response.Response(ForestStatsService.get_all_stats(), status=status.HTTP_200_OK)
