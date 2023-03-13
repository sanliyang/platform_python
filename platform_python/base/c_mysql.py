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

engine = create_engine("mysql+pymysql://{0}:{1}@{2}/{3}".format(
            "root",
            "root",
            "127.0.0.1",
            "log"
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
    om.execute(
        '''
        insert into system_log(
        log_level, log_file_name, log_file_no, log_msg, log_type
        ) values (
        :key, :log_file_name, :log_file_no, :log_msg, :log_type
        )
        ''', {
            "key": 'warning',
            "log_file_name": 'name',
            "log_file_no": 34,
            "log_msg": 'msg',
            "log_type": "type"
        }
    )
    om.close()
