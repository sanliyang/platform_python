# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name attribution_lookups_phone.py
@create->time 2023/3/14-10:03
@desc->
++++++++++++++++++++++++++++++++++++++ """
from phone import Phone

from base.c_json import CJson


class AttributionLookupsPhone:

    def __init__(self, phone):
        self.phone = phone
        self.phone_tools = Phone()
        self.phone_msg = None
        self.cj = CJson()

    def get_phone_json_msg(self):
        self.phone_msg = self.phone_tools.find(self.phone)
        self.cj.load(self.phone_msg)
        return self.phone_msg

    def get_phone_province(self):
        self.get_phone_json_msg()
        return None if self.phone_msg is None else self.cj.json_path_one("province")

    def get_phone_city(self):
        self.get_phone_json_msg()
        return self.cj.json_path_one("city") if self.phone_msg is not None else None

    def get_phone_zip_code(self):
        self.get_phone_json_msg()
        return None if self.phone_msg is None else self.cj.json_path_one("zip_code")

    def get_phone_area_code(self):
        self.get_phone_json_msg()
        return None if self.phone_msg is None else self.cj.json_path_one("area_code")

    def get_phone_type(self):
        self.get_phone_json_msg()
        return None if self.phone_msg is None else self.cj.json_path_one("phone_type")


if __name__ == '__main__':
    gpl = AttributionLookupsPhone("xxxxxxxx")
    phone_location = gpl.get_phone_json_msg()
    print(phone_location)

    print(gpl.get_phone_province())
    print(gpl.get_phone_city())
    print(gpl.get_phone_zip_code())
    print(gpl.get_phone_area_code())
    print(gpl.get_phone_type())

