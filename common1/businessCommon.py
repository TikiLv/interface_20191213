from common1 import common
from common1 import configHttp
import readConfig as readConfig
import requests

localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localLogin_xls = common.get_xls("userCase.xls", "login")
localAddAddress_xls = common.get_xls("userCase.xls", "addAddress")

# login
def login():
    """
    login
    :return: token
    """
    # set url
    # url = common.get_url_from_xml('login')
    # localConfigHttp.set_url(url)
    url = localConfigHttp.set_url('school/user/login')


    # set header
    # token = localReadConfig.get_headers("token_v")
    # header = {"token": token}
    # localConfigHttp.set_headers(header)

    # set param
    data = {"account": localLogin_xls[0][3],
            "password": localLogin_xls[0][4]}
    localConfigHttp.set_data(data)

    # login,构造session并将session存储到config.ini文件中
    session = requests.Session()
    response = session.post(url, data)
    # print(session.cookies)
    sessionId =  session.cookies.get_dict()['JSESSIONID']
    # print(sessionId)
    cookie = 'JSESSIONID=' + sessionId
    # print(cookie)
    localReadConfig.set_headers("cookie", cookie)
    return cookie


    # response = localConfigHttp.post().json()
    # token = common.get_value_from_return_json(response, "member", "token")
    # return token


# logout
def logout():
    """
    logout
    :param token: login token
    :return:
    """
    # set url
    url = localConfigHttp.set_url('account/setting/loginOut')
    localConfigHttp.set_url(url)

    # set header
    # header = {'token': token}
    # localConfigHttp.set_headers(header)

    # logout
    localConfigHttp.get()

if __name__ == "__main__":
    login()
    logout()

