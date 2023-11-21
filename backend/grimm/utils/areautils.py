import requests

from config import GrimmConfig
from grimm import logger


def address_to_coordinate(address):
    """
    Get location latitude and location longitude by tencent location services API
    Doc: https://lbs.qq.com/service/webService/webServiceGuide/webServiceQuota
         https://lbs.qq.com/service/webService/webServiceGuide/webServiceGeocoder
    API response: status = 0 means success
                  status != 0 means failed (eg: 347 no results)
    :param address: type str, a detail address would be better, like '上海市浦东新区世纪公园'
    :return: latitude - 纬度， longitude - 经度
    """
    logger.info('Get latitude/longitude by address.')
    developer_url = GrimmConfig.TENCENT_LOCATION_SERVICE_URL
    params = {
        'address': address,
        'key': GrimmConfig.TENCENT_LOCATION_SERVICE_KEY
    }
    response = requests.get(url=developer_url, params=params)
    res = response.json()
    if res['status'] == 0:
        return True, {'lng': res['result']['location']["lng"], 'lat': res['result']['location']["lat"]}
    logger.info('Get address failed. response is %s' % res)
    return False, 'Failed'


def coordinate_to_address(lat_lng):
    """
    Get location name by location latitude and location longitude
    Doc: https://lbs.qq.com/service/webService/webServiceGuide/webServiceQuota
         https://lbs.qq.com/service/webService/webServiceGuide/webServiceGcoder
    API response: status = 0 means success
                  status != 0 means failed (eg: 347 no results)
    :param lat_lng: type str, like '39.984154,116.307490'
    :return: location name, like '北京市海淀区北四环西路66号'
    """
    logger.info('Get address by latitude/longitude.')
    developer_url = GrimmConfig.TENCENT_LOCATION_SERVICE_URL
    params = {
        'location': lat_lng,
        'get_poi': 1,
        'key': GrimmConfig.TENCENT_LOCATION_SERVICE_KEY
    }
    response = requests.get(url=developer_url, params=params)
    res = response.json()
    if res['status'] == 0:
        return True, res['result']['address']
    logger.info('Get address failed, response is %s' % res)
    return False, 'Failed'
