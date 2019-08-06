import unittest
import paramunittest
import readConfig
from common1 import Log
from common1 import common
from common1 import businessCommon
from common1 import configHttp as ConfigHttp

deleteUserManager = common.get_xls("userCase.xls", "deleteUserManager")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()

@paramunittest.parametrized(*deleteUserManager)
class DeleteUserManager(unittest.TestCase):
    def setParameters(self, case_name, method, code, msg):
        '''
        :param case_name:
        :param method:
        :param code:
        :param msg:
        :return:
        '''
        self.case_name = str(case_name)
        self.method = str(method)
        self.code = int(code)
        self.msg = str(msg)
        self.pageNum = 1
        self.pageSize = 10

    def setUp(self):
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        self.cookie = localReadConfig.get_headers('cookie')

    def testDeleteUser(self):
        """
        删除用户
        :return:
        """
        #获取用户ID
        self.GetAccountId()

        #set url
        self.url = common.get_url_from_xml("testDeleteUser")
        configHttp.set_url(self.url)
        print(self.url)

        #set header
        cookie = str(self.cookie)
        header = {"cookie": cookie}
        configHttp.set_headers(header)

        #set data
        data = {"id":self.userId}
        configHttp.set_data(data)

        # test interface
        self.return_json = configHttp.post()

        #check result
        self.checkResult()

    def tearDown(self):
        """

                :return:
                """
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])
        print("测试结束，输出log完结\n\n")

    def GetAccountId(self):
        '''
        获取用户
        :return:
        '''

        get_url = common.get_url_from_xml("getAccountManager")
        configHttp.set_url(get_url)

        #设置请求头
        cookie = str(self.cookie)
        header = {"Cookie": cookie}
        configHttp.set_headers(header)

        #设置data
        data = {"pageNum": self.pageNum, "pageSize":self.pageSize}
        configHttp.set_data(data)

        #test interface
        self.return_json = configHttp.post()
        # 登录超时判断
        if self.return_json.json() == 4:
            businessCommon.login()
            self.return_json = configHttp.post()

        self.message = self.return_json.json()

        #获取用户id
        try:
            self.userId = str(self.message['data']['list'][0]['id'])
            return self.userId
        except IndexError:
            self.log.build_case_line(self.case_name, self.code, '用户不存在')

    def checkResult(self):
        """
        检查返回值
        :return:
        """
        self.info = self.return_json.json()
        common.show_return_msg(self.return_json)

        if self.info['code'] == 0:
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)

        elif self.info['code'] == 4:
            self.log.build_case_line(self.case_name, self.code, 'login timeout')

        else:
            self.log.build_case_line(self.case_name, self.code, 'the code doesn\'t exist')


if __name__ == "__main__":
    DeleteUserManager(unittest.TestCase)
