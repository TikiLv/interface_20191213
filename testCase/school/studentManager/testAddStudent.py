import unittest

import datetime as datetime
import paramunittest
import readConfig as readConfig
from common1 import Log
from common1 import common
from common1 import configHttp as ConfigHttp
from common1 import businessCommon
from datetime import datetime
import time

addStudentManager = common.get_xls("userCase.xls","addStudent")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}

@paramunittest.parametrized(*addStudentManager)
class AddStudent(unittest.TestCase):
    def setParameters(self, case_name, token, method, name, schoolCode, schoolNumber, startDate, gradeId, classId, address, code, message):
        """

        :param name:
        :param schoolCode:
        :param schoolNumber:
        :param startDate:
        :param gradeId:
        :param classId:
        :param address:
        :return:
        """
        self.case_name = str(case_name)
        self.token = str(token)
        self.method = str(method)
        self.name = str(name)
        self.schoolCode = str(schoolCode)
        self.schoolNumber = str(schoolNumber)
        self.startDate = time.strptime(startDate,'%Y')
        print(self.startDate)
        self.gradeId = str(gradeId)
        self.classId = str(classId)
        self.address = str(address)
        self.code = int(code)
        self.msg = str(message)


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
        self.cookie = businessCommon.login()

    def testAddStudent(self):
        """
        set url
        :return:
        """
        self.url = common.get_url_from_xml('testAddStudent')
        configHttp.set_url(self.url)

        #set headers
        cookie = str(self.cookie)
        header = {"Cookie":cookie}
        configHttp.set_headers(header)

        #set data
        data = {"name":self.name, "schoolCode":self.schoolCode, "schoolNumber":self.schoolNumber, "startDate":self.startDate, "gradeId":self.gradeId, "classId":self.classId, "address":self.address}
        configHttp.set_data(data)

        #test interface
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
        print(self.info['msg'])

        if self.info['code'] == 0:
            self.assertEqual(self.info['code'],self.code)
            self.assertEqual(self.info['msg'],self.msg)

        elif self.info['code'] == 3:
            self.assertEqual(self.info['code'],self.code)
            self.assertEqual(self.info['msg'],self.msg)

        else :
            self.log.build_case_line(self.case_name, self.code, 'the code doesn\'t exist')

if __name__ == '__main__':
    AddStudent(unittest.TestCase)
