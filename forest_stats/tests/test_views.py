from rest_framework.test import APITestCase, APIClient

from forest_stats.models import ForestStats


class ForestStatsIntegrationTests(APITestCase):
    """
    Forestrack statistics component
    Endpoint Testing
    """

    def setUp(self) -> None:
        self.rest_client = APIClient()

        # create data entry 1
        self.test_data0 = {
            "district": "Ampara",
            "water": 158,
            "artificial_bare_ground": 4778,
            "artificial_natural_ground": 63,
            "woody": 298.38478,
            "non_woody_cultivated": 348.394,
            "non_woody_natural": 45.139,
            "mean_ndvi": 2893.633,
            "mean_burn_index": 3647.9384,
        }

        self.stat_data0 = ForestStats.objects.create(**self.test_data0)

        # create data entry 2
        self.test_data1 = {
            "district": "Ampara",
            "water": 1.58,
            "artificial_bare_ground": 47.78,
            "artificial_natural_ground": 683.9,
            "woody": 678.3847,
            "non_woody_cultivated": 38.394,
            "non_woody_natural": 20.4857,
            "mean_ndvi": 150.3487,
            "mean_burn_index": 45.4,
        }

        self.stat_data1 = ForestStats.objects.create(**self.test_data1)

    def test_stats_district(self):
        """
        Testing Getting statistics end point
        :return:
        """
        response = self.rest_client.get(f"/api/forest_stats/stats/{self.test_data0['district']}")
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data["district"], self.test_data0["district"])
        self.assertEqual(float(data["last_month"]["water"]), self.test_data1["water"])
        self.assertEqual(float(data["change"]["water"]), self.test_data1["water"] - self.test_data0["water"])
