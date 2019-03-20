import unittest
import paramunittest
import readConfig as readConfig
from common1 import Log as Log
from common1 import common
from common1 import configHttp as ConfigHttp

addGroupManager = common.get_xls("userCase.xlsx","addGroupManager")
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
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.id = int(id)
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

    def testAddGroupManager(self):
        '''
        set url
        :return:
        '''
        self.url = common.get_url_from_xml('testAddGroupManager')
        configHttp.set_url(self.url)
        print(self.url)

        #set data
        data = {"id": self.id, "name": self.name, "remarks": self.remarks, "authoritys": self.authoritys}
        configHttp.set_data(data)
        print('第三步：设置发送请求的参数')

        #test interface
        self.return_json = configHttp.post()
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

        if self.result == '0':
            self.assertEqual(self.info['code'],self.code)
            self.assertEqual(self.info['msg'],self.msg)

        elif self.result == '3':
            self.assertEqual(self.info['code'],self.code)
            self.assertEqual(self.info['msg'],self.msg)

        else :
            self.log.build_case_line(self.case_name, self.result, 'the code doesn\'t exist')

if __name__ == '__main__':
    AddGroupManager(unittest.TestCase)