# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name loganysystem
@editor->name Sanliy
@file->name get_log_level.py
@create->time 2023/3/8-17:16
@desc->
++++++++++++++++++++++++++++++++++++++ """
import json

from kafka import KafkaConsumer
from c_logger import CLogger
from c_mysql import CMysql

logger = CLogger(False)

om = CMysql()

consumer = KafkaConsumer(
    'test',
    bootstrap_servers=['192.168.44.129:9092'],
    group_id="test",
    auto_offset_reset="earlist"
)
for msg in consumer:
    logger.info(f"消费者正在消费{msg}")
    key = json.loads(msg.key.decode())
    value = json.loads(msg.value.decode())
    file_name = value.get("file_name")
    file_no = value.get("file_no")
    msg = value.get("msg")
    log_type = value.get("type")

    om.execute(
        '''
        insert into system_log(
        log_level, log_file_name, log_file_no, log_msg, log_type
        ) values (
        :key, :log_file_name, :log_file_no, :log_msg, :log_type
        )
        ''', {
            "key": key,
            "log_file_name": file_name,
            "log_file_no": file_no,
            "log_msg": msg,
            "log_type": log_type
        }
    )
om.close()
