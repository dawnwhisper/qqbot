import requests

def tiangou_comment():
    data = requests.get(f'https://cloud.qqshabi.cn/api/tiangou/api.php').text
    return "\n" + data