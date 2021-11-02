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


class GetImagesForDistrict(GenericAPIView):
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def get(request, district, no_of):
        if (district is None) or (district not in districts_list) or (no_of is None):
            return response.Response({"No such district or error in Number of districts"},
                                     status=status.HTTP_400_BAD_REQUEST)

        images = ForestStatsService.get_images_district(district, int(no_of))
        _response = response.Response(images, status=status.HTTP_200_OK)

        return _response
