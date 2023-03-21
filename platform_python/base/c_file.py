# -*- coding: utf-8 -*-
# @Time : 2022/5/13 17:54
# @Author : sanliy
# @File : CFile
# @software: PyCharm
import os
import shutil
import pathlib
from base.c_resource import CResource


class CFile:

    @classmethod
    def path_join(cls, one_path, other_path):
        return pathlib.Path.home() / one_path / other_path

    @classmethod
    def get_file_main_name(cls, path_with_name):
        return pathlib.Path(path_with_name).stem

    @classmethod
    def get_name_with_suffix(cls, path_with_name):
        return pathlib.Path(path_with_name).name

    @classmethod
    def get_suffix(cls, file_path):
        return pathlib.Path(file_path).suffix

    @classmethod
    def path_is_exist(cls, path):
        return os.path.exists(path)

    @classmethod
    def is_file(cls, path):
        return pathlib.Path(path).is_file()

    @classmethod
    def is_dir(cls, path):
        return pathlib.Path(path).is_dir()

    @classmethod
    def check_work_dir(cls, work_dir):
        os.chdir(work_dir)

    @classmethod
    def get_file_size(cls, path, unit=CResource.MEMORY_KB):
        size_byte = os.path.getsize(path)
        if unit == CResource.MEMORY_KB:
            return size_byte / float(CResource.AWESOME), CResource.MEMORY_KB
        elif unit == CResource.MEMORY_MB:
            return size_byte / float(CResource.AWESOME * CResource.AWESOME), CResource.MEMORY_MB

    @classmethod
    def get_file_add_time(cls, file_name_with_path):
        return os.path.getctime(file_name_with_path)

    @classmethod
    def mk_dir(cls, path, parents=True):
        """

        :param path:
        :param parents: 为True可以创建多级目录
        :return: 为None表示创建成功
        """
        return pathlib.Path(path).mkdir(parents=parents)

    @classmethod
    def rename_file(cls, path, new_name):
        file_obj = pathlib.Path(path)
        new_file = file_obj.with_name(new_name)
        file_obj.replace(new_file)

    @classmethod
    def change_suffix(cls, file_path, new_suffix):
        file_obj = pathlib.Path(file_path)
        new_file = file_obj.with_suffix(new_suffix)
        file_obj.replace(new_file)

    @classmethod
    def add_suffix(cls, path, add_suffix):
        if add_suffix.startswith("."):
            return f"{path}{add_suffix}"
        else:
            return f"{path}.{add_suffix}"

    @classmethod
    def unlink(cls, path):
        pathlib.Path(path).unlink()

    @classmethod
    def path_dir_path(cls, path):
        file_obj = pathlib.Path(path)
        return file_obj.parent

    @classmethod
    def get_all_parents_path(cls, path):
        file_obj = pathlib.Path(path)
        return file_obj.parents

    @classmethod
    def get_relative_path(cls, file_path, root_path):
        file_obj = pathlib.Path(file_path)
        return file_obj.relative_to(root_path)

    @classmethod
    def file_root_path(cls, path):
        file_obj = pathlib.Path(path)
        return file_obj.anchor

    @classmethod
    def get_absolute_path(cls, relative_path):
        return os.path.abspath(relative_path)

    @classmethod
    def get_work_dir_current_file(cls):
        return os.getcwd()

    @classmethod
    def get_project_root_path(cls):
        return cls.path_dir_path(cls.path_dir_path(__file__))

    @classmethod
    def copy_file_without_attr(cls, source_file, target_file, follow_symlinks):
        shutil.copyfile(source_file, target_file, follow_symlinks=follow_symlinks)

    @classmethod
    def copy_file_with_attr(cls, source_file, target_file, follow_symlinks):
        """
        :param follow_symlinks: True 允许以创建软连接的方式拷贝
        :param source_file:
        :param target_file:
        :return:
        """
        shutil.copy2(source_file, target_file, follow_symlinks=follow_symlinks)

    @classmethod
    def copy_dir(cls, source_dir, target_dir):
        shutil.copytree(source_dir, target_dir)

    @classmethod
    def move_file_or_dir(cls, source_file, target_path):
        shutil.move(source_file, target_path)

    @classmethod
    def remove_dir(cls, dir_path):
        """
        递归删除文件夹
        :param dir_path:
        :return:
        """
        shutil.rmtree(dir_path)

    @classmethod
    def remove_file(cls, file_path):
        os.remove(file_path)

    @classmethod
    def touch_file(cls, file_path):
        """

        :param file_path:
        :return: 为None 表示该文件已经存在
        """
        return pathlib.Path(file_path).touch(exist_ok=True)

    @classmethod
    def find_file_from_path(cls, path, wildcard, recursive):
        """

        :param path: 路径
        :param wildcard: 通配符
        :param recursive: 是否递归
        :return:
        """
        if recursive:
            return list(pathlib.Path(path).rglob(wildcard))
        else:
            return list(pathlib.Path(path).glob(wildcard))

    @classmethod
    def check_path(cls, path, wildcard):
        return pathlib.Path(path).match(wildcard)


if __name__ == '__main__':
    # dir_path = CFile.path_dir_path("./c_file.py")
    # print(dir_path)
    # print(CFile.get_work_dir_current_file())
    # print(CFile.get_project_root_path())
    #
    # print(CFile.find_file_from_path("d:/platform_python", "*.py", True))

    # file_size, size_unit = CFile.get_file_size(r"D:\gdbgdb\530402红塔区.gdb\a00000029.gdbtable", "KB")
    # print(file_size, size_unit)
    # file_list = CFile.find_file_from_path(r"D:\测试", "*", True)
    # root_list = [r"D:\测试"] * len(file_list)
    # print(file_list)
    # results = map(CFile.get_relative_path, file_list, root_list)
    # print(results)
    # for result in results:
    #     print(result)

    print(CFile.mk_dir("{sas/sas}"))

