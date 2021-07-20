import json
import socket
from datetime import datetime

import requests

from config import GrimmConfig
from grimm import logger


def send_error_to_spark(url, method, traceback, err_msg, email=None):
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    hi = "Hi <@personEmail:" + email + ">  \n" if email else ''
    job_msg = "  \nRequest url is [ {} ]".format(url) if url else ''
    method_msg = "  \nRequest method is [ {} ]".format(method) if method else ''
    exec_msg = "  \nExecute time is [ {} ]".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    hostname_msg = "  \nExecute hostname is [ {} ]".format(hostname)
    ip_msg = "  \nExecute ip address is [ {} ]".format(ip)
    error_msg = "  \nExecute error message is [ {} ]".format(err_msg)
    traceback_msg = "  \n  \n{}  \n".format(traceback)
    msg = job_msg + method_msg + exec_msg + hostname_msg + ip_msg + error_msg + traceback_msg
    send_text_to_spark_room(hi + "```{}```".format(msg), GrimmConfig.GRIMM_EXCEPTION_MSG_ROOM)


def send_text_to_spark_room(markdown, room_id):
    headers = {'Authorization': "Bearer " + GrimmConfig.GRIMM_BOT_TOKEN,
               'Content-Type': 'application/json; charset=utf-8'}
    data = {'roomId': room_id, 'markdown': markdown}
    logger.info("Request url: " + str(GrimmConfig.GRIMM_BOT_MESSAGE_URL))
    response = requests.post(GrimmConfig.GRIMM_BOT_MESSAGE_URL, data=json.dumps(data),
                             headers=headers, timeout=10.0)
    status_code = response.status_code
    content = response.content
    if status_code != 200:
        logger.info('Error code: ' + str(response.status_code))
        logger.info('Error response content: ' + str(content))
    return status_code, content
