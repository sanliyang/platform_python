# -*- coding: utf-8 -*- 
""" ++++++++++++++++++++++++++++++++++++++
@product->name PyCharm
@project->name platform_python
@editor->name Sanliy
@file->name compress_file.py
@create->time 2023/3/20-15:30
@desc->
++++++++++++++++++++++++++++++++++++++ """
from multiprocessing import Pool

from base.c_file import CFile
from base.c_result import CResult
from base.c_utils import CUtils
from base.c_compress import CCompress
from node.base.node_base import NodeBase


class CompressFile(NodeBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_path = None
        self.target_suffix = None
        self.password = None
        self.compress_level = None
        # NodeBase.__init__(self)

    def help(self):
        return '''
        算法名称: 压缩文件算法
        分属类别：compress
        算法作用：这是一个文件压缩算法，可以用来压缩文件和文件夹
        算法接收参数
        {
            "input": ["aa/bb", "cc/dd"],
            "output": [],
            "params": {
                "target_path": "aa/bb",
                "target_suffix": ".zip",
                "password": "123",
                "compress_level": 6
            }
        }
        '''

    def check_params(self):
        result = super().check_params()
        if CResult.result_faild(result):
            return result
        if self.params is None:
            return CResult.merge_result(
                self.NODE_EXCEPTION,
                "请选择设置算法的参数， 因为有一些必要参数未设置，算法将停止运行，请检查后重试!"
            )
        self.target_path = CUtils.dict_value_by_name(self.params, "target_path")
        if not CFile.path_is_exist(self.target_path):
            CFile.mk_dir(self.target_path)
        self.target_suffix = CUtils.dict_value_by_name(self.params, "target_suffix")
        if self.target_suffix is None:
            self.target_suffix = ".zip"
        self.compress_level = CUtils.dict_value_by_name(self.params, "compress_level")
        if self.compress_level is None:
            self.compress_level = 6
        return CResult.merge_result(
            self.RESULT_SUCCESS,
            "输入参数检查成功，算法将继续运行..."
        )

    def check_input(self):
        result = super().check_input()
        if CResult.result_faild(result):
            return result
        if self.input_list == [] or self.input_list is None:
            return CResult.merge_result(
                self.NODE_EXCEPTION,
                "请选择需要压缩的文件, 算法将不再继续往下执行, 请选择文件后重试!"
            )
        return CResult.merge_result(
            self.RESULT_SUCCESS,
            "输入文件检查成功，算法将继续运行..."
        )

    def compress(self, file_name_with_path) -> CResult:
        try:
            file_main_name = CFile.get_file_main_name(file_name_with_path)
            file_name_with_suffix = CFile.add_suffix(file_main_name, self.target_suffix)
            target_path_with_name = CFile.path_join(CFile.path_dir_path(self.target_path), file_name_with_suffix)
            cc = CCompress(file_name_with_path, target_path_with_name, self.password, self.compress_level)
            cc.compress()
            result = CResult.merge_result(
                self.RESULT_SUCCESS,
                f"{file_name_with_path}正在被压缩成{target_path_with_name}..."
            )
        except Exception as error:
            result = CResult.merge_result(
                self.RESULT_FAILD,
                f"{file_name_with_path}压缩失败，具体原因是[{error}], 请检查修正!"
            )
        return result

    def run(self):
        result = super().run()
        if CResult.result_faild(result):
            return result
        result_update = None
        if len(self.input_list) < self.CONSTENT_NINE:
            pool = Pool(len(self.input_list))
        else:
            pool = Pool(self.CONSTENT_NINE)
        compress_results = pool.map(self.compress, self.input_list)
        for compress_result in compress_results:
            if result_update is None:
                result_update = CResult.result_xor(compress_result)
            else:
                result_update = CResult.result_xor(compress_result, result_update)
        target_path_list = [self.target_path] * len(self.input_list)
        self.update_output(list(map(CFile.path_join, target_path_list, self.input_list)))
        self.save_ouput()

        return result_update


if __name__ == '__main__':
    CompressFile.run_test(
        '''
        {
            "input": ["D:/西三旗数据入库/人口数据", "D:/西三旗数据入库/建筑物分层分户数据", "D:/西三旗数据入库/建筑物白模矢量数据"],
            "output": [],
            "params": {
                "target_path": "D:/西三旗数据入库/人口数据",
                "target_suffix": "tar.gz",
                "password": "123",
                "compress_level": 6
            }
        }
        '''
    )
