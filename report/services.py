from report.models import DeforestationReport, ReportPhoto


class ReportService:
    @staticmethod
    def get_reports_without_images(district, num_of=None):
        """
        Get Reports of a district without images
        :param district: district name
        :param num_of: Num of Reports to load
        :return: list of reports
        """
        if num_of is None:
            return DeforestationReport.objects.filter(district=district).order_by("-created_at").values()
        else:
            return DeforestationReport.objects.filter(district=district).order_by("-created_at").values()[:num_of]

    @staticmethod
    def get_reports_with_image(report_id):
        """
        Load report details and images
        :param report_id: Report Id
        :return: {dict} report details
        """
        if DeforestationReport.objects.filter(id=report_id).exists():
            photos = []
            report = DeforestationReport.objects.filter(id=report_id).values()[0]

            # load image urls
            for img in ReportPhoto.objects.filter(report_id=report_id):
                photos.append(img.image.url)

            report["images"] = photos

            return report

        return None
