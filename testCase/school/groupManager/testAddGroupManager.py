import unittest
import paramunittest
import readConfig as readConfig
from common1 import Log as Log
from common1 import common
from common1 import configHttp as ConfigHttp
from common1 import businessCommon
import time

addGroupManager = common.get_xls("userCase.xls","addGroupManager")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}

@paramunittest.parametrized(*addGroupManager)
class AddGroupManager(unittest.TestCase):
    def setParameters(self, case_name, method, token, id, name, remarks, authoritys, code, msg):
        """
                set params
                :param case_name:
                :param method:
                :param token:
                :param id:
                :param name:
                :param remarks:
                :param authoritys:
                :param code:
                :param msg:
                :return:
                """
        # print(type(id))
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        if id == '':
            self.newid = id
        else:
            self.newid = int(id)
        self.name = str(name)
        self.remarks = str(remarks)
        self.authoritys = str(authoritys)
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
        # self.cookie = 'JSESSIONID=111373CF525F2CC5FAF1D64A4348837C'

    def testAddGroupManager(self):
        '''
        set url
        :return:
        '''
        self.url = common.get_url_from_xml('testAddGroupManager')
        configHttp.set_url(self.url)
        print(self.url)

        #set headers
        cookie = str(self.cookie)
        header = {"Cookie":cookie}
        # print(header)
        configHttp.set_headers(header)


        #set data
        data = {"id": self.newid, "name": self.name, "remarks": self.remarks, "authoritys": self.authoritys}
        configHttp.set_data(data)
        print('第三步：设置发送请求的参数')

        #test interface
        self.return_json = configHttp.post()
        #判断是否登录超时
        if self.return_json.json()['code'] == 4:
            #重新设置cookie
            businessCommon.login()
            #重新获取cookie
            # time.sleep(2)
            self.newcookie = localReadConfig.get_headers('cookie')
            # set headers
            newcookie = str(self.newcookie)
            header = {"Cookie": newcookie}
            configHttp.set_headers(header)
            #重新请求
            self.return_json = configHttp.post()


        self.url = self.return_json.url
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法：" + method)

        #check result
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
            self.assertEqual(self.info['code'],self.code)
            self.assertEqual(self.info['msg'],self.msg)

        elif self.info['code'] == 3:
            self.assertEqual(self.info['code'],self.code)
            self.assertEqual(self.info['msg'],self.msg)

        else :
            self.log.build_case_line(self.case_name, self.code, 'the code doesn\'t exist')

if __name__ == '__main__':
    AddGroupManager(unittest.TestCase)