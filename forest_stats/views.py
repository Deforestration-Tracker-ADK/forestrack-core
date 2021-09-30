from rest_framework import response, status
from rest_framework.generics import GenericAPIView

from forest_stats.enum import districts_list
from forest_stats.services import ForestStatsService


class GetAllForestStats(GenericAPIView):
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def get(request, district):
        if (district is None) or (district not in districts_list):
            return response.Response({"No such district"}, status=status.HTTP_400_BAD_REQUEST)

        return response.Response(ForestStatsService.get_stats_district(district), status=status.HTTP_200_OK)
