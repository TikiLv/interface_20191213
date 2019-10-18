import unittest
import paramunittest
import time
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
    def setParameters(self,case_name, method, name, schoolNumber, startDate, gradeId, classId, address, code, msg):
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
            return case_name

        def setUp(self):
            '''

            :return:
            '''
            self.log = Log.MyLog.get_log()
            self.logger = self.log.get_logger()
            self.cookie = localReadConfig.set_headers('cookie')

        def getStudentId(self):
            '''
            获取学生ID
            :param self:
            :return:
            '''
            self.get_url = common.get_url_from_xml('getStudentId')
            configHttp.set_url(self.get_url)

            #设置请求头
            cookie = str(self.cookie)
            header = {'cookie':cookie}
            configHttp.set_headers(header)

            #测试接口
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
            self.message = self.return_json.json()


