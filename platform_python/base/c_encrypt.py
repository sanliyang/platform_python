# -*- coding: utf-8 -*-
# @Time : 2022/5/23 14:02
# @Author : sanliy
# @File : c_encrypt
# @software: PyCharm
import base64
import hashlib

from base.c_file import CFile
from base.c_process_bar import CProcessBar
from base.c_resource import CResource


class CEncrypt:

    @classmethod
    def str_2_base64(cls, plaint_text):
        return base64.b64encode(plaint_text.encode(CResource.ENCODE_UTF8))

    @classmethod
    def base64_2_str(cls, cipher_text):
        return base64.b64decode(cipher_text).decode(CResource.ENCODE_UTF8)

    @classmethod
    def str_2_md5(cls, plaint_text):
        hash_md5 = hashlib.md5()
        hash_md5.update(plaint_text.encode(CResource.ENCODE_UTF8))
        return hash_md5.hexdigest()

    @classmethod
    def str_2_sha1(cls, plaint_text):
        hash_sha1 = hashlib.sha1()
        hash_sha1.update(plaint_text.encode(CResource.ENCODE_UTF8))
        return hash_sha1.hexdigest()

    @classmethod
    def file_md5(cls, file_name_with_path):
        file_size = CFile.get_file_size(file_name_with_path, CResource.MEMORY_KB)[CResource.CONSTENT_ZERO]
        if CFile.path_is_exist(file_name_with_path):
            with CProcessBar(
                    file_size,
                    f"{CFile.get_file_main_name(file_name_with_path)} 指纹计算"
            ) as cb:
                process_size = CResource.WRITE_FINGERPRINT_BOLCK
                with open(file_name_with_path, 'rb') as f:
                    hash_chunk = hashlib.md5()
                    init_size = CResource.CONSTENT_ZERO
                    while init_size < file_size:
                        chunk = f.read(process_size)
                        hash_chunk.update(chunk)
                        init_size += process_size
                        if init_size > file_size:
                            process_size = process_size - (init_size - file_size)
                        cb.display_process(process_size)
            return hash_chunk.hexdigest()
        return None

    @classmethod
    def file_sha1(cls, file_name_with_path):
        file_size = CFile.get_file_size(file_name_with_path, CResource.MEMORY_KB)[CResource.CONSTENT_ZERO]
        if CFile.path_is_exist(file_name_with_path):
            with CProcessBar(
                    file_size,
                    f"{CFile.get_file_main_name(file_name_with_path)} 指纹计算"
            ) as cb:
                process_size = CResource.WRITE_FINGERPRINT_BOLCK
                with open(file_name_with_path, 'rb') as f:
                    hash_chunk = hashlib.sha1()
                    init_size = CResource.CONSTENT_ZERO
                    while init_size < file_size:
                        chunk = f.read(process_size)
                        hash_chunk.update(chunk)
                        init_size += process_size
                        if init_size > file_size:
                            process_size = process_size - (init_size - file_size)
                        cb.display_process(process_size)
            return hash_chunk.hexdigest()
        return None


if __name__ == '__main__':
    # z = "test"
    # x = CEncrypt.str_2_base64(z)
    # print(x)
    # y = CEncrypt.base64_2_str(x)
    # print(y)
    # k = CEncrypt.str_2_md5(z)
    # print(k)
    # 文件指纹获取
    file_fingerprint = CEncrypt.file_sha1(r"D:\工具\Windows10\Windows 10 x64-s001.vmdk")
    print(file_fingerprint)
