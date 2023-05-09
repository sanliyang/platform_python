# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name loganysystem
@editor->name Sanliy
@file->name op_mysql.py
@create->time 2023/3/8-21:13
@desc->
++++++++++++++++++++++++++++++++++++++ """
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from c_resource import CResource

engine = create_engine("mysql+pymysql://{0}:{1}@{2}/{3}".format(
            "root",
            "root",
            "localhost",
            "python_platform"
        ), poolclass=QueuePool)


class CMysql:

    def __init__(self):
        self.cursor = None
        session_maker = sessionmaker(bind=engine)
        self.session = session_maker()

    def fetchall(self, sql, *args, **kwargs):
        self.cursor = self.session.execute(text(sql), *args, **kwargs)
        self.session.commit()
        return self.cursor.fetchall()

    def fetchone(self, sql, *args, **kwargs):
        return self.fetchall(text(sql), *args, **kwargs)[0]

    def execute(self, sql, *args, **kwargs):
        self.cursor = self.session.execute(text(sql), *args, **kwargs)
        self.session.commit()

    def close(self):
        self.cursor.close()
        self.session.close()


if __name__ == '__main__':
    om = CMysql()
    a = om.fetchall(
        '''
        select node_config from python_platform.do_nodes where node_id =:node_id
        ''', {
            "node_id": '123'
        }
    )
    print(a[0][0])
    om.close()
