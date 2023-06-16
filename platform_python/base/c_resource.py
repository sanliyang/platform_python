# -*- coding: utf-8 -*-
# @Time : 2022/5/17 15:01
# @Author : sanliy
# @File : c_resource
# @software: PyCharm
class CResource:
    # result 结果常量
    RESULT_SUCCESS = 0
    RESULT_FAILD = 3

    # node算法 执行结果
    NODE_WAIT = 1
    NODE_PROCESS = 2
    NODE_SUCESS = 0
    NODE_FINISH = -1
    # 人为参数输入为 异常(31)， 算法主体执行中遇到问题为 失败(3)
    NODE_FAILD = 3
    NODE_EXCEPTION = 31

    # 0-9数字常量
    CONSTENT_ZERO = 0
    CONSTENT_ONE = 1
    CONSTENT_TWO = 2
    CONSTENT_THREE = 3
    CONSTENT_FOUR = 4
    CONSTENT_FIVE = 5
    CONSTENT_SIX = 6
    CONSTENT_SEVEN = 7
    CONSTENT_EIGHT = 8
    CONSTENT_NINE = 9

    # 编码方式
    ENCODE_UTF8 = "utf-8"

    # 单位
    MEMORY_KB = "KB"
    MEMORY_MB = "MB"
    MEMORY_GB = "GB"
    MEMORY_TB = "TB"

    # 读写块大小
    WRITE_FINGERPRINT_BOLCK = 8129

    # 常用进制数
    AWESOME = 1024

    # log 状态
    LOG_DEBUG = "debug"
    LOG_INFO = "info"
    LOG_WARNING = "warning"
    LOG_ERROR = "error"
    LOG_CRITICAL = "critical"

    # log name
    LOG_NAME = "platform_logger"

    # node constent name
    NODE_INPUT = "input"
    NODE_OUTPUT = "output"
    NODE_PARAMS = "params"

    # config path
    CONFIG_NAME = "workflow_platform.ini"

    # third_part
    THIRD_PART = "third_part"

