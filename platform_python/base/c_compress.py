# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name c_compress.py
@create->time 2023/3/17-23:39
@desc->
++++++++++++++++++++++++++++++++++++++ """
import zipfile
import py7zr
import rarfile
import tarfile

from base.c_file import CFile
from base.c_process_bar import CProcessBar
from base.c_resource import CResource


class CCompress(CResource):

    def __init__(self, source_path, target_path, password=None, compress_level=6):
        self.source_path = source_path
        self.target_path = target_path
        self.compress_mapping = {
            ".zip": [self.__compress_with_zip, self.__decompress_with_zip],
            ".gz": [self.__compress_with_tar_gz, self.__decompress_with_tar_gz],
            ".7z": [self.__compress_with_7z, self.__decompress_with_7z],
            ".xz": [self.__compress_with_7z, self.__decompress_with_7z],
            ".bz2": [self.__compress_with_7z, self.__decompress_with_7z],
            ".wim": [self.__compress_with_7z, self.__decompress_with_7z],
            ".rar": ["", self.__decompress_with_rar]
        }
        self.compress_mapping_with_passwod = {
            ".zip": [self.__compress_with_7z, self.__decompress_with_7z],
            ".gz": [self.__compress_with_7z, self.__decompress_with_7z],
            ".7z": [self.__compress_with_7z, self.__decompress_with_7z],
            ".xz": [self.__compress_with_7z, self.__decompress_with_7z],
            ".bz2": [self.__compress_with_7z, self.__decompress_with_7z],
            ".wim": [self.__compress_with_7z, self.__decompress_with_7z],
        }
        self.password = password
        self.compress_level = compress_level

    def __compress_with_tar_gz(self):
        with tarfile.open(self.target_path, "w:gz") as compress_obj:
            # 为了避免压缩文件的时候将目录层级压缩进去，使用切换工作目录的方式
            # source_work_path
            source_work_path = CFile.get_work_dir_current_file()
            # 改变工作目录
            CFile.check_work_dir(CFile.path_dir_path(self.source_path))
            if CFile.is_file(self.source_path):
                compress_obj.add(CFile.get_name_with_suffix(self.source_path))
            if CFile.is_dir(self.source_path):
                file_list_with_path = CFile.find_file_from_path(self.source_path, "*", True)
                root_list_path = [CFile.path_dir_path(self.source_path)] * len(file_list_with_path)
                file_set_relative_path = map(CFile.get_relative_path, file_list_with_path, root_list_path)
                with CProcessBar(
                        len(file_list_with_path),
                        f"{CFile.get_file_main_name(self.source_path)} compressing..."
                ) as cb:
                    for file_relative_path in file_set_relative_path:
                        compress_obj.add(file_relative_path)
                        cb.display_process(self.CONSTENT_ONE)

            # 切换回原先工作目录
            CFile.check_work_dir(source_work_path)

    def __compress_with_7z(self):
        with py7zr.SevenZipFile(self.target_path, "w", password=self.password) as compress_obj:
            # source_work_path
            source_work_path = CFile.get_work_dir_current_file()
            # 改变工作目录
            CFile.check_work_dir(CFile.path_dir_path(self.source_path))
            if CFile.is_file(self.source_path):
                compress_obj.write(CFile.get_name_with_suffix(self.source_path))
            if CFile.is_dir(self.source_path):
                file_list_with_path = CFile.find_file_from_path(self.source_path, "*", True)
                root_list_path = [CFile.path_dir_path(self.source_path)] * len(file_list_with_path)
                file_set_relative_path = map(CFile.get_relative_path, file_list_with_path, root_list_path)
                with CProcessBar(
                        len(file_list_with_path),
                        f"{CFile.get_file_main_name(self.source_path)} compressing..."
                ) as cb:
                    for file_relative_path in file_set_relative_path:
                        compress_obj.write(file_relative_path)
                        cb.display_process(self.CONSTENT_ONE)

            # 切换回原先工作目录
            CFile.check_work_dir(source_work_path)

    def __compress_with_zip(self):
        with zipfile.ZipFile(
                self.target_path,
                "w",
                compresslevel=self.compress_level,
                allowZip64=True
        ) as compress_obj:
            # source_work_path
            source_work_path = CFile.get_work_dir_current_file()
            # 改变工作目录
            CFile.check_work_dir(CFile.path_dir_path(self.source_path))
            if CFile.is_file(self.source_path):
                compress_obj.write(CFile.get_name_with_suffix(self.source_path))
            if CFile.is_dir(self.source_path):
                file_list_with_path = CFile.find_file_from_path(self.source_path, "*", True)
                root_list_path = [CFile.path_dir_path(self.source_path)] * len(file_list_with_path)
                file_set_relative_path = map(CFile.get_relative_path, file_list_with_path, root_list_path)
                with CProcessBar(
                        len(file_list_with_path),
                        f"{CFile.get_file_main_name(self.source_path)} compressing..."
                ) as cb:
                    for file_relative_path in file_set_relative_path:
                        compress_obj.write(
                            file_relative_path,
                            compress_type=zipfile.ZIP_DEFLATED,
                            compresslevel=self.compress_level
                        )
                        cb.display_process(self.CONSTENT_ONE)

            # 切换回原先工作目录
            CFile.check_work_dir(source_work_path)

    def compress(self):
        file_suffix = CFile.get_suffix(self.target_path)
        if not CFile.path_is_exist(self.source_path):
            return None
        if self.password is None:
            self.compress_mapping[file_suffix][self.CONSTENT_ZERO]()
        else:
            self.compress_mapping_with_passwod[file_suffix][self.CONSTENT_ZERO]()

    def __decompress_with_tar_gz(self):
        with tarfile.open(self.source_path, "r:gz") as uncompress_obj:
            # 解压缩到当前文件夹下
            if self.target_path is None:
                uncompress_obj.extractall()
            else:
                if CFile.path_is_exist(self.target_path):
                    uncompress_obj.extractall(self.target_path)
                else:
                    result = CFile.mk_dir(self.target_path)
                    if result is None:
                        uncompress_obj.extractall(self.target_path)

    def __decompress_with_7z(self):
        with py7zr.SevenZipFile(self.source_path, "r", password=self.password) as uncompress_obj:
            # 解压缩到当前文件夹下
            if self.target_path is None:
                uncompress_obj.extractall()
            else:
                if CFile.path_is_exist(self.target_path):
                    uncompress_obj.extractall(self.target_path)
                else:
                    result = CFile.mk_dir(self.target_path)
                    if result is None:
                        uncompress_obj.extractall(self.target_path)

    def __decompress_with_rar(self):
        with rarfile.RarFile(self.source_path, "r") as uncompress_obj:
            # 解压缩到当前文件夹下
            if self.target_path is None:
                uncompress_obj.extractall(pwd=self.password)
            else:
                if CFile.path_is_exist(self.target_path):
                    uncompress_obj.extractall(self.target_path, pwd=self.password)
                else:
                    result = CFile.mk_dir(self.target_path)
                    if result is None:
                        uncompress_obj.extractall(self.target_path, pwd=self.password)

    def __decompress_with_zip(self):
        with zipfile.ZipFile(
                self.source_path,
                "w",
                compresslevel=self.compress_level,
                allowZip64=True
        ) as uncompress_obj:
            # 解压缩到当前文件夹下
            if self.target_path is None:
                uncompress_obj.extractall(pwd=self.password)
            else:
                if CFile.path_is_exist(self.target_path):
                    uncompress_obj.extractall(self.target_path, pwd=self.password)
                else:
                    result = CFile.mk_dir(self.target_path)
                    if result is None:
                        uncompress_obj.extractall(self.target_path, pwd=self.password)

    def decompress(self):
        file_suffix = CFile.get_suffix(self.source_path)
        if not CFile.path_is_exist(self.source_path):
            return None
        if self.password is None:
            self.compress_mapping[file_suffix][self.CONSTENT_ONE]()
        else:
            self.compress_mapping_with_passwod[file_suffix][self.CONSTENT_ONE]()


if __name__ == "__main__":
    cc = CCompress(r"D:\工具\kali-linux-2022.3-vmware-amd64", r"D:\工具\kali-linux-2022.3-vmware-amd64.tar.gz")
    cc.compress()
