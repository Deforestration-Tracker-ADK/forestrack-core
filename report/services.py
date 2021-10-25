from report.models import DeforestationReport, ReportPhoto


class ReportService:
    @staticmethod
    def get_reports_without_images(district, num_of=None):
        if num_of is None:
            return DeforestationReport.objects.filter(district=district).order_by("-created_at").values()
        else:
            return DeforestationReport.objects.filter(district=district).order_by("-created_at").values()[:num_of]

    @staticmethod
    def get_reports_with_image(report_id):
        if DeforestationReport.objects.filter(id=report_id).exists():
            photos = []
            report = DeforestationReport.objects.filter(id=report_id).values()[0]
            for img in ReportPhoto.objects.filter(report_id=report_id):
                photos.append(img.image.url)

            report["images"] = photos

            return report

        return None
