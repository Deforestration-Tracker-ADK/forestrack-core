from forest_stats.models import ForestStats

stats_title = [
    "water",
    "artificial_bare_ground",
    "artificial_natural_ground",
    "woody",
    "non_woody_cultivated",
    "non_woody_natural",
    "mean_ndvi",
    "mean_burn_index",
]


class ForestStatsService:
    @staticmethod
    def get_stats_district(district):
        result_stats = {}
        past_2_months_stat = ForestStats.objects.filter(district=district).order_by("-created_at").values()[:2]
        result_stats["last_month"] = past_2_months_stat[0]
        change_percentage = {}
        change = {}
        for key in stats_title:
            change[key] = past_2_months_stat[0][key] - past_2_months_stat[1][key]
            if past_2_months_stat[1][key] == 0:
                change_percentage[key] = "Not A Number"
            else:
                change_percentage[key] = (change[key] / past_2_months_stat[1][key]) * 100

        result_stats["change_percentage"] = change_percentage
        result_stats["change"] = change

        return result_stats
