# -*- coding: utf-8 -*-
import sys

sys.path.append(r'C:\CgTeamWork_v7\bin\base')

import cgtw2


class CGTData:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CGTData, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.project_list = []
            self.user_info = []

            self.fetch_all()
            self.initialized = True

    def fetch_all(self):
        self.fetch_project_list()
        self.fetch_user_info()

    def fetch_project_list(self):
        """获取所有启用的项目"""
        try:
            field_sign_list = ['project.entity', 'project.full_name', 'project.id', 'project.database']
            filter_list = [['project.status', '=', 'Active']]
            id_list = cgtw2.tw().project.get_id(filter_list, limit="5000", start_num="")
            self.project_list = cgtw2.tw().project.get(id_list, field_sign_list, limit="5000", order_sign_list=[])
        except Exception as e:
            print(e)
            return []

    def fetch_user_info(self):
        """获取当前用户信息"""
        try:
            _id = cgtw2.tw().login.account_id()
            _field_sign_list = cgtw2.tw().account.fields()
            self.user_info = cgtw2.tw().account.get([_id], _field_sign_list)
        except Exception as e:
            print(e)
            return []

    def get_project_list(self):
        return self.project_list

    def get_user_info(self):
        return self.user_info


if __name__ == '__main__':
    cgt = CGTData()
    print(cgt.user_info)

