# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name loganysystem
@editor->name Sanliy
@file->name logger.py
@create->time 2023/3/8-16:02
@desc->
++++++++++++++++++++++++++++++++++++++ """
import logging.handlers
import inspect
import traceback

from kafka import KafkaProducer
from kafka.errors import kafka_errors

from base.c_json import CJson
from base.c_file import CFile
from base.c_time import CTime
from base.c_resource import CResource


class CLogger(CResource):

    def __init__(self, switch_kafka=False):
        self.switch_kafka = switch_kafka
        self.file_name = None
        self.fileno = None
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(file_name)s - [line:%(line_no)d] - "
            "%(levelname)s - [%(funcName)s] - [日志信息]: %(message)s "
        )
        self.logger = logging.getLogger(self.LOG_NAME)
        self.handler_console = logging.StreamHandler()
        project_path = CFile.get_project_root_path()
        log_path = CFile.path_join(project_path, "logs/{0}.log".format(CTime.get_date()))
        if not CFile.path_is_exist(log_path):
            CFile.touch_file(log_path)
        self.handler_file = logging.FileHandler(filename=log_path, encoding=self.ENCODE_UTF8)
        if switch_kafka:
            self.producer = KafkaProducer(
                bootstrap_servers=['192.168.44.129:9092'],
                key_serializer=lambda k: CJson.dict_2_json(k).encode(),
                value_serializer=lambda v: CJson.dict_2_json(v).encode()
            )

    def __set_level(self):
        self.logger.setLevel(logging.DEBUG)

        self.handler_console.setLevel(logging.INFO)

        self.handler_file.setLevel(logging.INFO)

    def __set_format(self):
        self.handler_console.setFormatter(self.formatter)

        self.handler_file.setFormatter(self.formatter)

    def __add_handler(self):
        self.logger.addHandler(self.handler_console)
        self.logger.addHandler(self.handler_file)

    def __do_process(self, level, msg, *args, **kwargs):
        self.__set_level()
        self.__set_format()
        self.__add_handler()
        # print(inspect.stack())
        frame = inspect.stack()[-self.CONSTENT_ONE]
        file_name = frame[self.CONSTENT_ONE]
        file_no = frame[self.CONSTENT_TWO]
        kafka_msg = {
            'file_name': file_name,
            'file_no': file_no,
            'msg': msg,
            'type': CFile.get_file_main_name(CFile.path_dir_path(file_name))
        }
        if self.switch_kafka:
            future = self.producer.send('test', key=level, value=kafka_msg, partition=self.CONSTENT_ZERO)
            try:
                future.get(timeout=self.CONSTENT_NINE)
            except kafka_errors:
                traceback.format_exc()

        kwargs["extra"] = {
            "file_name": file_name,
            "line_no": file_no
        }

        if level == self.LOG_INFO:
            self.logger.info(msg, *args, **kwargs)
        elif level == self.LOG_DEBUG:
            self.logger.debug(msg, *args, **kwargs)
        elif level == self.LOG_WARNING:
            self.logger.warning(msg, *args, **kwargs)
        elif level == self.LOG_ERROR:
            self.logger.error(msg, *args, **kwargs)
        elif level == self.LOG_CRITICAL:
            self.logger.critical(msg, *args, **kwargs)
        self.handler_console.close()
        self.handler_file.close()

    def debug(self, msg):
        self.__do_process(self.LOG_DEBUG, msg)

    def info(self, msg):
        self.__do_process(self.LOG_INFO, msg)

    def warning(self, msg):
        self.__do_process(self.LOG_WARNING, msg)

    def error(self, msg):
        self.__do_process(self.LOG_ERROR, msg)

    def critical(self, msg):
        self.__do_process(self.LOG_CRITICAL, msg)


if __name__ == '__main__':
    logger = CLogger(True)
    logger.info("name")
