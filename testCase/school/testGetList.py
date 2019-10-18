import unittest
import paramunittest
import readConfig as readConfig
from common1 import Log
from common1 import common
from common1 import configHttp as ConfigHttp
from common1 import businessCommon


getList = common.get_xls('getList.xls','getlist')
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}

@paramunittest.parametrized(*getList)
class GetList(unittest.TestCase):
    def setParameters(self, case_name, method, parameter, pageNum, pageSize, code, msg):
        '''

        :param case_name:
        :param method:
        :param parameter:
        :param pageNum:
        :param pageSize:
        :param code:
        :param msg:
        :return:
        '''

        self.case_name = str(case_name)
        self.method = str(method)
        self.parameter = str(parameter)
        if pageNum == '':
            self.pageNum = str(pageNum)
        else:
            self.pageNum = int(pageNum)
        if pageSize == '':
            self.pageSize = str(pageSize)
        else:
            self.pageSize = int(pageSize)
        self.code = int(code)
        self.msg = str(msg)

    def description(self):
        """
                test report description
                :return:
                """
        return  self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        self.cookie = localReadConfig.get_headers('cookie')

    def testGetList(self):
        """
        set url
        :return:
        """
        self.url = self.parameter
        print(self.url)
        configHttp.set_url(self.url)

        #set header
        cookie = str(self.cookie)
        header = {"Cookie": cookie}
        configHttp.set_headers(header)

        #判断页数是否为空，为空则data为空
        #区别最后一个接口，不带参数
        if self.pageNum == '':
            data = {}
            configHttp.set_data(data)
        else:
            data = {"pageNum": self.pageNum, "pageSize":self.pageSize}
            configHttp.set_data(data)

        #test interface
        self.return_json = configHttp.post()

        #判断cookie是否失效
        if self.return_json.json()['code'] == 4:
            businessCommon.login()
            # 重新设置cookie
            self.newcookie = localReadConfig.get_headers('cookie')
            newcookie = str(self.newcookie)
            header = {"Cookie": newcookie}
            configHttp.set_headers(header)
            # 重新请求
            self.return_json = configHttp.post()

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

        else:
            self.log.build_case_line(self.case_name, self.code, 'the code doesn\'t exist')


if __name__ == '__main__':
    GetList(unittest.TestCase)