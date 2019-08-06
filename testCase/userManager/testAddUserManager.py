import unittest
import paramunittest
import readConfig as readConfig
from common1 import Log as Log
from common1 import common
from common1 import configHttp as ConfigHttp
from common1 import businessCommon

addUserManager = common.get_xls("userCase.xls","addUserManager")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}

@paramunittest.parametrized(*addUserManager)
class AddUserManager(unittest.TestCase):
    def setParameters(self, case_name, account, name, password, mobile, code, msg):
        """

        :param case_name:
        :param account:
        :param name:
        :param password:
        :param mobile:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.account = str(account)
        self.name = str(name)
        self.password = str(password)
        self.mobile = str(mobile)
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


    def testAddUser(self):
        '''
        set url
        :return:
        '''
        #调用获取列表函数获取groupId
        self.GetGroup()

        self.url = common.get_url_from_xml('testAddUser')
        configHttp.set_url(self.url)
        print(self.url)

        #set headers
        cookie = str(self.cookie)
        header = {"Cookie":cookie}
        configHttp.set_headers(header)


        #set data
        if self.mobile == '':
            data = { "account": self.account, "name": self.name, "password": self.password, "groupIds": self.groupIds }
        else:
            data = { "account": self.account, "name": self.name, "password": self.password, "groupIds": self.groupIds , "mobile":self.mobile }
        configHttp.set_data(data)
        print('第三步：设置发送请求的参数'+str(data))

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

    def GetGroup(self):
        '''
        获取用户组列表
        :return:
        '''
        get_url = common.get_url_from_xml('testGetAllGroup')
        configHttp.set_url(get_url)

        #设置请求头
        cookie = str(self.cookie)
        header = {"Cookie": cookie}
        configHttp.set_headers(header)

        # test interface
        self.return_json = configHttp.post()
        #登录超时判断
        if self.return_json.json() == 4:
            businessCommon.login()
            self.return_json = configHttp.post()

        self.message = self.return_json.json()


        #获取groupIds
        try:
            self.groupIds = self.message['data'][0]['id']
            return self.groupIds
        except IndexError:
            self.log.build_case_line(self.case_name, self.code, '用户组不存在')

    def checkResult(self):
        """
        check result
        :return:
        """
        self.info = self.return_json.json()
        print(self.info)
        common.show_return_msg(self.return_json)

        if self.info['code'] == 0:
            self.assertEqual(self.info['code'],self.code)
            self.assertEqual(self.info['msg'],self.msg)

        elif self.info['code'] == 1:
            self.assertEqual(self.info['code'],self.code)
            self.assertEqual(self.info['msg'],self.msg)

        else:
            self.assertEqual(self.info['code'],[0,1])


if __name__ == '__main__':
    AddUserManager(unittest.TestCase)