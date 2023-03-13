# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name loganysystem
@editor->name Sanliy
@file->name logger.py
@create->time 2023/3/8-16:02
@desc->
++++++++++++++++++++++++++++++++++++++ """
import json
import logging.handlers
import inspect
import os
import traceback

from kafka import KafkaProducer
from kafka.errors import kafka_errors


class CLogger:

    def __init__(self, switch_kafka=True):
        self.switch_kafka = switch_kafka
        self.file_name = None
        self.fileno = None
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(file_name)s - [line:%(line_no)d] - "
            "%(levelname)s - [%(funcName)s] - [日志信息]: %(message)s "
        )
        self.logger = logging.getLogger("loganysystem")
        self.handler_console = logging.StreamHandler()
        self.handler_file = logging.FileHandler(filename="test.log")
        self.producer = KafkaProducer(
            bootstrap_servers=['192.168.44.129:9092'],
            key_serializer=lambda k: json.dumps(k).encode(),
            value_serializer=lambda v: json.dumps(v).encode()
        )

    def __set_level(self):
        self.logger.setLevel(logging.DEBUG)

        self.handler_console.setLevel(logging.INFO)

        self.handler_file.setLevel(logging.ERROR)

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
        frame = inspect.stack()[-1]
        file_name = frame[1]
        file_no = frame[2]
        kafka_msg = {
            'file_name': file_name,
            'file_no': file_no,
            'msg': msg,
            'type': os.path.basename(os.path.dirname(file_name))
        }
        if self.switch_kafka:
            future = self.producer.send('test', key=level, value=kafka_msg, partition=0)
            try:
                future.get(timeout=10)
            except kafka_errors:
                traceback.format_exc()

        kwargs["extra"] = {
            "file_name": file_name,
            "line_no": file_no
        }

        if level == 'info':
            self.logger.info(msg, *args, **kwargs)
        elif level == 'debug':
            self.logger.debug(msg, *args, **kwargs)
        elif level == 'warning':
            self.logger.warning(msg, *args, **kwargs)
        elif level == 'error':
            self.logger.error(msg,*args, **kwargs)
        elif level == 'critical':
            self.logger.critical(msg, *args, **kwargs)
        self.handler_console.close()
        self.handler_file.close()

    def debug(self, msg):
        self.__do_process("debug", msg)

    def info(self, msg):
        self.__do_process("info", msg)

    def warning(self, msg):
        self.__do_process("warning", msg)

    def error(self, msg):
        self.__do_process("error", msg)

    def critical(self, msg):
        self.__do_process("critical", msg)


if __name__ == '__main__':
    logger = CLogger(True)
    logger.info("name")
