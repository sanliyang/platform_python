# -*- coding: utf-8 -*-
# @Time : 2022/5/16 22:59
# @Author : sanliy
# @File : c_get_config
# @software: PyCharm

import configparser

from base.c_project import CProject
from base.c_resource import CResource


class CConfig(CResource):

    def __init__(self, config_path):
        self.config_obj = configparser.RawConfigParser()
        self.config_obj.read(config_path)

    def get_all_sections(self):
        return self.config_obj.sections()

    def get_options(self, section):
        return self.config_obj.options(section)

    def get_items(self, section):
        return self.config_obj.items(section)

    def get_value(self, section, option):
        return self.config_obj.get(section, option)


if __name__ == '__main__':
    cg = CConfig(CProject.config_path())
    print(cg.get_all_sections())
    print(cg.get_options('email'))
    print(cg.get_value('email', 'auth_pass'))