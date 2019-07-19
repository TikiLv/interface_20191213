import unittest
import paramunittest
import readConfig as readConfig
from common1 import Log as Log
from common1 import common
from common1 import configHttp as ConfigHttp
from common1 import businessCommon

addGroupManager = common.get_xls("userCase.xls", "deleteGroupManager")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()


@paramunittest.parametrized(*addGroupManager)
class DeleteGroupManager(unittest.TestCase):
    def setParameters(self, case_name, method, code, msg):
        """

        :param case_name:
        :param method:
        :param id:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.code = int(code)
        self.msg = str(msg)

    def description(self):
        """
                test report description
                :return:
                """
        return self.case_name

    def setUp(self):
        """

                :return:
                """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        self.cookie = businessCommon.login()
        # print(self.cookie)

    def GetGroupManagerId(self):
        """
        获取用户组ID
        :return:
        """
        self.get_url = common.get_url_from_xml('testGetGroupManager')
        configHttp.set_url(self.get_url)
        # print(self.get_url)

        # set headers
        cookie = str(self.cookie)
        header = {"Cookie": cookie}
        configHttp.set_headers(header)

        # test interface
        self.return_json = configHttp.post()
        self.info = self.return_json.json()
        self.message = self.return_json.json()
        try:
            self.newid = self.message['data']['list'][0]['id']
            return self.newid
        except IndexError:
            self.log.build_case_line(self.case_name, self.code,'用户组不存在')
        # print(self.newid)

        # validation
        # common.show_return_msg(self.return_json)



    def testDeleteGroupManager(self):
        """
        删除用户组
        :return:
        """
        self.GetGroupManagerId()

        # set url
        self.url = common.get_url_from_xml('testDeleteGroupManager')
        configHttp.set_url(self.url)
        print(self.url)

        # set headers
        cookie = str(self.cookie)
        header = {"Cookie": cookie}
        configHttp.set_headers(header)

        # set data
        data = {"id": self.newid}
        print(data)
        configHttp.set_data(data)
        print('第三步：设置发送请求的参数')

        # test interface
        self.return_json = configHttp.post()
        method = str(self.return_json.request)[int(str(self.return_json.request).find('[')) + 1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法：" + method)

        # check result
        self.checkResult()

    def tearDown(self):
        """

        :return:
        """
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])
        print("测试结束，输出log完结\n\n")

    def checkResult(self):
        """
        check result
        :return:
        """
        self.info = self.return_json.json()
        common.show_return_msg(self.return_json)

        if self.info['code'] == 0:
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)

        elif self.info['code'] == 1:
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)

        elif self.info['code'] == 4:
            self.log.build_case_line(self.case_name, self.code, 'login timeout')

        else:
            self.log.build_case_line(self.case_name, self.code, 'the code doesn\'t exist')


if __name__ == '__main__':
    # suit = unittest.TestSuite()
    # suit.addTest(DeleteGroupManager("test_01_GetGroupManagerId"))
    # suit.addTest(DeleteGroupManager("test_2_DeleteGroupManager"))
    DeleteGroupManager(unittest.TestCase)
