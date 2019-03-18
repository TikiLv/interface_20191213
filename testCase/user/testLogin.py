import unittest
import paramunittest
import readConfig as readConfig
from common1 import Log as Log
from common1 import common
from common1 import configHttp as ConfigHttp

login_xls = common.get_xls("userCase.xlsx", "login")
print(login_xls)
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*login_xls)
class Login(unittest.TestCase):
    def setParameters(self, case_name, method, token, account, password, result, code, msg):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param email:
        :param password:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.account = str(account)
        self.password = str(password)
        self.result = str(result)
        self.code = int(code)
        self.msg = str(msg)
        self.return_json = None
        self.info = None

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+"测试开始前准备")

    def testLogin(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('login')
        configHttp.set_url(self.url)
        print("第一步：设置url  "+self.url)

        # get visitor token
        # if self.token == '0':
        #     token = localReadConfig.get_headers("token_v")
        # elif self.token == '1':
        #     token = None

        # set headers
        # header = {"token": str(token)}
        # configHttp.set_headers(header)
        # print("第二步：设置header(token等)")

        # set params
        data = {"account": self.account, "password": self.password}
        configHttp.set_data(data)
        print("第三步：设置发送请求的参数")

        # test interface
        self.return_json = configHttp.post()
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        # check result
        self.checkResult()
        print("第五步：检查结果")

    def tearDown(self):
        """

        :return:
        """
        # info = self.info
        # if info['code'] == 0:
        #     # get uer token
        #     token_u = common.get_value_from_return_json(info, 'member', 'token')
        #     # set user token to config file
        #     localReadConfig.set_headers("TOKEN_U", token_u)
        # else:
        #     pass
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])
        print("测试结束，输出log完结\n\n")

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # print(self.info)
        # show return message
        common.show_return_msg(self.return_json)

        if self.result == '0':
            # data = common.get_value_from_return_json(self.info, 'code', 'msg')
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)

        elif self.result == '1':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)

        elif self.result == '2':
            self.log.build_case_line(self.case_name, self.result,'the result doesn\'t exist')

if __name__ ==  "__main__":
    Login(unittest.TestCase)