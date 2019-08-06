# -*- coding: utf-8 -*-

import unittest
import paramunittest
import readConfig
from common1 import Log
from common1 import common
from common1 import configHttp as ConfigHttp
from common1 import businessCommon

addGroupManager = common.get_xls("userCase.xls", "editGroupManager")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()

@paramunittest.parametrized(*addGroupManager)
class EditGroupManager(unittest.TestCase):
    def setParameters(self,case_name, name, remarks, authoritys, code, msg):
        '''

        :param case_name:
        :param name:
        :param remarks:
        :param authoritys:
        :param code:
        :param msg:
        :return:
        '''
        self.case_name = str(case_name)
        self.name = str(name)
        self.remarks = str(remarks)
        self.authoritys = str(authoritys)
        self.code = int(code)
        self.msg = msg


    def setUp(self):
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        self.cookie = localReadConfig.get_headers('cookie')

    def GetGroupManagerContent(self):
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
        #登录超时则重新调用登录
        if self.return_json.json()['code'] == 4:
            businessCommon.login()
            self.return_json = configHttp.post()

        self.info = self.return_json.json()
        self.message = self.return_json.json()
        # print(self.message)
        try:
            self.newid = self.message['data']['list'][0]['id']
            return self.newid
        except IndexError:
            self.log.build_case_line(self.case_name, self.code,'用户组不存在')
        # print(self.newid)

    def testEditGroupManager(self):
        """
        修改用户组
        :return:
        """

        #获取用户组id
        self.GetGroupManagerContent()

        #设置url
        self.url = common.get_url_from_xml('testAddGroupManager')
        configHttp.set_url(self.url)

        #设置请求头
        cookie = str(self.cookie)
        header = {"cookie":cookie}
        configHttp.set_headers(header)

        #设置body
        data = {"id":self.newid , "authoritys":self.authoritys ,"name":self.name ,"remarks":self.remarks}
        configHttp.set_data(data)
        print('第三步：设置发送请求的参数')

        #测试接口
        self.return_json = configHttp.post()
        self.url = self.return_json.url
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法：" + method)

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
        print(type(self.code))

        if self.info['code'] == 0:
            self.assertEqual(self.info['code'],self.code)
            self.assertEqual(self.info['msg'],self.msg)

        elif self.info['code'] == 3:
            self.assertEqual(self.info['code'],self.code)
            self.assertEqual(self.info['msg'],self.msg)

        else :
            self.log.build_case_line(self.case_name, self.code, 'the code doesn\'t exist')


if __name__ == '__main__':
    EditGroupManager(unittest.TestCase)
