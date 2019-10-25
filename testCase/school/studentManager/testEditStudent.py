import unittest
import paramunittest
import readConfig as readConfig
from common1 import Log
from common1 import common
from common1 import configHttp as ConfigHttp
from common1 import businessCommon

editStudent = common.get_xls("userCase.xls","editStudent")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info ={}

@paramunittest.parametrized(*editStudent)
class editStudent(unittest.TestCase):
    def setParameters(self, case_name, method, name, schoolNumber, startDate, gradeId, classId, address, code, msg):
        '''

        :param case_name:
        :param method:
        :param name:
        :param schoolNumber:
        :param startDate:
        :param gradeId:
        :param classId:
        :param address:
        :param code:
        :param msg:
        :return:
        '''

        self.case_name = str(case_name)
        self.method = str(method)
        self.name = str(name)
        self.schoolNumber = str(schoolNumber)
        self.startDate = str(startDate)
        self.gradeId = int(gradeId)
        self.classId = int(classId)
        self.address = str(address)
        self.code = int(code)
        self.msg = str(msg)

    def description(self):
        '''

        :param self:
        :return:
        '''
        return self.case_name

    def setUp(self):
        '''

        :return:
        '''
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        self.cookie = localReadConfig.get_headers('cookie')


    def getStudentId(self):
        '''
        获取学生ID
        :param self:
        :return:z
        '''
        self.get_url = common.get_url_from_xml('getStudentId')
        configHttp.set_url(self.get_url)

        # 设置请求头
        cookie = str(self.cookie)
        header = {'cookie': cookie}
        configHttp.set_headers(header)

        # set data
        data = {"pageNum": 1, "pageSize": 10}
        configHttp.set_data(data)

        # 测试接口
        self.returnMessage_json = configHttp.post()
        # 登录超时则重新调用登录
        if self.returnMessage_json.json()['code'] == 4:
            businessCommon.login()
            # 重新设置cookie
            self.newcookie = localReadConfig.get_headers('cookie')
            # set headers
            newcookie = str(self.newcookie)
            header = {"Cookie": newcookie}
            configHttp.set_headers(header)
            # 重新请求
            self.returnMessage_json = configHttp.post()

        self.info = self.returnMessage_json.json()

        self.studentMessage = self.info['data']['list'][0]
        # 判断列表是否有学生
        try:
            self.studentId = self.studentMessage['id']
            self.schoolCode = self.studentMessage['cardCode']
        except IndexError:
            self.log.build_case_line(self.case_name, self.code, '学生列表为空')

    def getGrade(self):
        """
        获取班级年级ID
        :return:
        """
        self.get_url = common.get_url_from_xml("getGrade")
        configHttp.set_url(self.get_url)

        #设置请求头
        cookie = str(self.cookie)
        header = {"cookie":cookie}
        configHttp.set_headers(header)

        #发送请求
        self.return_json = configHttp.post()
        # 登录超时则重新调用登录
        if self.return_json.json()['code'] == 4:
            businessCommon.login()
            # 重新设置cookie
            self.newcookie = localReadConfig.get_headers('cookie')
            # set headers
            newcookie = str(self.newcookie)
            header = {"Cookie": newcookie}
            configHttp.set_headers(header)
            # 重新请求
            self.return_json = configHttp.post()



    def testEditStudent(self):
        """
        编辑学生
        :param self:
        :return:
        """
        self.getStudentId()
        self.get_url = common.get_url_from_xml('editStudent')
        configHttp.set_url(self.get_url)

        # 设置请求头
        cookie = str(self.cookie)
        header = {'cookie': cookie}
        configHttp.set_headers(header)

        # set data
        data = {"pageNum": 1, "pageSize": 10}
        configHttp.set_data(data)

        # 测试接口
        self.return_json = configHttp.post()
        # 登录超时则重新调用登录
        if self.return_json.json()['code'] == 4:
            businessCommon.login()
            # 重新设置cookie
            self.newcookie = localReadConfig.get_headers('cookie')
            # set headers
            newcookie = str(self.newcookie)
            header = {"Cookie": newcookie}
            configHttp.set_headers(header)
            # 重新请求
            self.return_json = configHttp.post()

        self.info = self.return_json.json()

    def tearDown(self):
        """

        :param self:
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
        print(self.info['msg'])

        if self.info['code'] == 0:
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)

        elif self.info['code'] == 3:
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)

        else:
            self.log.build_case_line(self.case_name, self.code, 'the code doesn\'t exist')


if __name__ == '__main__':
    unittest.main()