import unittest
import paramunittest
import readConfig
from common1 import common
from common1 import configHttp as ConfigHttp
from common1 import Log
from common1 import businessCommon

editUserManager = common.get_xls('userCase.xls','editUserManager')
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()

@paramunittest.parametrized(*editUserManager)
class EditUserManager(unittest.TestCase):
    def setParameters(self, case_name, account, name, mobile, code, msg):
        '''

        :param account:
        :param name:
        :param mobile:
        :param code:
        :param msg:
        :return:
        '''
        self.case_name = str(case_name)
        self.account = str(account)
        self.name = str(name)
        self.mobile = str(mobile)
        self.code = int(code)
        self.msg = str(msg)
        self.pageNum = 1
        self.pageSize = 10

    def setUp(self):

        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        self.cookie = localReadConfig.get_headers('cookie')


    def testEditUserManager(self):
        '''
        编辑用户接口
        :return:
        '''
        #获取用户id
        self.GetAccountId()

        #获取用户组id
        self.GetGroup()
        self.newgroupIds = str(self.groupIds)+','+str(self.groupIds2)
        # print(self.newgroupIds)

        #设置url
        self.url = common.get_url_from_xml('testAddUser')
        configHttp.set_url(self.url)

        #设置请求头
        cookie = str(self.cookie)
        header = {"cookie":cookie}
        configHttp.set_headers(header)

        #设置data
        if self.mobile == '':
            data = {"account":self.account, "name":self.name, "id":self.userId, "groupIds":self.newgroupIds}
        else:
            data = {"account":self.account, "name":self.name, "id":self.userId, "groupIds":self.newgroupIds, "mobile":self.mobile}
        configHttp.set_data(data)
        print(data)

        #test interface
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
        self.message = self.return_json.json()


        #获取groupIds
        try:
            self.groupIds = self.message['data'][0]['id']
            self.groupIds2 = self.message['data'][1]['id']
            return self.groupIds,self.groupIds2
        except IndexError:
            self.log.build_case_line(self.case_name, self.code, '用户组不存在')

    def checkResult(self):
        """
        检查返回值
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
    EditUserManager()



