import unittest
import paramunittest
import readConfig as readConfig
from common1 import Log
from common1 import common
from common1 import configHttp as ConfigHttp
from common1 import businessCommon

getGrade = common.get_xls("userCase.xls","getGrade")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()

@paramunittest.parametrized(*getGrade)
class getGrade(unittest.TestCase):
    def setParameters(self, case_name, code, msg):
        """

        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.code = int(code)
        self.msg = str(msg)
        self.gradeId = []

    def description(self):
        '''

        :param self:
        :return:
        '''
        return self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        self.cookie = localReadConfig.get_headers('cookie')

    def testGetGrade(self):
        """
        获取班级ID并写入excel
        :return:
        """
        self.get_url = common.get_url_from_xml('getGrade')
        configHttp.set_url(self.get_url)

        #设置请求头
        cookie = str(self.cookie)
        header = {'cookies': cookie}
        configHttp.set_headers(header)

        #set data
        data ={}
        configHttp.set_data(data)

        #test interface
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

        #判断请求是否成功
        if self.info['code'] == 0:
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            #判断返回的gradeId是否为空，不为空则写入excel
            self.allGrade = self.info['data']
            if len(self.allGrade) != 0:
                for i in range(len(self.allGrade)):
                    self.gradeId.append(self.allGrade[i]['id'])
                    # print(self.gradeId)
                common.write_xls('saveData.xls', 'grade',self.gradeId, 'gradeId')
            else:
                self.log.build_case_line(self.case_name, self.code, 'the Grade is null')
        else:
            self.log.build_case_line(self.case_name, self.code, 'the code doesn\'t exist')

if __name__ == '__main__':
    getGrade()