import base64
import io
from datetime import datetime, timedelta

import environ
import numpy as np
from PIL import Image, ImageEnhance
from dotenv import load_dotenv
from sentinelhub import read_data, UtmZoneSplitter, CRS, SentinelHubDownloadClient, SHConfig, bbox_to_dimensions, \
    SentinelHubRequest, DataCollection, MimeType
from shapely.geometry import shape

from forest_stats.models import ForestStats
from forestrack_core import settings

load_dotenv()
env = environ.Env()

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

config = SHConfig()

config.instance_id = env("SENTINELHUB_INSTANCEID")
config.sh_client_id = env("SENTINELHUB_CLIENTID")
config.sh_client_secret = env("SENTINELHUB_CLIENT_SECRET")
config.save()

resolution = 80
needed_bands = ['B02', 'B03', 'B04']
parallel = 2

evalscript_true_color = """
    //VERSION=3
    function setup() {
        return {
            input: [{
                bands: ["B02","B03","B04"],
                units: "DN"
            }],
            output: {
                bands: 3,
                sampleType: "INT16",
                mosaicking: "SIMPLE",
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B02,
                sample.B03,
                sample.B04];
    }
"""


def get_sattelite_bands_request(time_interval, bbox, size):
    return SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=time_interval,
                mosaicking_order='leastCC'
            )],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.TIFF)
        ],
        bbox=bbox,
        size=size,
        config=config
    )


def get_satellite_images(bbox_list, bbox_info, day_slots):
    tiles = []
    for i in range(len(bbox_list)):
        bbox = bbox_list[i]
        info = bbox_info[i]
        bbox_size = bbox_to_dimensions(bbox, resolution=resolution)

        list_of_requests = [get_sattelite_bands_request(slot, bbox, bbox_size) for slot in day_slots]
        list_of_requests = [request.download_list[0] for request in list_of_requests]

        data = SentinelHubDownloadClient(config=config).download(list_of_requests, max_threads=10)
        tiles.append(data)
    return tiles


def read_json_and_break_into_bbox(geo_json_file, distance_of_image=(2560 * 8, 2560 * 8)):
    geo_json = read_data(geo_json_file)
    aoi = shape(geo_json["features"][0]["geometry"])

    utm_zone_splitter = UtmZoneSplitter([aoi], CRS.WGS84, distance_of_image)
    return utm_zone_splitter


def get_date_slots(no_days_back=90, n_chunks=1):
    start = datetime.now() - timedelta(days=no_days_back)
    end = datetime.now()
    tdelta = (end - start) / n_chunks
    edges = [(start + i * tdelta).date().isoformat() for i in range(n_chunks)]
    slots = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]
    slots.append((edges[-1], datetime.now().date().isoformat()))
    return slots


def get_sort_band(img_arr, axs=2):
    '''
    numpy  sorting
    '''

    sorted_img = np.sort(img_arr, axis=axs)
    return sorted_img


def generate_cld_less(sorted_arr, min_limit=0, max_limit=1):
    avg_arr = np.mean(sorted_arr[:, :, min_limit:max_limit, :, :], axis=2)
    # print(avg_arr.shape)
    return avg_arr


def remove_clds(image_stack):
    image_stack = get_sort_band(image_stack)
    image_stack = generate_cld_less(image_stack)
    return image_stack


class ForestStatsService:
    @staticmethod
    def get_images_district(district, no_of):
        day_slots = get_date_slots()
        input_file = f"{settings.BASE_DIR}/forest_stats/static/{district}.json"
        bbox_splitter = read_json_and_break_into_bbox(input_file)

        bbox_list = bbox_splitter.get_bbox_list()[:no_of]
        info_list = bbox_splitter.get_info_list()[:no_of]

        cld_less_images = get_satellite_images(bbox_list, info_list, day_slots)

        images = []
        for i in range(no_of):
            img = np.uint8(np.clip(np.array(cld_less_images[i][0]) * 5 / 255, 0, 255))
            img = Image.fromarray(img)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(2)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr = base64.b64encode(img_byte_arr.getvalue())
            images.append(img_byte_arr)
        return images

    @staticmethod
    def get_stats_district(district):
        result_stats = {
            "district": district,
        }
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
